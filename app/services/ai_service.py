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


def extract_tasks(text: str) -> list[str]:
    """
    Extract actionable tasks from an email body.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract clear, actionable tasks from emails. "
                    "Return each task as a bullet point. "
                    "If no tasks exist, return an empty list."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.2
    )

    raw_tasks = response.choices[0].message.content.strip()

    # Convert bullet output into Python list
    tasks = [
        line.strip("- ").strip()
        for line in raw_tasks.split("\n")
        if line.strip()
    ]

    return tasks
