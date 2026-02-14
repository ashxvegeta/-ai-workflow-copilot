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
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract actionable tasks from the email.\n"
                    "Return ONLY bullet points starting with '-'.\n"
                    "If no tasks exist, return NOTHING."
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

    # 🚨 Guard clause
    if raw_tasks in ("", "[]"):
        return []

    tasks = [
        line.strip("- ").strip()
        for line in raw_tasks.split("\n")
        if line.strip().startswith("-")
    ]

    return tasks


def detect_urgency(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the urgency of this email as one of: "
                    "high, medium, or low.\n\n"
                    "Rules:\n"
                    "- Deadlines or time pressure → high\n"
                    "- Requests without strict deadlines → medium\n"
                    "- Informational or FYI emails → low\n\n"
                    "Return ONLY the urgency word."
                )
            },
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content.strip().lower()
