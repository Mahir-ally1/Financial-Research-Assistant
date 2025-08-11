from strands import Agent
from agent.prompts import SYSTEM_PROMPT
from agent.tools import (
    get_rsi_summary,
    get_news_sentiment_summary,
    get_insider_activity_summary,
    get_institutional_ownership_summary,
    get_eps_yoy_growth_summary,
    get_earnings_call_summary,
)
from config.settings import settings

agent = Agent(
    model=settings.model_id,
    system_prompt=SYSTEM_PROMPT,
    tools=[
        get_rsi_summary,
        get_news_sentiment_summary,
        get_insider_activity_summary,
        get_institutional_ownership_summary,
        get_eps_yoy_growth_summary,
        get_earnings_call_summary,
    ],
)
