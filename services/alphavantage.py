import requests

def fetch_transcript(ticker: str, quarter: str) -> dict:
    """Fetch earnings call transcript JSON from Alpha Vantage."""
    from config.settings import settings
    url = (
        "https://www.alphavantage.co/query"
        f"?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={quarter}&apikey={settings.alphavantage_api_key}"
    )
    r = requests.get(url, timeout=25)
    r.raise_for_status()
    return r.json()
