from flask import Flask, request, send_file, Response
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io
import json

app = Flask(__name__)


def get_brent_data():
    """Загрузка реальных данных Brent из CSV"""
    try:
        df = pd.read_csv('/path/to/your/data/brent_data.csv')
        df['date'] = pd.to_datetime(df['date'], utc=True).dt.tz_localize(None)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df.dropna()
        if len(df) < 10:
            raise ValueError("Мало данных")
        return df, True
    except Exception as e:
        print(f"CSV недоступен: {e}, использую моделирование")
        np.random.seed(42)
        dates = pd.date_range('2025-03-01', '2026-03-21', freq='B')
        base_price = 74.0
        changes = np.random.normal(0, 0.8, len(dates))
        prices = base_price + np.cumsum(changes)
        prices = np.clip(prices, 62, 88)
        df = pd.DataFrame({'date': dates, 'price': prices.round(2)})
        return df, False


@app.route('/')
def home():
    return "Brent API is working!"


@app.route('/brent', methods=['GET', 'POST'])
def brent_analysis():
    df, is_real = get_brent_data()

    df['ma_7'] = df['price'].rolling(window=7).mean()
    df['ma_30'] = df['price'].rolling(window=30).mean()

    last_month_avg = df[df['date'] >= df['date'].max() - pd.Timedelta(days=30)]['price'].mean()
    prev_month_avg = df[(df['date'] >= df['date'].max() - pd.Timedelta(days=60)) &
                         (df['date'] < df['date'].max() - pd.Timedelta(days=30))]['price'].mean()
    trend = "растущий" if last_month_avg > prev_month_avg else "снижающийся"
    trend_pct = ((last_month_avg - prev_month_avg) / prev_month_avg * 100)

    source = "Yahoo Finance (реальные данные)" if is_real else "Моделирование"

    fmt = request.args.get('format', 'json')

    if fmt == 'image':
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                        gridspec_kw={'height_ratios': [3, 1]})
        title = 'Анализ цен на нефть Brent'
        if is_real:
            title += f'\n{df["date"].min().strftime("%d.%m.%Y")} — {df["date"].max().strftime("%d.%m.%Y")} (Yahoo Finance)'
        fig.suptitle(title, fontsize=14, fontweight='bold')

        dates = df['date'].values
        prices = df['price'].values
        ma7 = df['ma_7'].values
        ma30 = df['ma_30'].values

        ax1.plot(dates, prices, alpha=0.5, label='Дневная цена', color='gray')
        ax1.plot(dates, ma7, label='MA 7 дней', color='#2196F3', linewidth=2)
        ax1.plot(dates, ma30, label='MA 30 дней', color='#FF5722', linewidth=2)
        ax1.set_ylabel('Цена (USD/баррель)')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)

        daily_change = (df['price'].pct_change() * 100).values
        colors = ['green' if x >= 0 else 'red' for x in daily_change]
        ax2.bar(range(len(daily_change)), daily_change, color=colors, alpha=0.6)
        ax2.set_ylabel('Изменение (%)')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linewidth=0.5)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        return send_file(buf, mimetype='image/png')

    result = {
        'avg_price': round(df['price'].mean(), 2),
        'min_price': round(df['price'].min(), 2),
        'max_price': round(df['price'].max(), 2),
        'trend': trend,
        'trend_pct': round(trend_pct, 1),
        'source': source,
        'period': f"{df['date'].min().strftime('%Y-%m-%d')} — {df['date'].max().strftime('%Y-%m-%d')}",
        'last_price': round(df['price'].iloc[-1], 2)
    }
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json; charset=utf-8')


@app.route('/brent/detailed')
def brent_detailed():
    df, is_real = get_brent_data()

    df['ma_7'] = df['price'].rolling(window=7).mean()
    df['ma_30'] = df['price'].rolling(window=30).mean()

    last_month = df[df['date'] >= df['date'].max() - pd.Timedelta(days=30)]
    prev_month = df[(df['date'] >= df['date'].max() - pd.Timedelta(days=60)) &
                     (df['date'] < df['date'].max() - pd.Timedelta(days=30))]

    last_month_avg = last_month['price'].mean()
    prev_month_avg = prev_month['price'].mean()
    trend_pct = ((last_month_avg - prev_month_avg) / prev_month_avg * 100)

    # Последние 30 дней — дневные данные для AI
    recent = df.tail(30).copy()
    daily_data = []
    for _, row in recent.iterrows():
        daily_data.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'price': round(row['price'], 2),
            'ma_7': round(row['ma_7'], 2) if pd.notna(row['ma_7']) else None,
            'ma_30': round(row['ma_30'], 2) if pd.notna(row['ma_30']) else None
        })

    # Волатильность
    df['daily_change'] = df['price'].pct_change() * 100
    volatility_30d = df['daily_change'].tail(30).std()
    volatility_all = df['daily_change'].std()

    result = {
        'summary': {
            'current_price': round(df['price'].iloc[-1], 2),
            'avg_price_6m': round(df['price'].mean(), 2),
            'min_price': round(df['price'].min(), 2),
            'min_date': df.loc[df['price'].idxmin(), 'date'].strftime('%Y-%m-%d'),
            'max_price': round(df['price'].max(), 2),
            'max_date': df.loc[df['price'].idxmax(), 'date'].strftime('%Y-%m-%d'),
            'change_1m_pct': round(trend_pct, 1),
            'avg_last_month': round(last_month_avg, 2),
            'avg_prev_month': round(prev_month_avg, 2),
            'trend': 'растущий' if trend_pct > 0 else 'снижающийся',
            'volatility_30d': round(volatility_30d, 2),
            'volatility_6m': round(volatility_all, 2),
            'period': f"{df['date'].min().strftime('%Y-%m-%d')} — {df['date'].max().strftime('%Y-%m-%d')}",
            'source': 'Yahoo Finance' if is_real else 'Моделирование'
        },
        'daily_prices_last_30d': daily_data
    }

    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json; charset=utf-8')