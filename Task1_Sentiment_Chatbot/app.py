import streamlit as st
from transformers import pipeline

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
CONFIDENCE_THRESHOLD = 0.60


@st.cache_resource
def load_sentiment_model():
    return pipeline(
        "sentiment-analysis",
        model=MODEL_NAME
    )


def analyze_sentiment(message):
    model = load_sentiment_model()
    result = model(message)[0]

    sentiment = result["label"].lower()
    confidence = result["score"]

    if confidence < CONFIDENCE_THRESHOLD:
        sentiment = "uncertain"

    return sentiment, confidence


def generate_response(sentiment):
    responses = {
        "positive": (
            "Thank you! 😊 We're happy to know that you are "
            "satisfied with our service."
        ),
        "negative": (
            "I'm sorry to hear that. 😔 We understand your concern "
            "and will do our best to help resolve it."
        ),
        "neutral": (
            "Thank you for contacting us. "
            "How can I assist you further?"
        ),
        "uncertain": (
            "I want to make sure I understand you correctly. "
            "Could you please provide a little more detail?"
        )
    }

    return responses.get(
        sentiment,
        "Thank you for contacting us. How can I assist you?"
    )


st.set_page_config(
    page_title="Customer Service Chatbot",
    page_icon="🤖"
)

st.title("🤖 Customer Service Chatbot")
st.write(
    "Chat with the assistant and see how it responds "
    "based on the sentiment of your message."
)

message = st.text_input("Enter your message:")

if st.button("Send"):
    if not message.strip():
        st.warning("Please enter a message.")
    else:
        try:
            sentiment, confidence = analyze_sentiment(message)
            response = generate_response(sentiment)

            st.write("### Sentiment")
            st.write(sentiment.capitalize())

            st.write("### Confidence")
            st.write(f"{confidence:.2%}")

            st.write("### Chatbot Response")
            st.write(response)

        except Exception as error:
            st.error(
                "Sorry, something went wrong while analyzing "
                "your message. Please try again."
            )
            st.caption(f"Error details: {error}")