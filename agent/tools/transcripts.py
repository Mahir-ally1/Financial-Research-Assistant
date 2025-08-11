import json
from strands import tool
from botocore.exceptions import ClientError

from services.alphavantage import fetch_transcript
from services.bedrock import converse_json
from agent.utils import get_most_recent_quarter

PROMPT_TEMPLATE = """
You are an expert financial analyst tasked with summarizing key investment-related developments from a quarterly earnings call transcript.

Your job is to analyze the transcript enclosed in <transcript> tags and identify signals that could positively impact the company’s stock price. Focus especially on announcements related to:
- New product launches
- Management changes
- Positive business developments or guidance

Only base your analysis on the transcript content. If there are no such signals, say so explicitly.
Prioritize insights from company spokespersons (e.g., CEO, CFO) over external analysts or moderators.

Your output must include valid JSON with keys: quarter, summary, new_product, new_management, overall_sentiment.

<transcript>
{transcript}
</transcript>
"""

@tool
def get_earnings_call_summary(ticker: str, quarter: str | None = None) -> str:
    """Fetches earnings call transcript and summarizes with Bedrock, returning JSON string."""
    try:
        if quarter is None:
            quarter = get_most_recent_quarter()

        transcript_data = fetch_transcript(ticker, quarter)
        if (not transcript_data) or ("Information" in transcript_data and "limit" in str(transcript_data.get("Information", "")).lower()):
            return json.dumps({"error": "Transcript not found or API limit exceeded."})

        prompt = PROMPT_TEMPLATE.format(transcript=json.dumps(transcript_data))
        messages = [{"role": "user", "content": [{"text": prompt}]}]
        response_text = converse_json(messages)

        try:
            structured = json.loads(response_text)
            return json.dumps(structured)
        except json.JSONDecodeError:
            return json.dumps({"error": "Model output could not be parsed as JSON.", "raw_output": response_text})
    except (ClientError, Exception) as e:
        return json.dumps({"error": str(e)})
