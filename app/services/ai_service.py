import os 
from dotenv import load_dotenv
from openai  import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_email(text: str) -> str:
    """
    Takes plain email text and returns a concise summary using AI.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You summarize emails clearly in 1–2 lines."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()