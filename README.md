🧠 Insurance Sales Copilot (GenAI Advisor Assistant)

A Generative AI powered conversational copilot designed to assist insurance advisors with product recommendations, sales pitch support, and intelligent customer interaction workflows.

This project demonstrates enterprise-style LLM application engineering for sales enablement and decision-support automation.

🚀 Overview

Insurance advisors often need quick access to:

Product positioning guidance

Customer goal mapping

Sales pitch personalization

Recommendation filtering

Knowledge retrieval

This system acts as an AI sales companion that helps advisors respond intelligently and confidently during customer conversations.

The copilot leverages:

LLM reasoning

structured goal-based filtering

embeddings-based contextual understanding

configurable prompt templates

✨ Key Capabilities
✅ Conversational Sales Assistance

Understands advisor queries

Provides product insights

Helps craft contextual sales responses

Supports dynamic recommendation workflows

✅ Goal-Based Recommendation Engine

Uses structured logic to:

match customer financial goals

filter relevant insurance products

provide tailored advisory suggestions

✅ Knowledge Grounding using Embeddings

Semantic understanding of sales pitch data

Context-aware information retrieval

Improved response relevance

✅ Prompt-Driven LLM Orchestration

Custom prompt templates enable:

response shaping

advisory tone control

recommendation reasoning

✅ Modular Architecture

System separates:

configuration

recommendation logic

utility processing

application layer

This enables easier experimentation and deployment readiness.

🏗️ System Flow
Advisor Query
     ↓
Application Layer (app.py)
     ↓
LLM Reasoning + Prompt Templates
     ↓
Embedding Context Retrieval
     ↓
Goal-Based Recommendation Filtering
     ↓
Response Generation
     ↓
Advisor-Friendly Output
📂 Project Structure
ABSLI-SALES-COPILOT/

config/
   ├── config.py
   └── prompts.py

embeddings/
   └── (vector / embedding artifacts)

src/
   ├── dependencies.py
   ├── recommend_filter.py
   └── utils.py

ABSLI_Sales_pitch_data.json
ABSLI_Sales_Pitch_Profile_Goals.xlsx

app.py
requirements.txt
test.ipynb
⚙️ Tech Stack
Layer	Technology
LLM	Azure OpenAI / OpenAI
Language	Python
Recommendation Logic	Custom filtering engine
Knowledge Retrieval	Embeddings
Prompt Engineering	Structured templates
Data Sources	JSON + Excel
🧪 Example Use Cases

Suggest suitable insurance products for a customer profile

Assist advisor in explaining policy benefits

Map financial goals to product positioning

Generate contextual sales pitch guidance

▶️ Running the Application
Install Dependencies
pip install -r requirements.txt
Run Copilot
python app.py
🚀 Future Enhancements

Streamlit / Web UI integration

Conversation memory management

Multi-product comparison reasoning

Voice-enabled advisory assistant

CRM integration

👨‍💻 Author

Keshav Rathore
GenAI Engineer | Data Scientist | Azure | Databricks | LLM Systems
