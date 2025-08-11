import json
import pandas as pd
import yfinance as yf
from strands import tool

@tool
def get_insider_activity_summary(ticker: str) -> str:
    """Fetch insider activity and return a JSON-formatted summary."""
    try:
        dat = yf.Ticker(ticker)
        df = dat.get_insider_purchases()
        if df is None or df.empty:
            return json.dumps({"error": f"No insider activity available for '{ticker}'"})

        # Expect first column to contain metric names, 'Shares' column to contain values
        first_col = df.columns[0]
        purchases = df.loc[df.iloc[:, 0] == 'Purchases', 'Shares'].values[0]
        sales = df.loc[df.iloc[:, 0] == 'Sales', 'Shares'].values[0]
        net_shares = df.loc[df.iloc[:, 0] == 'Net Shares Purchased (Sold)', 'Shares'].values[0]
        pct_net = df.loc[df.iloc[:, 0] == '% Net Shares Purchased (Sold)', 'Shares'].values[0]
        pct_buy = df.loc[df.iloc[:, 0] == '% Buy Shares', 'Shares'].values[0]
        pct_sell = df.loc[df.iloc[:, 0] == '% Sell Shares', 'Shares'].values[0]
        total_held = df.loc[df.iloc[:, 0] == 'Total Insider Shares Held', 'Shares'].values[0]

        reported_date = first_col if "Unnamed" not in first_col else None

        summary = {
            "Ticker": ticker,
            "Reported_Date": reported_date,
            "Purchases_6m": int(purchases),
            "Sales_6m": int(sales),
            "Net_Shares": int(net_shares),
            "Percent_Net_Change": round(float(pct_net) * 100, 2),
            "Percent_Buy": round(float(pct_buy) * 100, 2),
            "Percent_Sell": round(float(pct_sell) * 100, 2),
            "Total_Shares_Held": int(total_held),
            "Net_Bias": "Buying" if net_shares > 0 else "Selling",
        }
        return json.dumps(summary)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def get_institutional_ownership_summary(ticker: str) -> str:
    """Fetch institutional holders and return a JSON-formatted summary."""
    try:
        dat = yf.Ticker(ticker)
        df = dat.get_institutional_holders()
        if df is None or df.empty:
            return json.dumps({"error": f"No institutional holder data available for '{ticker}'"})

        df_sorted = df.sort_values(by='pctHeld', ascending=False)
        top_holders = df_sorted.head(5)

        total_pct_held = float(df['pctHeld'].sum())
        avg_pct_change = float(df['pctChange'].mean()) if 'pctChange' in df.columns else 0.0
        increasing = int(df[df.get('pctChange', pd.Series()) > 0].shape[0]) if 'pctChange' in df.columns else 0
        decreasing = int(df[df.get('pctChange', pd.Series()) < 0].shape[0]) if 'pctChange' in df.columns else 0

        latest_reported_date = pd.to_datetime(df['Date Reported']).max().strftime('%Y-%m-%d') if 'Date Reported' in df.columns else None

        summary = {
            "Ticker": ticker,
            "Reported_Date": latest_reported_date,
            "Top_5_Holders": top_holders[['Holder', 'pctHeld'] + (["pctChange"] if 'pctChange' in df.columns else [])].to_dict(orient='records'),
            "Total_Institutional_Percent_Held": round(total_pct_held * 100, 2),
            "Average_Percent_Change": round(avg_pct_change * 100, 2),
            "Number_Increasing_Stakes": increasing,
            "Number_Decreasing_Stakes": decreasing,
            "Bias": "Accumulating" if avg_pct_change > 0 else "Trimming",
        }
        return json.dumps(summary, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
