import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

PROMPT_TEMPLATE = """
You are an assistant that organizes a transcript into structured entries.

Return ONLY valid JSON.
Return a JSON array.

Each item in the array must have exactly these fields:
- text
- type
- priority
- time_category
- context
- uncertainty_note
- reason

Allowed values:
type: Task, Calendar, Note, Unclear
priority: High, Medium, Low, Unclear
time_category: Today, Tomorrow, This week, Later/someday, Unclear
context: Study/work, Personal, Errands, Communication, Health, Unclear

Rules:
- Not everything is a task.
- Calendar = events, appointments, or things tied to a date/time.
- Note = general thoughts, ideas, or information that is not directly actionable.
- Task = actionable thing the user should do.
- If unclear, use type = Unclear.
- Do not invent information that is not implied by the transcript.
- If no meaningful content exists, return [].
- uncertainty_note should be an empty string if there is no uncertainty.
- reason should briefly explain why the type/labels were chosen.
- Do not include any text outside the JSON.

Transcript:
{transcript}
"""


def organize_tasks(transcript):
    """
    Send transcript to Ollama and parse the response as JSON.
    """
    prompt = PROMPT_TEMPLATE.format(transcript=transcript)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()

    raw_text = response.json().get("response", "").strip()

    try:
        parsed = json.loads(raw_text)

        if isinstance(parsed, list):
            return parsed

        return [{
            "text": "Model output was not a list",
            "type": "Unclear",
            "priority": "Unclear",
            "time_category": "Unclear",
            "context": "Unclear",
            "uncertainty_note": "The model returned JSON, but not in the expected list format.",
            "reason": "Fallback result due to formatting issue."
        }]

    except json.JSONDecodeError:
        return [{
            "text": "Could not parse model output",
            "type": "Unclear",
            "priority": "Unclear",
            "time_category": "Unclear",
            "context": "Unclear",
            "uncertainty_note": "The model response was not valid JSON.",
            "reason": "Fallback result due to parsing error."
        }]