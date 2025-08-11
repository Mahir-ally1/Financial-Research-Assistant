import json
import numpy as np
import pandas as pd
import yfinance as yf
from strands import tool

@tool
def get_rsi_summary(ticker: str, period: int = 14) -> str:
    """
    Fetch historical stock data, compute RSI, and return RSI summary statistics as JSON.
    """
    try:
        data = yf.Ticker(ticker).history()
        if data.empty:
            return json.dumps({"error": f"No data available for ticker '{ticker}'"})

        df = data.reset_index()
        delta = df['Close'].diff()
        gains = delta.where(delta > 0, 0.0)
        losses = -delta.where(delta < 0, 0.0)

        avg_gain = gains.ewm(span=period, adjust=False).mean()
        avg_loss = losses.ewm(span=period, adjust=False).mean()

        rs = avg_gain / avg_loss.replace({0: np.nan})
        rsi = 100 - (100 / (1 + rs))
        df['RSI'] = rsi

        latest_rsi = float(df['RSI'].iloc[-1])
        date_reported = str(pd.to_datetime(df['Date'].iloc[-1]).date())

        if latest_rsi > 70:
            signal = "OVERBOUGHT (RSI > 70) - Potential sell signal"
        elif latest_rsi < 30:
            signal = "OVERSOLD (RSI < 30) - Potential buy signal"
        else:
            signal = "NEUTRAL (30 < RSI < 70) - No strong signal"

        summary = {
            "Ticker": ticker,
            "Reported_Date": date_reported,
            "Latest_RSI": round(latest_rsi, 2),
            "Signal": signal,
            "Max_RSI": round(float(df['RSI'].max()), 2),
            "Min_RSI": round(float(df['RSI'].min()), 2),
            "Average_RSI": round(float(df['RSI'].mean()), 2),
        }
        return json.dumps(summary)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def get_eps_yoy_growth_summary(ticker: str) -> str:
    """Calculate YoY EPS growth for each quarter and return a summary as JSON."""
    try:
        dat = yf.Ticker(ticker)
        df = dat.quarterly_income_stmt
        if df is None or df.empty:
            return json.dumps({"error": f"No income statement data for '{ticker}'"})

        eps_rows = df.index[df.index.str.contains('EPS', case=False, na=False)]
        if len(eps_rows) == 0:
            return json.dumps({"error": "No EPS-related rows found in income statement"})

        df.columns = pd.to_datetime(df.columns)
        df = df.sort_index(axis=1)

        results = []
        quarter_map = {3: 'Q1', 6: 'Q2', 9: 'Q3', 12: 'Q4'}
        for eps_metric in eps_rows:
            eps_data = df.loc[eps_metric].dropna()
            eps_by_quarter = {}
            for date, value in eps_data.items():
                eps_by_quarter.setdefault(date.month, []).append((date, float(value)))

            for month, quarter_data in eps_by_quarter.items():
                quarter = quarter_map.get(month, f'M{month}')
                quarter_data.sort(key=lambda x: x[0])
                for i in range(1, len(quarter_data)):
                    curr_date, curr_eps = quarter_data[i]
                    prev_date, prev_eps = quarter_data[i - 1]
                    if curr_date.year - prev_date.year == 1:
                        yoy_growth = ( (curr_eps - prev_eps) / abs(prev_eps) * 100 ) if prev_eps != 0 else (
                            float('inf') if curr_eps > 0 else float('-inf') if curr_eps < 0 else 0
                        )
                        results.append({
                            "Metric": eps_metric,
                            "Quarter": quarter,
                            "Current_Date": curr_date.strftime('%Y-%m-%d'),
                            "Current_EPS": round(curr_eps, 4),
                            "Previous_Date": prev_date.strftime('%Y-%m-%d'),
                            "Previous_EPS": round(prev_eps, 4),
                            "EPS_Change": round(curr_eps - prev_eps, 4),
                            "YoY_Growth_Percent": (None if not np.isfinite(yoy_growth) else round(float(yoy_growth), 2)),
                        })

        if not results:
            return json.dumps({"error": "Not enough data for YoY EPS growth calculation"})

        df_res = pd.DataFrame(results)
        valid = pd.to_numeric(df_res['YoY_Growth_Percent'], errors='coerce').dropna()
        summary = {
            "Ticker": ticker,
            "Total_Comparisons": len(results),
            "Average_YoY_Growth": round(float(valid.mean()), 2) if not valid.empty else None,
            "Max_YoY_Growth": round(float(valid.max()), 2) if not valid.empty else None,
            "Min_YoY_Growth": round(float(valid.min()), 2) if not valid.empty else None,
            "Standard_Deviation": round(float(valid.std()), 2) if not valid.empty else None,
            "Details": results,
        }
        return json.dumps(summary, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
