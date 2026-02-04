# 🚑 MedBot AI - TCCC Assistant



![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)

![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)

![AI](https://img.shields.io/badge/AI-RAG%20System-orange)

![Status](https://img.shields.io/badge/Status-Active-green)



**MedBot** is an AI-powered assistant designed to support military medics and first responders. It utilizes **RAG (Retrieval-Augmented Generation)** technology to provide accurate, protocol-based answers strictly following **TCCC (Tactical Combat Casualty Care)** guidelines.



The system combines the generative power of **Google Gemini 1.5** with a local vector database to ensure answers are grounded in verified medical documents.



---



## 🚀 Key Features



* **RAG Architecture:** Retrives context from a local vector database (ChromaDB) before generating answers, reducing hallucinations.

* **Smart Search:** Uses `intfloat/multilingual-e5-base` embeddings for high-precision semantic search (understands meaning, not just keywords).

* **LLM Integration:** Powered by **Google Gemini 1.5 Flash** for fast and coherent responses.

* **Dockerized:** Fully containerized setup (Bot + API + Database) for easy deployment.

* **Telegram UI:** Accessible interface via Telegram for field usage.



---



## 🛠️ Tech Stack



| Category | Technology |

|----------|------------|

| **Language** | Python 3.11 |

| **Backend API** | FastAPI |

| **Telegram Interface** | Aiogram 3.x |

| **AI Framework** | LangChain |

| **LLM** | Google Gemini API |

| **Vector Database** | ChromaDB |

| **DevOps** | Docker, Docker Compose |



---



## ⚙️ Installation & Setup



### Prerequisites

* Docker & Docker Compose

* Git



### 1. Clone the repository

```bash

git clone https://github.com/romanshypka11-maker/med-bot-with-AI.git
```

### 2. Environment Configuration

* Create a .env file based on the example:

```

cp .env.example .env

```

* Open .env addd fill your credentials

```

GOOGLE_API_KEY=your_google_api_key_here

TELEGRAM_BOT_TOKEN=your_telegram_token_here

SERVER_URL=http://api:8000/ask

```

### Run with Docker(Recommended)

* Launch the entire system with a single command

```

docker-compose up --build

```

*The bot will start and the API will be available at http://localhost:8000.



## 📂 Project Structure

├── bot_telegram.py  = Telegram bot frontend (Aiogram)

├── ingest.py   = Backend API & RAG Logic (FastAPI)

├── Dockerfile  -  Image configuration

├── docker-compose.yml  -  Services orchestration

├── requirements.txt  -   Dependencies

└── embeddings_med -  Pre-computed vector database

## ⚠️ Disclaimer

* Educational Purpose Only. This bot is developed as a pet project for educational purposes. While it uses official TCCC protocols, it should not replace professional medical training or official decision-making in critical situations.



## 👨‍💻 Author

Roman Shypka

* https://github.com/romanshypka11-maker