# Task 4 - Research Expert Chatbot

## Project Overview

The Research Expert Chatbot is an AI-powered application designed to help users explore and understand scientific research papers in the Computer Science domain.

The system uses a subset of the arXiv research paper dataset containing 5,000 Computer Science research papers. It provides paper searching, summarization, information extraction, concept explanation, and concept visualization through an interactive Streamlit interface.

## Objectives

- Search Computer Science research papers using a research topic.
- Retrieve the most relevant papers using TF-IDF and cosine similarity.
- Generate concise summaries of research abstracts.
- Extract important research concepts and evaluation metrics.
- Identify challenges mentioned in research abstracts.
- Explain complex Computer Science concepts using an open-source language model.
- Visualize important concepts from research abstracts.
- Provide an interactive chatbot-style interface using Streamlit.

## Dataset

Dataset: arXiv Scientific Papers

Source:

https://www.kaggle.com/datasets/Cornell-University/arxiv

For this project, 5,000 papers belonging to Computer Science and related Machine Learning categories were extracted from the complete arXiv metadata dataset.

The extracted dataset is stored as:

```text
data/arxiv_cs.jsonl


