import os 
from dotenv import load_dotenv
from openai  import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_email(email_text: str) -> str:
    """
    Takes cleaned email text and returns a short summary.
    """

    prompt = f"""
    Summarize the following email in 3 short bullet points.
    Use simple and clear language.

    Email:
    {email_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content