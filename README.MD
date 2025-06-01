# 🧠 Multi-Agent AI File Classifier

This system accepts input in **PDF, JSON, or Email (TXT)** format, classifies the **format** and **intent**, and routes it to the appropriate agent. All extracted metadata is logged in a **shared SQLite memory** for chaining and traceability.

---

## 📂 Features

- 📄 Format Detection: PDF / JSON / Email
- 🎯 Intent Classification: Invoice, RFQ, Complaint, Regulation, etc.
- 🔄 Agent Routing:
  - JSON Agent: Schema validation + anomaly flagging
  - Email Agent: Sender, intent, urgency extraction
  - PDF: Routed via classifier
- 🧠 Shared Memory: Logs all metadata + results in SQLite

---

## 🚀 Getting Started

### 1. Clone & Setup

```bash
git clone https://github.com/your-username/multi-agent-classifier
cd multi-agent-classifier
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
