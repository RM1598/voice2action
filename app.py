import streamlit as st
import streamlit.components.v1 as components
from utils.transcribe import transcribe_audio
from utils.organize import organize_tasks

st.set_page_config(page_title="Voice2Action", layout="wide")

TYPE_OPTIONS = ["Task", "Calendar", "Note", "Unclear"]
PRIORITY_OPTIONS = ["High", "Medium", "Low", "Unclear"]
TIME_OPTIONS = ["Today", "Tomorrow", "This week", "Later/someday", "Unclear"]
CONTEXT_OPTIONS = ["Study/work", "Personal", "Errands", "Communication", "Health", "Unclear"]


def safe_index(options, value, fallback=0):
    try:
        return options.index(value)
    except ValueError:
        return fallback


def get_priority_style(priority):
    if priority == "High":
        return {"bg": "#ffe6e6", "border": "#d9534f", "badge": "#d9534f"}
    elif priority == "Medium":
        return {"bg": "#fff4e5", "border": "#f0ad4e", "badge": "#f0ad4e"}
    elif priority == "Low":
        return {"bg": "#e8f5e9", "border": "#5cb85c", "badge": "#5cb85c"}
    else:
        return {"bg": "#f3f4f6", "border": "#6c757d", "badge": "#6c757d"}


def get_context_icon(context):
    icons = {
        "Study/work": "📘",
        "Personal": "👤",
        "Errands": "🛒",
        "Communication": "💬",
        "Health": "❤️",
        "Unclear": "❓"
    }
    return icons.get(context, "❓")


def get_type_badge_color(entry_type):
    colors = {
        "Task": "#2563eb",
        "Calendar": "#7c3aed",
        "Note": "#0f766e",
        "Unclear": "#6b7280"
    }
    return colors.get(entry_type, "#6b7280")


def render_entry_card(entry, index, category):
    entry_type = entry.get("type", "Unclear")
    priority = entry.get("priority", "Unclear")
    time_category = entry.get("time_category", "Unclear")
    context = entry.get("context", "Unclear")
    text = entry.get("text", "Untitled entry")
    uncertainty_note = entry.get("uncertainty_note", "")
    reason = entry.get("reason", "")

    style = get_priority_style(priority)
    context_icon = get_context_icon(context)
    type_color = get_type_badge_color(entry_type)

    uncertainty_html = ""
    if uncertainty_note:
        uncertainty_html = f"""
        <div style="
            margin-top: 10px;
            padding: 8px 10px;
            border-radius: 8px;
            background: #fff1f0;
            color: #a94442;
            font-size: 14px;
        ">
            <strong>Uncertainty:</strong> {uncertainty_note}
        </div>
        """

    reason_html = ""
    if reason:
        reason_html = f"""
        <div style="
            margin-top: 10px;
            color: #555;
            font-size: 14px;
        ">
            <strong>Reason:</strong> {reason}
        </div>
        """

    card_html = f"""
    <div style="
        font-family: Arial, sans-serif;
        background-color: {style['bg']};
        border-left: 6px solid {style['border']};
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    ">
        <div style="
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 12px;
            color: #222;
        ">
            {category} {index + 1}: {text}
        </div>

        <div style="margin-bottom: 10px;">
            <span style="
                display: inline-block;
                background-color: {type_color};
                color: white;
                padding: 5px 10px;
                border-radius: 999px;
                font-size: 13px;
                font-weight: 600;
                margin-right: 8px;
            ">
                {entry_type}
            </span>

            <span style="
                display: inline-block;
                background-color: {style['badge']};
                color: white;
                padding: 5px 10px;
                border-radius: 999px;
                font-size: 13px;
                font-weight: 600;
                margin-right: 8px;
            ">
                {priority}
            </span>

            <span style="
                display: inline-block;
                background-color: #f1f3f5;
                color: #333;
                padding: 5px 10px;
                border-radius: 999px;
                font-size: 13px;
                margin-right: 8px;
            ">
                ⏰ {time_category}
            </span>

            <span style="
                display: inline-block;
                background-color: #f1f3f5;
                color: #333;
                padding: 5px 10px;
                border-radius: 999px;
                font-size: 13px;
            ">
                {context_icon} {context}
            </span>
        </div>

        {reason_html}
        {uncertainty_html}
    </div>
    """

    components.html(card_html, height=190, scrolling=False)


st.title("Voice2Action")
st.write(
    "Voice2Action helps users capture spoken thoughts and review them later as tasks, "
    "calendar items, notes, or unclear entries."
)

