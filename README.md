# Groq-Powered Qwen AI Agent

A lightweight, terminal-based AI agent leveraging Groq Cloud's ultra-low latency infrastructure and the **Qwen** Large Language Model. This agent features an explicit ReAct (Reasoning and Acting) framework, displaying its step-by-step "thought process" directly in the terminal before executing tools or returning a final answer.

## 🚀 Key Features

*   **Groq Inference Engine**: Maximizes response tokens-per-second using Groq's LPU (Language Processing Unit) architecture.
*   **Qwen Intelligence**: Powered by Qwen's advanced reasoning capabilities for coding, logic, and context management.
*   **Visible Chain-of-Thought**: Displays internal agent reasoning logs (`Thought -> Action -> Observation -> Final Answer`) directly in the console.
*   **Integrated Tool Set**: Equipped with local execution functions including:
    *   🔢 **Calculations**: Safe math evaluation capabilities.
    *   🌐 **Web Scraping**: Real-time extraction of web text data to counter static training data cutoffs.

## 📁 Repository Structure

```text
groq-qwen-agent/
│
├── .env.example            # Placeholder templates for API tokens
├── .gitignore              # Restricts runtime files and local secrets from being committed
├── LICENSE                 # Open-source MIT License
├── README.md               # Documentation and usage guide
├── requirements.txt        # Exact software dependencies
│
└── src/
    ├── __init__.py         # Defines src as an importable module
    ├── main.py             # CLI Entrypoint for interactive chatting
    ├── agent.py            # Primary agent loop managing prompts and states
    ├── tools.py            # Web scraping and calculation functions
    └── config.py           # Validates and loads environment configurations
```

## 🛠️ Installation & Setup

Follow these steps to clone, configure, and execute the agent inside your local VS Code terminal.

### 1. Pre-requisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/groq-qwen-agent.git
cd groq-qwen-agent
```

### 3. Establish a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables
Create a local `.env` file in the root directory by copying the template file:
```bash
cp .env.example .env
```
Open your newly created `.env` file and insert your private Groq credentials:
```env
GROQ_API_KEY=gsk_your_actual_key_here
```

## 🖥️ Usage

Run the main application script from your terminal:
```bash
python src/main.py
```

### 🧠 Terminal Trace Example (Reasoning Loop)

When prompted with a multi-step query, the agent reveals its execution trace sequentially in the terminal layout:

```text
User: Look up the current stock price of Apple (AAPL) and calculate the cost for 15 shares.

[THOUGHT]: The user wants to know the stock price of Apple and calculate a total cost. I need to scrape the live web data for AAPL first.
[ACTION]: web_scrape("https://finance.yahoo.com/quote/AAPL")
[OBSERVATION]: "Apple Inc. (AAPL) Price: \$324.50"

[THOUGHT]: I have retrieved the price (\$324.50). Now I need to multiply this price by 15.
[ACTION]: calculate("324.50 * 15")
[OBSERVATION]: "4867.5"

[THOUGHT]: The calculation is complete. I can now present the final answer to the user.
[FINAL ANSWER]: The current stock price of Apple (AAPL) is \$324.50 per share. The total cost for 15 shares would be \$4,867.50.
```

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
