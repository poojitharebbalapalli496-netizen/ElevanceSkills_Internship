import copy
import hashlib
import logging
import os
import tempfile
import uuid
from io import BytesIO

import streamlit as st
from PIL import Image

from image_analyzer import ImageAnalyzer
from evidence import EvidenceExtractor
from conversation import ConversationMemory
from reasoning import ReasoningEngine
from validator import ResponseValidator


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Display / application settings
# ==========================================================

# UI-only threshold.
# This does NOT change the reasoning or validation logic.
STRONG_EVIDENCE_THRESHOLD = 0.50

# Analyze an image once and reuse the result for follow-up
# questions about the same image.
CACHE_IMAGE_ANALYSIS = True

ALLOWED_TYPES = ["png", "jpg", "jpeg"]


EXAMPLE_QUESTIONS = [
    "What is shown in the image?",
    "What about that device?",
    "How much RAM does it have?",
    "Is this definitely an HP laptop?",
    "What is the exact model?",
]


REFERENCE_LABELS = {
    "resolved": "Resolved from context",
    "current_image": "Current image",
    "unclear": "Unclear",
}


# ==========================================================
# Page configuration
# ==========================================================

st.set_page_config(
    page_title="Multimodal AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# Light UI styling
# ==========================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# Load backend components
# ==========================================================

@st.cache_resource
def load_image_analyzer():
    return ImageAnalyzer()


@st.cache_resource
def load_evidence_extractor():
    return EvidenceExtractor()


@st.cache_resource
def load_reasoning_engine():
    return ReasoningEngine()


@st.cache_resource
def load_validator():
    return ResponseValidator()


def initialize_memory():
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = ConversationMemory()

    return st.session_state.conversation_memory


analyzer = load_image_analyzer()
extractor = load_evidence_extractor()
reasoning_engine = load_reasoning_engine()
validator = load_validator()
memory = initialize_memory()


# ==========================================================
# Helper functions
# ==========================================================

def create_image_id(image_bytes):
    """Create a stable identifier for the uploaded image."""

    return hashlib.sha256(image_bytes).hexdigest()


def is_valid_image(image_bytes):
    """Check whether uploaded bytes represent a readable image."""

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()

        return True

    except Exception:
        return False


def escape_md(text):
    """
    Escape dollar signs so user/model text is not interpreted
    as Streamlit LaTeX.
    """

    return str(text).replace("$", r"\$")


def to_float(value):
    """Safely convert a value to float."""

    try:
        return float(value)

    except (TypeError, ValueError):
        return None


def fmt_pct(value):
    """Format a numeric value as a percentage."""

    number = to_float(value)

    if number is None:
        return "N/A"

    return f"{number:.2%}"


def pretty(value):
    """Convert internal labels into readable UI text."""

    if value is None or value == "":
        return "N/A"

    return str(value).replace("_", " ").title()


def reference_label(reference_status):
    """Convert internal reference status to readable text."""

    if not reference_status:
        return "Not applicable"

    return REFERENCE_LABELS.get(
        reference_status,
        pretty(reference_status)
    )


def validation_outcome(validation):
    """
    Convert validator output into:
    label, Streamlit message level, explanatory message.
    """

    if not validation.get("valid"):
        return (
            "FAIL",
            "error",
            "Response validation failed. "
            "A safe fallback response was used."
        )

    if validation.get("status") == "pass":
        return (
            "PASS",
            "success",
            "Response validated against available visual evidence."
        )

    return (
        "WARN",
        "warning",
        "Response is cautious because the available evidence is limited."
    )


# ==========================================================
# Temporary image handling
# ==========================================================

def get_upload_path():
    """
    Create a unique temporary image path for this Streamlit session.

    This prevents different users/sessions from overwriting
    the same uploaded_image.png file.
    """

    if "upload_path" not in st.session_state:

        st.session_state.upload_path = os.path.join(
            tempfile.gettempdir(),
            f"multimodal_upload_{uuid.uuid4().hex}.png"
        )

    return st.session_state.upload_path


# ==========================================================
# Image analysis caching
# ==========================================================

def get_analysis_result(image_bytes, image_id):
    """
    Analyze the image once and reuse the result when the
    same image is used for follow-up questions.
    """

    cached = st.session_state.get("analysis_cache")

    if (
        CACHE_IMAGE_ANALYSIS
        and cached is not None
        and cached.get("image_id") == image_id
    ):
        return copy.deepcopy(cached["result"])

    image_path = get_upload_path()

    with open(image_path, "wb") as file:
        file.write(image_bytes)

    result = analyzer.analyze(image_path)

    st.session_state.analysis_cache = {
        "image_id": image_id,
        "result": copy.deepcopy(result)
    }

    return result


# ==========================================================
# Existing Task 5 pipeline
# ==========================================================

def run_pipeline(question, image_bytes, image_id):
    """
    Run the existing multimodal pipeline.

    Pipeline:
    Image analysis
        ↓
    Evidence extraction
        ↓
    Conversation context
        ↓
    Reasoning
        ↓
    Response validation
        ↓
    Memory storage
    """

    # ------------------------------------------------------
    # Step 1: Image analysis
    # ------------------------------------------------------

    analysis_result = get_analysis_result(
        image_bytes,
        image_id
    )

    # ------------------------------------------------------
    # Step 2: Evidence extraction
    # ------------------------------------------------------

    evidence = extractor.extract(
        analysis_result
    )

    # ------------------------------------------------------
    # Step 3: Previous conversation
    # ------------------------------------------------------

    previous_turn = memory.get_last_turn()

    # ------------------------------------------------------
    # Step 4: Evidence-based reasoning
    # ------------------------------------------------------

    reasoning_result = reasoning_engine.reason(
        question,
        evidence,
        previous_turn
    )

    # ------------------------------------------------------
    # Step 5: Response validation
    # ------------------------------------------------------

    validation_result = validator.validate(
        reasoning_result,
        evidence
    )

    final_response = validation_result["response"]

    # ------------------------------------------------------
    # Step 6: Store structured memory
    # ------------------------------------------------------

    unresolved_ambiguities = []

    if reasoning_result.get("status") == "ambiguous":

        unresolved_ambiguities.append(
            "User reference could not be resolved."
        )

    memory.add_turn(
        user_message=question,
        assistant_response=final_response,
        image_id=image_id,
        evidence=evidence,
        intent=reasoning_result.get("intent"),
        unresolved_ambiguities=unresolved_ambiguities
    )

    return {
        "image_id": image_id,
        "question": question,
        "response": final_response,
        "evidence": evidence,
        "reasoning": reasoning_result,
        "validation": validation_result
    }


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.header("Session")

turn_counter = st.sidebar.empty()


def update_turn_counter():
    turn_counter.metric(
        "Stored conversation turns",
        len(memory.get_history())
    )


update_turn_counter()


if st.sidebar.button(
    "Clear conversation",
    width="stretch"
):

    memory.clear()

    for key in (
        "current_image_id",
        "last_result",
        "analysis_cache"
    ):
        st.session_state.pop(key, None)

    update_turn_counter()

    st.rerun()


st.sidebar.caption(
    "Clears stored conversation turns and the current result. "
    "The uploaded image remains selected."
)


# ==========================================================
# Sidebar information
# ==========================================================

with st.sidebar.expander("How it works"):

    st.markdown(
        """
        **1. Image analysis**

        MobileNet V3 Small classification and BLIP image captioning.

        **2. Evidence extraction**

        Visual labels, confidence values and caption are collected.

        **3. Reasoning**

        The assistant detects intent, uses conversation context
        and handles ambiguous references.

        **4. Validation**

        The generated response is checked against the available
        visual evidence before being displayed.
        """
    )

    st.caption(
        "The uploaded image is written to a temporary file "
        "for model analysis."
    )


# ==========================================================
# UI rendering functions
# ==========================================================

def render_examples():

    with st.expander("Example questions"):

        for example in EXAMPLE_QUESTIONS:
            st.markdown(
                f"- {escape_md(example)}"
            )

        st.caption(
            "Questions about information that cannot be reliably "
            "seen in the image, such as RAM or an exact model, "
            "may receive a cautious response."
        )


def render_footer():

    st.divider()

    st.caption(
        "Responses are based on available visual evidence and "
        "may be incomplete. The assistant avoids unsupported claims."
    )


def render_empty_state():

    with st.container(border=True):

        st.subheader("Get started")

        st.write(
            "Upload a PNG or JPEG image and ask a question about it. "
            "Follow-up questions can refer to earlier conversation context."
        )

        st.markdown(
            """
            1. **Upload** an image
            2. **Ask** a question
            3. **Review** the response, evidence and validation
            """
        )

        render_examples()


def render_response(result):

    label, _, _ = validation_outcome(
        result["validation"]
    )

    with st.container(border=True):

        st.subheader("Assistant response")

        st.caption(
            "Question: "
            + escape_md(result["question"])
        )

        st.markdown(
            escape_md(result["response"])
        )

        if label == "PASS":

            st.success(
                "Validation result: PASS"
            )

        elif label == "WARN":

            st.warning(
                "Validation result: WARN — "
                "response is intentionally cautious."
            )

        else:

            st.error(
                "Validation result: FAIL"
            )


def render_evidence(evidence):

    with st.container(border=True):

        st.subheader("Evidence used")

        st.caption(
            "Visual evidence extracted from the uploaded image. "
            "The reasoning step uses this evidence."
        )

        primary_label = evidence.get(
            "primary_label"
        )

        if primary_label:

            confidence = to_float(
                evidence.get("primary_confidence")
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Primary classification",
                str(primary_label)
            )

            col2.metric(
                "Confidence",
                fmt_pct(confidence)
            )

            if confidence is not None:

                if confidence >= STRONG_EVIDENCE_THRESHOLD:

                    st.success(
                        "Strong visual evidence: confidence is "
                        f"{confidence:.2%}."
                    )

                else:

                    st.warning(
                        "Limited visual evidence: confidence is "
                        f"{confidence:.2%}."
                    )

        else:

            st.info(
                "No primary classification is available."
            )

        caption = evidence.get("caption")

        if caption:

            st.markdown(
                "**Image caption:** "
                + escape_md(caption)
            )

        classifications = evidence.get(
            "visual_labels",
            []
        )

        if classifications:

            with st.expander("Top visual classifications"):

                for prediction in classifications:

                    confidence = to_float(
                        prediction.get("confidence")
                    )

                    bar_value = min(
                        max(confidence or 0.0, 0.0),
                        1.0
                    )

                    label = prediction.get(
                        "label",
                        "Unknown"
                    )

                    st.progress(
                        bar_value,
                        text=(
                            f"{escape_md(label)}: "
                            f"{fmt_pct(confidence)}"
                        )
                    )


def render_reasoning(reasoning):

    with st.container(border=True):

        st.subheader("Reasoning")

        st.caption(
            "How the question was interpreted and how the "
            "available evidence was used."
        )

        row1 = st.columns(2)

        row1[0].metric(
            "Detected intent",
            pretty(
                reasoning.get("intent")
            )
        )

        row1[1].metric(
            "Reasoning status",
            pretty(
                reasoning.get("status")
            )
        )

        reference_status = reasoning.get(
            "reference_status"
        )

        row2 = st.columns(2)

        row2[0].metric(
            "Evidence confidence",
            fmt_pct(
                reasoning.get("confidence")
            )
        )

        row2[1].metric(
            "Reference status",
            reference_label(
                reference_status
            )
        )

        if reference_status == "resolved":

            st.info(
                "Previous conversation context was used "
                "to resolve the reference."
            )

        elif reference_status == "current_image":

            st.info(
                "The reference was interpreted using "
                "the currently uploaded image."
            )

        elif reference_status == "unclear":

            st.warning(
                "The conversation reference could not "
                "be resolved confidently."
            )


def render_validation(validation):

    label, level, message = validation_outcome(
        validation
    )

    with st.container(border=True):

        st.subheader("Response validation")

        st.caption(
            "The response is checked against the extracted "
            "visual evidence before being displayed."
        )

        getattr(st, level)(
            f"**{label}** — {message}"
        )

        with st.expander("Validation details"):

            st.write(
                "**Validation status:** "
                + str(
                    validation.get("status")
                )
            )

            st.write(
                "**Valid:** "
                + str(
                    validation.get("valid")
                )
            )

            reasons = validation.get(
                "reasons"
            )

            if reasons:

                st.write(
                    "**Validation reasons:**"
                )

                for reason in reasons:

                    st.write(
                        "- "
                        + escape_md(reason)
                    )

            else:

                st.write(
                    "No additional validation notes."
                )


def render_history():

    history = memory.get_history()

    with st.container(border=True):

        st.subheader("Conversation history")

        st.caption(
            "Stored turns that can be used to resolve "
            "follow-up references for the current image."
        )

        if not history:

            st.info(
                "No conversation history yet."
            )

            return

        for index, turn in enumerate(
            history,
            start=1
        ):

            with st.chat_message("user"):

                st.markdown(
                    escape_md(
                        turn.get(
                            "user_question",
                            ""
                        )
                    )
                )

            with st.chat_message("assistant"):

                st.markdown(
                    escape_md(
                        turn.get(
                            "answer",
                            ""
                        )
                    )
                )

                if turn.get("intent"):

                    st.caption(
                        f"Turn {index} | Intent: "
                        f"{pretty(turn['intent'])}"
                    )


# ==========================================================
# Application header
# ==========================================================

st.title(
    "Multimodal AI Assistant"
)

st.caption(
    "Evidence-based visual question answering with "
    "conversation memory, ambiguity handling and "
    "response validation."
)


# ==========================================================
# Image upload
# ==========================================================

st.subheader("Upload image")

uploaded_file = st.file_uploader(
    "Select a PNG or JPEG image",
    type=ALLOWED_TYPES,
    help=(
        "The image is analyzed to extract visual evidence "
        "for your questions."
    )
)


# ==========================================================
# Empty state
# ==========================================================

if uploaded_file is None:

    render_empty_state()
    render_footer()

    st.stop()


# ==========================================================
# Validate uploaded image
# ==========================================================

image_bytes = uploaded_file.getvalue()


if not is_valid_image(image_bytes):

    st.error(
        "This file could not be read as an image. "
        "Please upload a valid PNG or JPEG file."
    )

    st.stop()


image_id = create_image_id(
    image_bytes
)


# ==========================================================
# Detect image changes
# ==========================================================

previous_image_id = st.session_state.get(
    "current_image_id"
)


if (
    previous_image_id is not None
    and previous_image_id != image_id
):

    # The conversation belongs to the previous image.
    memory.clear()

    # Remove previous result/cache.
    st.session_state.pop(
        "last_result",
        None
    )

    st.session_state.pop(
        "analysis_cache",
        None
    )

    update_turn_counter()

    st.info(
        "A new image was uploaded. "
        "Previous image context has been cleared."
    )


st.session_state.current_image_id = image_id


# ==========================================================
# Image preview + question
# ==========================================================

left_column, right_column = st.columns(
    [1, 1],
    gap="large"
)


# ----------------------------------------------------------
# Image preview
# ----------------------------------------------------------

with left_column:

    st.subheader(
        "Image preview"
    )

    with st.container(border=True):

        st.image(
            image_bytes,
            caption="Uploaded image",
            width="stretch"
        )


# ----------------------------------------------------------
# Question input
# ----------------------------------------------------------

with right_column:

    st.subheader(
        "Ask a question"
    )

    st.caption(
        "Ask about information visible in the image. "
        "Follow-up questions can refer to previous answers."
    )

    with st.form(
        "question_form",
        clear_on_submit=True
    ):

        question = st.text_input(
            "Your question",
            placeholder=(
                "Example: What is shown in the image?"
            )
        )

        submitted = st.form_submit_button(
            "Analyze and answer",
            type="primary",
            width="stretch"
        )

    render_examples()


# ==========================================================
# Process question
# ==========================================================

if submitted:

    if not question.strip():

        st.warning(
            "Please enter a question about the image."
        )

    else:

        try:

            with st.spinner(
                "Analyzing image and preparing response..."
            ):

                st.session_state.last_result = (
                    run_pipeline(
                        question,
                        image_bytes,
                        image_id
                    )
                )

            update_turn_counter()

        except Exception as error:

            # Full traceback goes to the application log,
            # not directly onto the main UI.
            logger.exception(
                "Task 5 processing failed"
            )

            st.error(
                "Something went wrong while processing "
                "the image or question. Please try again."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(
                    f"{type(error).__name__}: {error}"
                )


# ==========================================================
# Results
# ==========================================================

st.divider()


result = st.session_state.get(
    "last_result"
)


# ----------------------------------------------------------
# No result yet
# ----------------------------------------------------------

if (
    result is None
    or result.get("image_id") != image_id
):

    st.info(
        "Enter a question above to see the assistant's "
        "response and the evidence behind it."
    )


# ----------------------------------------------------------
# Display results
# ----------------------------------------------------------

else:

    render_response(
        result
    )

    st.subheader(
        "Analysis details"
    )

    evidence_column, analysis_column = st.columns(
        [1, 1],
        gap="large"
    )

    with evidence_column:

        render_evidence(
            result["evidence"]
        )

    with analysis_column:

        render_reasoning(
            result["reasoning"]
        )

        render_validation(
            result["validation"]
        )


# ==========================================================
# Conversation history
# ==========================================================

render_history()


# ==========================================================
# Footer
# ==========================================================

render_footer()