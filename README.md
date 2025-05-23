# LangChain GitHub Architecture Agent

This project analyzes the architecture of a public GitHub repository using LangChain and OpenAI's LLM. It generates:
- A PowerPoint presentation describing the architecture
- A PNG architecture diagram based on code analysis

---

## Features
- Summarizes the README and code structure
- Detects AWS components:
  - Lambda, S3, API Gateway
  - ECS, Step Functions, EventBridge, ALB, DynamoDB, etc.
- Automatically generates:
  - A PowerPoint presentation (`.pptx`)
  - An architecture diagram (`.png`)

---

## 🛠Setup

### 1. Clone the project

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

## 2. Install dependencies

pip install -r requirements.txt

## 3. Create a .env file in the root of the project:

OPENAI_API_KEY=your-openai-api-key

## 4. Run the tool

python main.py


## Requirements
-Python 3.10+
-Graphviz must be installed and on your system PATH





