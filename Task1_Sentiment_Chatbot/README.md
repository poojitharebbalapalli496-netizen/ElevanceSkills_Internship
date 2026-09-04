# Task 1 - Sentiment Analysis Customer Service Chatbot

## Objective

The objective of this task is to integrate sentiment analysis into a customer service chatbot so that it can identify the sentiment expressed in a user's message and provide an appropriate customer-service response.

## Problem Statement

Customer messages can express positive, negative, or neutral sentiment. The chatbot analyzes these messages and generates a suitable response based on the detected sentiment.

The system also handles low-confidence predictions by marking them as uncertain instead of blindly accepting the model's prediction.

## Technologies Used

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- CardiffNLP Twitter-RoBERTa sentiment model
- Pytest

## Model Used

The application uses the pretrained:

`cardiffnlp/twitter-roberta-base-sentiment-latest`

sentiment-analysis model through the Hugging Face Transformers pipeline.

## Implementation

The application is organized into separate functions for:

- Loading the sentiment model
- Analyzing user messages
- Generating customer-service responses

The sentiment model is loaded using Streamlit's `@st.cache_resource` so that the model does not need to be unnecessarily reloaded during Streamlit reruns.

A confidence threshold of 60% is used. Predictions below this threshold are classified as **Uncertain**, allowing the chatbot to request more information from the user.

The application also includes exception handling to prevent unexpected model errors from crashing the user interface.

## Sentiment Categories

The chatbot handles:

- Positive
- Negative
- Neutral
- Uncertain

## Working Process

1. The user enters a customer message.
2. The message is passed to the sentiment-analysis model.
3. The model predicts the sentiment and confidence score.
4. The confidence score is compared with the 60% threshold.
5. Low-confidence predictions are classified as Uncertain.
6. The detected sentiment and confidence are displayed.
7. A suitable customer-service response is generated.

## Customer-Service Responses

### Positive

The chatbot thanks the customer and acknowledges their satisfaction.

### Negative

The chatbot apologizes for the customer's experience and offers assistance.

### Neutral

The chatbot asks how it can assist the customer further.

### Uncertain

The chatbot asks the customer to provide additional details when the model confidence is low.

## Testing

Automated tests were implemented using Pytest to verify the chatbot response logic and confidence-threshold behavior.

### Automated Test Results

The application passed all 5 automated tests:

- Positive response test
- Negative response test
- Neutral response test
- Uncertain response test
- Confidence threshold test

**Result: 5/5 tests passed**

The Streamlit application was also tested manually with positive, negative, and neutral customer messages.

## Example Test Cases

### Positive Test

Input:

`I am very happy with your service!`

Expected sentiment:

`Positive`

### Negative Test

Input:

`I am extremely disappointed with your service.`

Expected sentiment:

`Negative`

### Neutral Test

Input:

`I want to know about my order.`

Expected sentiment:

`Neutral`

## Results

The chatbot successfully:

- Detects customer sentiment
- Displays model confidence
- Generates sentiment-based customer-service responses
- Handles low-confidence predictions
- Uses cached model loading
- Handles prediction errors gracefully
- Passes automated response-logic tests

## Challenges and Solutions

### Model Reloading

Repeated Streamlit interactions could cause unnecessary model loading.

**Solution:** Streamlit's `@st.cache_resource` is used to cache the sentiment-analysis model.

### Low-Confidence Predictions

A model prediction should not always be treated as completely reliable.

**Solution:** A 60% confidence threshold is used. Predictions below the threshold are handled as Uncertain.

### Error Handling

Model inference may occasionally fail because of unexpected input or runtime issues.

**Solution:** Prediction is wrapped in exception handling and an error message is displayed to the user.

## Future Improvements

Future versions could include:

- Conversation history
- Personalized customer responses
- Multilingual sentiment analysis
- More detailed emotion categories
- Integration with customer-support databases
- Conversation context and memory

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt