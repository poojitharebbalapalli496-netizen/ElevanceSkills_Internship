import streamlit as st

from search_engine import search_papers
from summarizer import summarize_text
from information_extractor import extract_information
from llm_explainer import explain_concept
from visualization import create_concept_visualization


st.set_page_config(
    page_title="Research Expert Chatbot",
    page_icon="🔬",
    layout="wide"
)

st.title("Research Expert Chatbot")
st.write(
    "AI-powered assistant for exploring Computer Science research papers."
)

st.sidebar.title("Research Tools")

option = st.sidebar.selectbox(
    "Choose a feature",
    [
        "Paper Search",
        "Paper Summarization",
        "Information Extraction",
        "Concept Explanation",
        "Concept Visualization"
    ]
)


# -------------------------------
# PAPER SEARCH
# -------------------------------

if option == "Paper Search":

    st.header("Search Research Papers")

    query = st.text_input(
        "Enter research topic",
        placeholder="Example: machine learning"
    )

    if st.button("Search Papers"):

        if query.strip():

            with st.spinner("Searching research papers..."):

                results = search_papers(query)

            if results:

                for i, paper in enumerate(results, 1):

                    st.subheader(
                        f"{i}. {paper['title']}"
                    )

                    st.write(
                        f"Similarity Score: {paper['score']:.3f}"
                    )

                    st.write(paper["abstract"])

                    st.divider()

            else:

                st.warning("No research papers found.")

        else:

            st.warning("Please enter a research topic.")


# -------------------------------
# SUMMARIZATION
# -------------------------------

elif option == "Paper Summarization":

    st.header("Research Paper Summarization")

    abstract = st.text_area(
        "Enter research abstract",
        height=250
    )

    if st.button("Summarize Paper"):

        if abstract.strip():

            with st.spinner("Generating summary..."):

                summary = summarize_text(abstract)

            st.subheader("Generated Summary")

            st.write(summary)

        else:

            st.warning("Please enter an abstract.")


# -------------------------------
# INFORMATION EXTRACTION
# -------------------------------

elif option == "Information Extraction":

    st.header("Research Information Extraction")

    abstract = st.text_area(
        "Enter research abstract",
        height=250
    )

    if st.button("Extract Information"):

        if abstract.strip():

            with st.spinner("Extracting information..."):

                result = extract_information(abstract)

            st.subheader("Key Concepts")

            for concept in result["Key Concepts"]:
                st.write("•", concept)

            st.subheader("Evaluation Metrics")

            if result["Evaluation Metrics"]:

                for metric in result["Evaluation Metrics"]:
                    st.write("•", metric)

            else:

                st.write("No evaluation metrics detected.")

            st.subheader("Challenges")

            if result["Challenges"]:

                for challenge in result["Challenges"]:
                    st.write("•", challenge)

            else:

                st.write("No challenges detected.")


        else:

            st.warning("Please enter an abstract.")


# -------------------------------
# CONCEPT EXPLANATION
# -------------------------------

elif option == "Concept Explanation":

    st.header("Research Concept Explanation")

    concept = st.text_input(
        "Enter research concept",
        placeholder="Example: Neural Networks"
    )

    if st.button("Explain Concept"):

        if concept.strip():

            with st.spinner("Generating explanation..."):

                explanation = explain_concept(concept)

            st.subheader("Explanation")

            st.write(explanation)

        else:

            st.warning("Please enter a concept.")


# -------------------------------
# CONCEPT VISUALIZATION
# -------------------------------

elif option == "Concept Visualization":

    st.header("Research Concept Visualization")

    abstract = st.text_area(
        "Enter research abstract",
        height=250
    )

    if st.button("Generate Visualization"):

        if abstract.strip():

            with st.spinner("Creating visualization..."):

                image_path = create_concept_visualization(abstract)

            if image_path:

                st.image(
                    image_path,
                    caption="Research Paper Concept Visualization"
                )

            else:

                st.warning("No concepts could be extracted.")

        else:

            st.warning("Please enter an abstract.")