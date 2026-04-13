from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

def generate_sample_data(months=24):
    np.random.seed(42)
    today = datetime.today()
    dates = [today - timedelta(days=30*(months-i)) for i in range(months)]
    trend_in  = np.linspace(8, 14, months)
    trend_out = np.linspace(6, 10, months)
    seasonal  = np.sin(np.linspace(0, 4*np.pi, months)) * 1.5
    df = pd.DataFrame({
        'date':          dates,
        'inflow':        np.round(trend_in  + seasonal + np.random.normal(0,0.4,months), 2),
        'outflow':       np.round(trend_out + seasonal*0.6 + np.random.normal(0,0.3,months), 2),
        'current_ratio': np.round(np.random.uniform(1.8, 2.8, months), 2),
        'quick_ratio':   np.round(np.random.uniform(1.2, 2.1, months), 2),
        'cash_ratio':    np.round(np.random.uniform(0.5, 1.1, months), 2),
    })
    return df

def forecast_cashflow(df, horizon=6, interest_rate=27.0):
    rate_factor_in  = 1 + (interest_rate - 27) * 0.008
    rate_factor_out = 1 + (interest_rate - 27) * 0.005
    X = np.arange(len(df)).reshape(-1,1)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    reg_in  = LinearRegression().fit(X_poly, df['inflow'])
    reg_out = LinearRegression().fit(X_poly, df['outflow'])
    future_X      = np.arange(len(df), len(df)+horizon).reshape(-1,1)
    future_X_poly = poly.transform(future_X)
    seasonal = np.sin(np.linspace(np.pi, 3*np.pi, horizon)) * 0.8
    fin  = np.round(reg_in.predict(future_X_poly)  * rate_factor_in  + seasonal,     2)
    fout = np.round(reg_out.predict(future_X_poly) * rate_factor_out + seasonal*0.5, 2)
    mape = float(np.mean(np.abs((df['inflow'].values - reg_in.predict(X_poly)) / df['inflow'].values)) * 100)
    last = df['date'].iloc[-1]
    dates = [(last + timedelta(days=30*(i+1))).strftime('%b %Y') for i in range(horizon)]
    alerts = []
    for i, (fi, fo, d) in enumerate(zip(fin, fout, dates)):
        pct = fo/fi*100
        if pct > 95:
            alerts.append({'month': d, 'level': 'CRITICAL', 'message': f'التدفق الخارج {pct:.1f}% من الداخل — خطر عجز!', 'color': 'red'})
        elif pct > 85:
            alerts.append({'month': d, 'level': 'WARNING',  'message': f'التدفق الخارج {pct:.1f}% من الداخل — يحتاج مراقبة', 'color': 'amber'})
    return {
        'dates': dates, 'inflow': fin.tolist(), 'outflow': fout.tolist(),
        'net_flow': (fin-fout).tolist(),
        'coverage_pct': np.round(fin/fout*100,1).tolist(),
        'mape': round(mape,2), 'alerts': alerts,
        'current_metrics': {
            'inflow_latest':  round(float(fin[0]),2),
            'outflow_latest': round(float(fout[0]),2),
            'net_latest':     round(float(fin[0]-fout[0]),2),
            'current_ratio':  round(float(df['current_ratio'].iloc[-1]),2),
            'quick_ratio':    round(float(df['quick_ratio'].iloc[-1]),2),
            'cash_ratio':     round(float(df['cash_ratio'].iloc[-1]),2),
        }
    }

df_global = generate_sample_data(24)

@app.route('/health')
def health():
    return jsonify({'status': 'running'})

@app.route('/forecast')
def api_forecast():
    horizon = int(request.args.get('horizon', 6))
    rate    = float(request.args.get('rate', 27.0))
    return jsonify(forecast_cashflow(df_global, horizon, rate))

if __name__ == '__main__':
    print("=" * 50)
    print("  Liquidity Vision API — شغّال!")
    print("  http://localhost:5000")
    print("  افتح LiquidityVision.html في المتصفح")
    print("=" * 50)
    app.run(port=5000, debug=False)
