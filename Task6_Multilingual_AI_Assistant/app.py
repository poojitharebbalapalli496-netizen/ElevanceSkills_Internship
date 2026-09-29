import html
import logging

import streamlit as st

from multilingual_engine import MultilingualConversationEngine

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Multilingual AI Customer Service Assistant",
    page_icon="🌐",
    layout="wide",
)

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

LANG_BADGES = {
    "english": ("EN", "English"), "en": ("EN", "English"),
    "hindi": ("हिं", "Hindi"), "hi": ("हिं", "Hindi"),
    "telugu": ("తె", "Telugu"), "te": ("తె", "Telugu"),
    "spanish": ("ES", "Spanish"), "es": ("ES", "Spanish"),
}

EXAMPLES = [
    ("EN", "English", "What is your return policy?"),
    ("हिं", "Hindi", "मैं उत्पाद कब वापस कर सकता हूँ?"),
    ("తె", "Telugu", "ఉత్పత్తిని ఎన్ని రోజుల్లో తిరిగి ఇవ్వవచ్చు?"),
    ("ES", "Spanish", "¿Cuánto tiempo tengo para devolver un producto?"),
]

STATUS_TILES = [
    ("Supported languages", "4"),
    ("Context-aware", "Yes"),
    ("Mixed-language", "Yes"),
    ("Knowledge-grounded", "Yes"),
]

CAPABILITIES = [
    ("🌐", "Automatic language detection"),
    ("🔀", "Mixed-language understanding"),
    ("🧠", "Context retention"),
    ("🎯", "Cross-lingual intent detection"),
    ("📚", "Evidence-based responses"),
]

CSS = """
<style>
.block-container { max-width: 1100px; padding-top: 2rem; padding-bottom: 6rem; }

.app-header {
    border: 1px solid rgba(128,128,128,0.25); border-radius: 16px;
    padding: 1.3rem 1.5rem; margin-bottom: 1rem;
    background: linear-gradient(135deg, rgba(79,107,237,0.12), rgba(79,107,237,0.02));
}
.app-header h1 { font-size: 1.7rem; margin: 0 0 .25rem 0; padding: 0; line-height: 1.25; }
.app-header p { margin: 0; opacity: .8; }
.status-online { display: inline-block; margin-top: .7rem; font-size: .82rem; font-weight: 500;
    padding: .15rem .65rem; border-radius: 999px; background: rgba(34,160,90,0.14); color: #22a05a; }

.tile-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: .6rem; margin-bottom: 1.2rem; }
.tile { border: 1px solid rgba(128,128,128,0.25); border-radius: 12px; padding: .6rem .85rem;
    background: rgba(128,128,128,0.05); }
.tile .label { font-size: .75rem; opacity: .7; }
.tile .value { font-size: 1.15rem; font-weight: 600; }

.badge { display: inline-block; min-width: 2rem; text-align: center; font-size: .75rem;
    font-weight: 600; padding: .1rem .5rem; margin-right: .35rem; border-radius: 6px;
    background: rgba(79,107,237,0.16); color: #4f6bed; border: 1px solid rgba(79,107,237,0.35); }

.side-title { font-size: .72rem; letter-spacing: .08em; text-transform: uppercase;
    opacity: .65; margin: .9rem 0 .4rem 0; font-weight: 600; }
.side-item { padding: .3rem 0; font-size: .92rem; }

.welcome { text-align: center; padding: 1.5rem 1rem .5rem 1rem; }
.welcome h2 { margin-bottom: .2rem; }
.welcome p { opacity: .75; }

[data-testid="stChatMessage"] { border: 1px solid rgba(128,128,128,0.2); border-radius: 14px;
    padding: .8rem 1rem; margin-bottom: .6rem; background: rgba(128,128,128,0.05); }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(79,107,237,0.10); border-color: rgba(79,107,237,0.30); }

.detail-row { display: flex; flex-wrap: wrap; gap: .25rem .75rem; padding: .3rem 0;
    border-bottom: 1px solid rgba(128,128,128,0.15); font-size: .92rem; }
.detail-row:last-child { border-bottom: none; }
.detail-label { min-width: 170px; opacity: .7; }
.detail-value { flex: 1; overflow-wrap: anywhere; }

div.stButton > button { border-radius: 10px; text-align: left; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def esc(value):
    return html.escape(str(value))


def badge(code):
    return f'<span class="badge">{esc(code)}</span>'


def lang_info(value):
    """Return (badge_code, display_name) for a language name or code."""
    key = str(value).strip().lower()
    if key in LANG_BADGES:
        return LANG_BADGES[key]
    return (str(value)[:2].upper(), str(value))


def lang_chip(value):
    code, name = lang_info(value)
    return f"{badge(code)}{esc(name)}"


def prettify(value):
    text = str(value)
    return text.replace("_", " ").title() if "_" in text else text


def format_validation(value):
    """Turn the validation result (bool / str / dict) into a short label."""
    if isinstance(value, dict):
        for key in ("passed", "is_valid", "valid", "approved"):
            if key in value:
                return "Passed" if value[key] else "Failed"
        if value.get("status") is not None:
            return format_validation(value["status"])
        return str(value)
    if isinstance(value, bool):
        return "Passed" if value else "Failed"
    text = str(value)
    if text.strip().lower() in ("passed", "pass", "valid", "ok", "true", "success"):
        return "Passed"
    if text.strip().lower() in ("failed", "fail", "invalid", "false"):
        return "Failed"
    return text


def detail_row(label, value_html):
    return (
        '<div class="detail-row">'
        f'<div class="detail-label">{esc(label)}</div>'
        f'<div class="detail-value">{value_html}</div></div>'
    )


def build_metadata(result):
    langs = result["detected_languages"]
    if isinstance(langs, str):
        langs = [langs]
    return {
        "language": result["language"],
        "detected_languages": list(langs),
        "is_mixed": bool(result["is_mixed_language"]),
        "english_text": result["english_text"],
        "intent": result["intent"],
        "source": result["source"],
        "knowledge_response": result["knowledge_response"],
        "validation": format_validation(result["validation"]),
    }


def render_details(meta):
    rows = []
    if meta["is_mixed"]:
        joined = " + ".join(lang_chip(l) for l in meta["detected_languages"])
        rows.append(detail_row("Detected languages", joined))
    else:
        rows.append(detail_row("Detected language", lang_chip(meta["language"])))
    rows.append(detail_row("Mixed language", "Yes" if meta["is_mixed"] else "No"))
    rows.append(detail_row("Intent", esc(prettify(meta["intent"]))))
    rows.append(detail_row("Knowledge source", esc(prettify(meta["source"]))))
    rows.append(detail_row("Validation", esc(meta["validation"])))
    rows.append(detail_row("English interpretation", esc(meta["english_text"])))
    rows.append(detail_row("Grounded answer (English)", esc(meta["knowledge_response"])))
    with st.expander("🔍 Response Details"):
        st.markdown("".join(rows), unsafe_allow_html=True)


def render_message(message):
    avatar = "🧑" if message["role"] == "user" else "🌐"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["text"])
        meta = message.get("metadata")
        if message["role"] == "assistant" and meta and "language" in meta:
            render_details(meta)


def clear_conversation():
    st.session_state.engine = MultilingualConversationEngine()
    st.session_state.chat_history = []
    st.session_state.pop("pending_prompt", None)


def use_example(text):
    st.session_state.pending_prompt = text


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "engine" not in st.session_state:
    st.session_state.engine = MultilingualConversationEngine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

engine = st.session_state.engine


# ---------------------------------------------------------
# Input (typed message or clicked example)
# ---------------------------------------------------------

typed_input = st.chat_input(
    "Type your message in English, Hindi, Telugu, Spanish, or a mixed-language message..."
)
pending = st.session_state.pop("pending_prompt", None)
user_input = typed_input or pending

if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("### 🌐 Assistant Panel")

    st.markdown('<div class="side-title">Supported Languages</div>', unsafe_allow_html=True)
    st.markdown(
        "".join(
            f'<div class="side-item">{badge(code)}{label}</div>'
            for code, label in [("EN", "English"), ("हिं", "हिन्दी"),
                                ("తె", "తెలుగు"), ("ES", "Español")]
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-title">Capabilities</div>', unsafe_allow_html=True)
    st.markdown(
        "".join(f'<div class="side-item">{icon} {text}</div>' for icon, text in CAPABILITIES),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-title">Open-Source Stack</div>', unsafe_allow_html=True)
    st.caption("NLLB-200 (distilled 600M) · CTranslate2 · langdetect")

    st.divider()
    st.button("🗑️ Clear Conversation", use_container_width=True, on_click=clear_conversation)


# ---------------------------------------------------------
# Header + status tiles
# ---------------------------------------------------------

st.markdown(
    """
