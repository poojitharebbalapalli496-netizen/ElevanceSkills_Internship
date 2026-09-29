# Task 6 – Multilingual AI Assistant

A multilingual customer-service chatbot that supports English, Hindi, Telugu, and Spanish while maintaining conversation context, resolving user intent, handling mixed-language inputs, and generating knowledge-grounded responses.

---

## 1. Objective

The objective of Task 6 is to extend an existing chatbot to support multilingual conversations across at least three additional languages while preserving context, intent, and conversational continuity during language switches.

The assistant is designed to:

* Automatically identify the user's language
* Support multilingual conversations
* Handle mixed-language inputs
* Preserve conversation context
* Resolve user intent across languages
* Normalize multilingual input for intent processing
* Generate knowledge-grounded responses
* Validate responses before translation
* Return responses in the user's detected language

---

## 2. Task Requirement

> Extend the existing chatbot to support multilingual conversations across at least three additional languages while preserving context, intent, and conversational continuity throughout language switches. The assistant should automatically identify language, manage mixed-language inputs within the same conversation, resolve ambiguous queries across languages, and maintain consistent responses regardless of the language used. The solution should demonstrate cross-lingual reasoning, context retention, and intelligent handling of multilingual interactions using open-source models and frameworks.

---

## 3. Problem Statement

Customer-service chatbots are often designed to work with a single language. This can create difficulties when users communicate in different languages or switch languages during the same conversation.

This project addresses this requirement by extending a customer-service chatbot with multilingual language detection, translation, context retention, intent resolution, mixed-language handling, knowledge-grounded responses, and response validation.

The system supports four languages and maintains a common English representation for intent processing and knowledge retrieval.

---

## 4. Key Features

* Multilingual conversation support
* Support for English, Hindi, Telugu, and Spanish
* Automatic language detection
* Mixed-language detection
* Cross-lingual input normalization
* Conversation memory
* Context-aware intent resolution
* Customer-service knowledge base
* Knowledge-grounded responses
* Response validation
* Translation of responses into the user's language
* Streamlit-based interactive interface
* Clear-conversation functionality
* Automated testing using pytest

---

## 5. Supported Languages

The application supports four languages:

| Language | Language Code |
| -------- | ------------- |
| English  | `eng_Latn`    |
| Hindi    | `hin_Deva`    |
| Telugu   | `tel_Telu`    |
| Spanish  | `spa_Latn`    |

Therefore, the project supports three additional languages beyond English: Hindi, Telugu, and Spanish.

---

## 6. System Architecture

The overall processing workflow is:

```text
User Message
     ↓
Language Detection
     ↓
Mixed-Language Detection / Normalization
     ↓
Conversation Memory
     ↓
Intent Resolution
     ↓
Customer-Service Knowledge Base
     ↓
Response Validation
     ↓
Translation to User's Language
     ↓
Final Response
```

The main orchestration is handled by `multilingual_engine.py`.

---

## 7. Technologies Used

### Programming and Interface

* Python
* Streamlit

### Language Processing

* `langdetect`
* `tokenizers`

### Machine Translation

* CTranslate2
* NLLB-200 distilled 600M
* Hugging Face Hub

### Testing

* pytest

All major components are implemented using open-source libraries and models.

---

## 8. Implementation Details

### 8.1 `language_detector.py`

This module is responsible for identifying the language of user input.

It:

* Uses `langdetect`
* Sets `DetectorFactory.seed = 0` for deterministic detection
* Supports English, Hindi, Telugu, and Spanish
* Detects Telugu using Telugu Unicode characters
* Detects Hindi using Devanagari Unicode characters
* Uses English and Spanish marker words to improve short-text detection
* Provides `detect_language()` for primary language detection
* Provides `detect_languages()` for identifying multiple languages
* Provides `is_mixed_language()` for mixed-language detection

---

### 8.2 `translator_ct2.py`

This module provides the multilingual translation functionality.

The final implementation uses:

* CTranslate2 for CPU-based neural machine translation
* NLLB-200 distilled 600M converted to CTranslate2 INT8 format
* Hugging Face Hub for model and tokenizer files
* `tokenizers` for tokenizer processing

The translation model repository used is:

```text
osa911/nllb-200-distilled-600M-ct2-int8
```

The original NLLB tokenizer is obtained from:

```text
facebook/nllb-200-distilled-600M
```

The supported translation language codes are:

```text
English = eng_Latn
Hindi   = hin_Deva
Telugu  = tel_Telu
Spanish = spa_Latn
```

The module supports translation between the four supported languages.

---

### 8.3 `multilingual_engine.py`

`multilingual_engine.py` acts as the main conversation orchestration layer.

It:

