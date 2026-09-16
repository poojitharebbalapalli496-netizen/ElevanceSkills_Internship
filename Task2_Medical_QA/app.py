import streamlit as st
import spacy

from retriever import MedicalRetriever


st.set_page_config(
    page_title="Medical Q&A Chatbot",
    page_icon="🩺"
)


@st.cache_resource
def load_retriever():
    return MedicalRetriever(
        confidence_threshold=0.20
    )


@st.cache_resource
def load_ner_model():
    nlp = spacy.load("en_core_web_sm")

    ruler = nlp.add_pipe(
        "entity_ruler",
        config={"overwrite_ents": True},
        last=True
    )

    patterns = [
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "leukemia"}
            ]
        },
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "diabetes"}
            ]
        },
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "asthma"}
            ]
        },
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "cancer"}
            ]
        },
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "pneumonia"}
            ]
        },
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "arthritis"}
            ]
        },
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "hypertension"}
            ]
        },
        {
            "label": "MEDICAL_CONDITION",
            "pattern": [
                {"LOWER": "slipped"},
                {"LOWER": "capital"},
                {"LOWER": "femoral"},
                {"LOWER": "epiphysis"}
            ]
        }
    ]

    ruler.add_patterns(patterns)

    return nlp


st.title("🩺 Medical Q&A Chatbot")

st.write(
    "Ask a medical question based on the MedQuAD dataset."
)


retriever = load_retriever()
nlp = load_ner_model()


question = st.text_input(
    "Enter your medical question:"
)


if st.button("Get Answer"):

    if not question.strip():

        st.warning(
            "Please enter a medical question."
        )

    else:

        try:

            # Step 1: Retrieve relevant medical answer
            results = retriever.search(
                question,
                top_k=1
            )

            if not results:

                st.warning(
                    "I could not find a sufficiently "
                    "relevant answer in the MedQuAD dataset. "
                    "Please try rephrasing your question."
                )

            else:

                result = results[0]

                st.subheader(
                    "Best Matching Question"
                )

                st.write(
                    result["question"]
                )

                st.subheader(
                    "Similarity"
                )

                st.write(
                    round(result["score"], 3)
                )

                st.subheader(
                    "Answer"
                )

                st.write(
                    result["answer"]
                )

                # Step 2: Named Entity Recognition
                doc = nlp(question)

                medical_entities = [
                    ent
                    for ent in doc.ents
                    if ent.label_ == "MEDICAL_CONDITION"
                ]

                st.subheader(
                    "Detected Medical Entities"
                )

                if medical_entities:

                    for ent in medical_entities:

                        st.write(
                            f"**Entity:** {ent.text}  "
                            f"| **Type:** {ent.label_}"
                        )

                else:

                    st.write(
                        "No medical entities detected."
                    )

        except Exception as error:

            st.error(
                "An error occurred while processing "
                "your question."
            )

            st.caption(
                f"Error details: {error}"
            )