st.info(
    "This is a prototype. It supports local transcription and AI-based organization, "
    "while calendar and notes integration are currently simulated."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Capture a voice note")

    audio_recording = st.audio_input("Record a voice note")

    if audio_recording is not None:
        st.audio(audio_recording)

        if st.button("Transcribe recording"):
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(audio_recording)
                st.session_state["transcript"] = transcript

    st.markdown("---")

    audio_file = st.file_uploader(
        "Or upload a short voice note",
        type=["wav", "mp3", "m4a"]
    )

    if audio_file is not None:
        st.audio(audio_file)

        if st.button("Transcribe uploaded file"):
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(audio_file)
                st.session_state["transcript"] = transcript

    st.markdown("---")
    st.subheader("Or use a sample transcript")

    sample_text = st.text_area(
        "Sample transcript input",
        "Tomorrow I need to finish the lab draft, text Anna about the slides, and I should book a dentist appointment next week. Also, I had an idea for my project introduction.",
        height=140
    )

    if st.button("Use sample transcript"):
        st.session_state["transcript"] = sample_text

with col2:
    st.subheader("2. Review transcript")

    if "transcript" not in st.session_state:
        st.info("Record audio, upload a file, or use the sample transcript.")
    else:
        st.caption("This transcript may contain errors. Please review it before organizing.")
        st.session_state["transcript"] = st.text_area(
            "Transcript",
            st.session_state["transcript"],
            height=220
        )

        if st.button("Organize into dashboard"):
            with st.spinner("Classifying entries..."):
                entries = organize_tasks(st.session_state["transcript"])
                st.session_state["entries"] = entries

st.markdown("---")
st.subheader("3. Daily Review Dashboard")

if "entries" not in st.session_state:
    st.info(
        "No organized entries yet. First record or upload audio, or use the sample transcript, "
        "then click 'Organize into dashboard'."
    )
else:
    entries = st.session_state["entries"]

    if not entries:
        st.warning("No meaningful entry found.")
    else:
        grouped = {
            "Task": [],
            "Calendar": [],
            "Note": [],
            "Unclear": []
        }

        for entry in entries:
            entry_type = entry.get("type", "Unclear")
            if entry_type not in grouped:
                entry_type = "Unclear"
            grouped[entry_type].append(entry)

        total_entries = len(entries)
        total_tasks = len(grouped["Task"])
        total_calendar = len(grouped["Calendar"])
        total_notes = len(grouped["Note"])

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        metric_col1.metric("All entries", total_entries)
        metric_col2.metric("Tasks", total_tasks)
        metric_col3.metric("Calendar", total_calendar)
        metric_col4.metric("Notes", total_notes)

        edited_entries = []

        for category in ["Task", "Calendar", "Note", "Unclear"]:
            st.markdown(f"## {category}")

            if not grouped[category]:
                st.info(f"No {category.lower()} entries.")
                continue

            for i, entry in enumerate(grouped[category]):
                render_entry_card(entry, i, category)

                st.markdown(f"#### Edit {category} entry {i + 1}")

                text_value = st.text_input(
                    f"Text {category} {i + 1}",
                    value=entry.get("text", ""),
                    key=f"text_{category}_{i}"
                )

                type_value = st.selectbox(
                    f"Type {category} {i + 1}",
                    TYPE_OPTIONS,
                    index=safe_index(TYPE_OPTIONS, entry.get("type", "Unclear"), fallback=3),
                    key=f"type_{category}_{i}"
                )

                priority_value = st.selectbox(
                    f"Priority {category} {i + 1}",
                    PRIORITY_OPTIONS,
                    index=safe_index(PRIORITY_OPTIONS, entry.get("priority", "Unclear"), fallback=3),
                    key=f"priority_{category}_{i}"
                )

                time_value = st.selectbox(
                    f"Time category {category} {i + 1}",
                    TIME_OPTIONS,
                    index=safe_index(TIME_OPTIONS, entry.get("time_category", "Unclear"), fallback=4),
                    key=f"time_{category}_{i}"
                )

                context_value = st.selectbox(
                    f"Context {category} {i + 1}",
                    CONTEXT_OPTIONS,
                    index=safe_index(CONTEXT_OPTIONS, entry.get("context", "Unclear"), fallback=5),
                    key=f"context_{category}_{i}"
                )

                reason_value = entry.get("reason", "")
                uncertainty_value = entry.get("uncertainty_note", "")

                action_col1, action_col2 = st.columns(2)

                with action_col1:
                    st.button(
                        "Mark for Calendar export",
                        key=f"calendar_export_{category}_{i}"
                    )

                with action_col2:
                    st.button(
                        "Mark for Notes export",
                        key=f"notes_export_{category}_{i}"
                    )

                edited_entries.append({
                    "text": text_value,
                    "type": type_value,
                    "priority": priority_value,
                    "time_category": time_value,
                    "context": context_value,
                    "uncertainty_note": uncertainty_value,
                    "reason": reason_value
                })

                st.divider()

        st.session_state["entries"] = edited_entries

        with st.expander("Show current structured data"):
            st.json(st.session_state["entries"])