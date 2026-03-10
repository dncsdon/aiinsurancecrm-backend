import anthropic
from typing import Dict

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def qualify_lead(lead_data: Dict) -> Dict:
    """AI scores leads and suggests next action"""
    prompt = f"""
    Analyze this insurance lead and score 0-100 (100=immediate call):
    Name: {lead_data['name']}
    Email: {lead_data['email']}
    Phone: {lead_data['phone']}
    Notes: {lead_data.get('notes', '')}
    
    FINAL EXPENSE INSURANCE CONTEXT:
    - Target: Seniors 55+, budget $50-150/month
    - Hot signals: Recently lost spouse, health issues, fixed income
    
    Respond JSON only:
    {{
        "score": 85,
        "priority": "high|medium|low",
        "next_action": "call|email|followup",
        "confidence": "high|medium|low",
        "recommended_policy": "final_expense|medicare|life"
    }}
    """
    
    response = await client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Parse AI response (simple JSON extract)
    ai_json = response.content[0].text.strip()
    return eval(ai_json)  # In prod, use proper JSON parser