<div class="app-header">
<h1>🌐 Multilingual AI Customer Service Assistant</h1>
<p>Context-aware customer support across English, Hindi, Telugu and Spanish</p>
<span class="status-online">● AI Assistant Online</span>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="tile-grid">'
    + "".join(
        f'<div class="tile"><div class="label">{label}</div><div class="value">{value}</div></div>'
        for label, value in STATUS_TILES
    )
    + "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Welcome state or conversation history
# ---------------------------------------------------------

if not st.session_state.chat_history:
    st.markdown(
        '<div class="welcome"><h2>How can I help you today?</h2>'
        "<p>Ask about returns, delivery or membership in any supported language. "
        "Try one of these examples:</p></div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, (code, name, text) in enumerate(EXAMPLES):
        with cols[i % 2]:
            st.button(
                f"{code} · {text}",
                key=f"example_{i}",
                help=f"{name} example",
                use_container_width=True,
                on_click=use_example,
                args=(text,),
            )
else:
    for message in st.session_state.chat_history:
        render_message(message)


# ---------------------------------------------------------
# Process the new message through the multilingual pipeline
# ---------------------------------------------------------

if user_input:
    try:
        with st.chat_message("assistant", avatar="🌐"):
            with st.spinner("Detecting language, resolving intent and translating..."):
                result = engine.answer(user_input)

            response = result["response"]
            metadata = build_metadata(result)

            st.write(response)
            render_details(metadata)

        st.session_state.chat_history.append(
            {"role": "assistant", "text": response, "metadata": metadata}
        )

    except Exception as error:
        logger.exception("Error while processing message")  # full traceback in terminal

        error_message = (
            "I encountered a problem while processing your message. Please try again."
        )
        with st.chat_message("assistant", avatar="🌐"):
            st.error(error_message)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "text": error_message,
                "metadata": {"error": str(error)},
            }
        )