1. Detects the user's language
2. Detects mixed-language input
3. Normalizes multilingual input into English for intent resolution
4. Maintains conversation memory
5. Resolves intent using the current message and previous user messages
6. Retrieves information from the customer-service knowledge base
7. Validates the grounded English response
8. Translates the validated response into the user's language
9. Stores assistant responses in conversation memory
10. Handles unsupported or unknown language cases safely

---

### 8.4 `conversation_memory.py`

This module maintains conversation state.

It:

* Stores user and assistant messages
* Stores language information for each message
* Retrieves recent conversation context
* Retrieves the last user message
* Supports context limits
* Allows the conversation to be cleared

This enables the assistant to use previous conversation information when resolving later messages.

---

### 8.5 `intent_resolver.py`

The intent resolver identifies the purpose of a customer-service query.

The currently supported intents are:

* `return`
* `delivery`
* `membership`
* `general`

The resolver uses multilingual keywords and can also use previous conversation context when the current message is ambiguous.

For example, when a follow-up message does not explicitly contain an intent keyword, previous user messages can be considered while resolving the intent.

---

### 8.6 `customer_service.py`

The customer-service knowledge base contains the information used to generate grounded responses.

#### Return

> You can return the product within 30 days of purchase.

#### Delivery

> Standard delivery usually takes 3 to 5 business days. Express delivery is available within 1 to 2 business days.

#### Membership

> Premium members receive free standard shipping on all orders.

#### General

> Could you please provide more details about your question?

The assistant retrieves responses from this knowledge base rather than generating unsupported customer-service information.

---

### 8.7 `response_validator.py`

The response validator checks the grounded response before translation.

It:

* Checks whether the response is non-empty
* Rejects responses that are too short
* Detects failure and error phrases
* Checks whether the response is consistent with the detected intent
* Validates the English grounded response before translation

This provides an additional validation layer before the final response is translated to the user's language.

---

### 8.8 `app.py`

The Streamlit application provides the user interface.

The interface displays:

* Supported languages
* System capabilities
* Detected languages
* Mixed-language status
* Detected intent
* Knowledge source
* Validation status
* English interpretation
* Grounded answer
* Conversation history
* Clear-conversation option

The application supports English, Hindi, Telugu, Spanish, and mixed-language conversations.

---

## 9. Multilingual Translation Approach

The system uses a cross-lingual processing approach.

For a non-English query, the input is normalized into English before intent resolution and knowledge retrieval.

The resulting grounded English response is then translated back into the user's detected language.

```text
User Input
    ↓
Language Detection
    ↓
Cross-Lingual Normalization
    ↓
English Intent Resolution
    ↓
Knowledge Retrieval
    ↓
Response Validation
    ↓
Translation
    ↓
User's Language
```

The final translation pipeline uses:

```text
CTranslate2
      +
NLLB-200 distilled 600M INT8
      +
NLLB tokenizer
      +
Hugging Face Hub
```

---

## 10. Context Retention

Conversation memory is maintained using `conversation_memory.py`.

Each stored message contains:

* Role
* Message text
* Language

The system can retrieve recent messages and the previous user message.

This allows the intent resolver to use previous conversation context when the current message does not explicitly identify an intent.

The conversation can also be cleared from the Streamlit interface.

---

## 11. Mixed-Language Handling

The system can identify when multiple supported languages are present in the same input.

For example:

```text
I want to devolver this product
```

The application identifies:

```text
English
Spanish
Mixed language = Yes
```

The input is normalized for intent processing, allowing the system to identify the `return` intent and retrieve the corresponding customer-service information.

---

## 12. Intent Resolution

The system currently supports four intents:

```text
return
delivery
membership
general
```

Intent resolution uses multilingual keywords.

When the current message is ambiguous or does not directly contain an intent keyword, previous user messages in the conversation context can be considered.

This allows the system to maintain conversational continuity across follow-up messages.

---

## 13. Knowledge-Grounded Responses

Responses are retrieved from the customer-service knowledge base.

The current knowledge base covers:

* Product returns
* Delivery information
* Premium membership shipping benefits
* General clarification

For example, a return query is mapped to the return-policy information:

```text
You can return the product within 30 days of purchase.
```

The response is then validated and translated into the user's language.

---

## 14. Response Validation

Before translation, the grounded English response is passed through the response validator.

The validator checks:

1. Whether the response exists
2. Whether the response is sufficiently long
3. Whether failure/error phrases are present
4. Whether the response is consistent with the detected intent

Only after the grounded response passes validation is it translated into the user's language.

---

## 15. Testing

The project includes an automated pytest test suite.

### Final Automated Test Result

```text
23 passed
0 failed
```

The tests cover:

* Language detection
* Translation
* Intent detection
* Conversation memory and context
* Response validation

The test suite is organized into separate test modules for these areas.

---

## 16. Manual Test Results

The application was also tested through the Streamlit interface.

### Test 1 – English Return Query

**Input:**

```text
I want to return this product
```

**Result:**

The application returned the correct return-policy response.

---

### Test 2 – Hindi Return Query

