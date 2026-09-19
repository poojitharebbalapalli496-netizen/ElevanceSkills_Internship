\# Task 5 - Multimodal AI Assistant



\## Overview



This project implements a multimodal AI assistant capable of understanding and reasoning over image and text inputs.



The assistant combines image classification, image captioning, structured evidence extraction, conversational memory, intent detection, reasoning, and response validation.



The system is designed to provide evidence-based responses and communicate uncertainty when the available visual evidence is insufficient.



\## Task Objective



The assistant is designed to:



\* Understand image and text inputs

\* Analyze visual content

\* Extract relevant visual evidence

\* Maintain conversational context across multiple interactions

\* Handle contextual references such as "it", "that device", and "this laptop"

\* Detect the user's question intent

\* Reason using available visual evidence

\* Handle ambiguity and insufficient evidence

\* Validate responses before displaying them

\* Avoid unsupported claims and direct unverified model output



\## System Architecture



```text

Image Input

&#x20;   |

&#x20;   v

Image Analyzer

&#x20;   |

&#x20;   +--> MobileNet V3 Small

&#x20;   |       |

&#x20;   |       +--> Top-5 visual classifications

&#x20;   |

&#x20;   +--> BLIP Image Captioning

&#x20;           |

&#x20;           +--> Image caption

&#x20;   |

&#x20;   v

Evidence Extraction

&#x20;   |

&#x20;   v

Conversation Memory + Context

&#x20;   |

&#x20;   v

Intent Detection

&#x20;   |

&#x20;   v

Reasoning Engine

&#x20;   |

&#x20;   v

Response Validator

&#x20;   |

&#x20;   v

Final Evidence-Based Response

```



\## Main Components



\### 1. Image Analyzer



\*\*File:\*\* `image\_analyzer.py`



The image analyzer uses:



\* MobileNet V3 Small for image classification

\* Salesforce BLIP image captioning model for generating visual descriptions



The analyzer returns:



\* Image caption

\* Top-5 classifications

\* Confidence scores

\* Primary classification



\### 2. Evidence Extraction



\*\*File:\*\* `evidence.py`



The evidence extraction layer converts image-analysis results into structured evidence.



It stores:



\* Primary visual label

\* Primary confidence

\* Top visual labels

\* Image caption

\* Whether the primary classification meets the configured confidence threshold



The visual confidence threshold is configured as `0.50`.



\### 3. Conversation Memory



\*\*File:\*\* `conversation.py`



The conversation memory component maintains structured conversation state.



It stores:



\* User questions

\* Assistant responses

\* Image identifiers

\* Visual evidence

\* Detected intent

\* Unresolved ambiguities



The conversation history is limited to the configured maximum number of turns.



\### 4. Reasoning Engine



\*\*File:\*\* `reasoning.py`



The reasoning engine:



\* Detects question intent

\* Resolves contextual references

\* Uses previous conversation evidence

\* Checks available visual evidence

\* Handles ambiguous questions

\* Avoids unsupported claims

\* Produces cautious responses when evidence is insufficient



Supported intent categories include:



\* Visual identification

\* Brand identification

\* Model identification

\* Technical specification

\* Operating system

\* General visual questions



\### 5. Response Validator



\*\*File:\*\* `validator.py`



The response validator checks whether the reasoning result is appropriately supported by the available visual evidence.



Validation states include:



\* \*\*PASS\*\* - The response is supported by the available evidence.

\* \*\*WARN\*\* - The response correctly communicates uncertainty or insufficient evidence.

\* \*\*FAIL\*\* - The response contains an unsupported claim.



\## Streamlit Application



\*\*File:\*\* `app.py`



The project provides an interactive Streamlit interface with:



\* Image upload

\* Image analysis

\* Chat-style interaction

\* Conversation history

\* Evidence information

\* Classification confidence

\* Reasoning information

\* Response validation status

\* Example questions

\* Clear conversation functionality

\* Error handling



\## Example Questions



The assistant can handle questions such as:



```text

What is shown in the image?



What about that device?



Is this definitely an HP laptop?



What is the exact model?



How much RAM does it have?



What operating system does it use?

```



The assistant is designed not to invent technical specifications, exact models, or brands when the available image evidence is insufficient.



\## Evidence-Based Reasoning



A key design principle of this project is that raw model output is not directly treated as verified information.



For example, when an image classifier identifies an object with sufficient confidence, that evidence can be used for visual identification.



However, questions about exact RAM, processor, storage, brand, or model may not be answerable from the available image.



In such cases, the system communicates the limitation instead of guessing.



\## Testing



The project uses `pytest` for automated testing.



Test files:



```text

test\_conversation.py

test\_evidence.py

test\_image\_analyzer.py

test\_reasoning.py

test\_validator.py

```



The complete test suite contains \*\*27 automated tests\*\*.



Latest test result:



```text

27 passed in 73.18s

```



The tests cover:



\* Conversation history

\* Conversation history limits

\* Reference resolution

\* Previous evidence retrieval

\* Evidence extraction

\* Confidence threshold handling

\* Empty evidence

\* Image analyzer output

\* Visual identification

\* Follow-up references

\* Ambiguity handling

\* Brand identification limitations

\* Model identification limitations

\* Technical specification limitations

\* Operating system reasoning

\* Low-confidence reasoning

\* Response validation

\* Unsupported claim detection

\* Missing reasoning results

\* Missing visual evidence



\## Project Structure



```text

Task5\_Multimodal\_AI\_Assistant/

│

├── app.py

├── config.py

├── conversation.py

├── evidence.py

├── image\_analyzer.py

├── reasoning.py

├── validator.py

│

├── test\_conversation.py

├── test\_evidence.py

├── test\_image\_analyzer.py

├── test\_reasoning.py
├── test\_validator.py
│
├── test_image.png
├── requirements.txt
├── .gitignore
└── screenshots/
    ├── task5_visual_identification.png
    ├── task5_contextual_followup.png
    ├── task5_technical_specification.png
    ├── task5_brand_reasoning.png
    ├── task5_model_reasoning.png
    └── task5_low_confidence_handling.png
```



\## Installation



Create and activate a Python virtual environment and install the required dependencies:



```bash

pip install -r requirements.txt

```



\## Run the Application



From the Task 5 directory:



```bash

streamlit run app.py

```



The Streamlit application will open in the browser.



\## Run Tests



Run the complete test suite using:



```bash

pytest -v

```



Expected result:



```text

27 passed

```



\## Models Used



\### MobileNet V3 Small



Used for image classification and generating the top-5 visual predictions.



\### Salesforce BLIP Image Captioning



Used to generate an image caption that provides additional visual context.



Model-generated captions are treated as supporting evidence rather than guaranteed facts.



\## Limitations



The system reasons conservatively from available visual evidence.



It cannot reliably determine information that is not visible or sufficiently supported by the image, including:



\* Exact device model

\* RAM capacity

\* Processor specifications

\* Storage capacity

\* Confirmed brand when the logo is unclear

\* Exact operating system version



When evidence is insufficient, the assistant communicates uncertainty instead of fabricating information.



\## Quality and Validation



The project includes automated unit testing and manual Streamlit testing.



The latest automated test run passed:



```text

27/27 tests

```



Manual testing covered:



\* Normal visual identification

\* Follow-up questions

\* Contextual references

\* Brand uncertainty

\* Model uncertainty

\* Technical specification uncertainty

\* Low-confidence image handling

\* Conversation clearing

\* Image switching

\* Response validation