**Input:**

```text
मैं इस उत्पाद को वापस करना चाहता हूँ।
```

**Result:**

```text
आप खरीद के 30 दिनों के भीतर उत्पाद लौटा सकते हैं।
```

---

### Test 3 – Telugu Return Query

**Input:**

```text
ఈ ఉత్పత్తిని తిరిగి ఇవ్వడానికి ఎంత సమయం ఉంది?
```

**Result:**

```text
మీరు కొనుగోలు చేసిన 30 రోజుల్లోపు ఉత్పత్తిని తిరిగి ఇవ్వవచ్చు.
```

---

### Test 4 – Spanish Return Query

**Input:**

```text
Quiero devolver este producto.
```

**Result:**

```text
Puede devolver el producto dentro de los 30 días siguientes a la compra.
```

---

### Test 5 – Mixed English + Spanish

**Input:**

```text
I want to devolver this product
```

The application detected:

```text
English
Spanish
Mixed language = Yes
Intent = return
Knowledge source = Return Policy
Validation = Passed
```

**English interpretation:**

```text
I want to return this product
```

**Grounded answer:**

```text
You can return the product within 30 days of purchase.
```

---

## 17. Screenshots / Evidence

The `screenshots/` directory contains the following evidence:

* `task6_dashboard.png`
* `task6_english_return.png`
* `task6_hindi_response.png`
* `task6_mixed_language.png`
* `task6_context_language_switch.png`

These screenshots demonstrate the Streamlit interface, multilingual responses, mixed-language handling, and conversation interaction.

---

## 18. Technical Challenge and Solution

During development, the original Torch/Transformers translation approach could not be used reliably in the Windows environment because Windows Device Guard / Application Control blocked the required native Torch and SentencePiece DLLs.

This was an environment compatibility and security constraint rather than a failure of the chatbot implementation.

The final translation pipeline was therefore implemented using:

```text
CTranslate2
+
NLLB-200 distilled 600M INT8
+
tokenizers
+
Hugging Face Hub
```

This allowed the multilingual translation pipeline to run on CPU without depending on the blocked Torch inference path.

---

## 19. Limitations

The current implementation has the following limitations:

* The customer-service knowledge base is intentionally small and focuses on return, delivery, and membership scenarios.
* Translation quality depends on the NLLB-200 model.
* Short or ambiguous text can make automatic language detection less certain.
* The system is designed as an internship demonstration and is not a production customer-service deployment.
* CPU-based translation can be slower than GPU inference.
* Mixed-language handling is implemented for the supported language combinations and is not intended to represent unrestricted multilingual language mixing.

---

## 20. How to Run

### Step 1 – Open the project directory

```cmd
cd /d D:\ElevanceSkills_Internship\Elevance_GitHub\Task6_Multilingual_AI_Assistant
```

### Step 2 – Activate the virtual environment

```cmd
D:\ElevanceSkills_Internship\venv\Scripts\activate
```

### Step 3 – Install dependencies

```cmd
pip install -r requirements.txt
```

### Step 4 – Start the Streamlit application

The Windows environment blocks the Streamlit executable launcher, so the application is started using Python's module execution:

```cmd
python -m streamlit run app.py
```

The Streamlit interface can then be opened in the browser.

---

## 21. Project Structure

```text
Task6_Multilingual_AI_Assistant/
│
├── app.py
├── conversation_memory.py
├── customer_service.py
├── intent_resolver.py
├── language_detector.py
├── multilingual_engine.py
├── requirements.txt
├── response_validator.py
├── translator_ct2.py
│
├── screenshots/
│   ├── task6_dashboard.png
│   ├── task6_english_return.png
│   ├── task6_hindi_response.png
│   ├── task6_mixed_language.png
│   └── task6_context_language_switch.png
│
└── tests/
    ├── conftest.py
    ├── test_language_detection.py
    ├── test_translation.py
    ├── test_intent_detection.py
    ├── test_context.py
    └── test_validation.py
```

---

## 22. Conclusion

Task 6 extends the customer-service chatbot with multilingual conversation capabilities across English, Hindi, Telugu, and Spanish.

The implementation combines language detection, mixed-language handling, cross-lingual normalization, conversation memory, intent resolution, knowledge-grounded responses, response validation, and multilingual translation.

The project was tested using both automated pytest tests and manual Streamlit interactions. The final automated test suite completed with:

```text
23 passed
0 failed
```

The implementation demonstrates the complete development cycle of understanding the multilingual chatbot requirement, implementing the required components, testing the functionality, and documenting the resulting system and its limitations.

---

## 23. GitHub Repository Path

The Task 6 project is maintained as part of the internship repository:

```text
ElevanceSkills_Internship/
└── Task6_Multilingual_AI_Assistant/
```

GitHub repository:

`https://github.com/poojitharebbalapalli496-netizen/ElevanceSkills_Internship`
