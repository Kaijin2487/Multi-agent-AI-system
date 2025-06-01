import filetype
import os
import fitz  # PyMuPDF

from agents.email_agent import EmailAgent
from agents.json_agent import JSONAgent
from memory.shared_memory import log_entry

class ClassifierAgent:
    def __init__(self):
        self.email_agent = EmailAgent()
        self.json_agent = JSONAgent()

    def detect_format(self, path):
        if path.endswith(".json"):
            return "JSON"
        elif path.endswith(".txt"):
            return "Email"
        else:
            kind = filetype.guess(path)
            if kind and kind.mime == "application/pdf":
                return "PDF"
            return "Unknown"

    def detect_intent(self, content):
        content_lower = content.lower()
        if "invoice" in content_lower:
            return "Invoice"
        elif "quote" in content_lower or "rfq" in content_lower:
            return "RFQ"
        elif "complaint" in content_lower:
            return "Complaint"
        elif "regulation" in content_lower:
            return "Regulation"
        return "Unknown"

    def read_pdf(self, path):
        try:
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            return f"ERROR: {e}"

    def classify(self, input_path: str):
        try:
            if input_path.endswith(".json"):
                file_format = "JSON"
                with open(input_path, "r", encoding="utf-8") as f:
                    content = f.read()

            elif input_path.endswith(".txt"):
                file_format = "Email"
                with open(input_path, "r", encoding="utf-8") as f:
                    content = f.read()

            elif input_path.endswith(".pdf"):
                file_format = "PDF"
                with fitz.open(input_path) as doc:
                    content = "\n".join([page.get_text() for page in doc])

            else:
                raise ValueError("Unsupported file format")

            print(f"[DEBUG] Detected format: {file_format}")
            print(f"[DEBUG] Content length: {len(content)}")

            # Heuristic intent detection
            content_lower = content.lower()
            if "invoice" in content_lower:
                intent = "Invoice"
            elif "rfq" in content_lower or "request for quotation" in content_lower:
                intent = "RFQ"
            elif "complaint" in content_lower:
                intent = "Complaint"
            elif "regulation" in content_lower:
                intent = "Regulation"
            else:
                intent = "Unknown"

            print(f"[DEBUG] Detected intent: {intent}")

            result = {
                "format": file_format,
                "intent": intent,
                "source": input_path
            }

            log_entry(result)
            return result

        except Exception as e:
            print("❌ Error during classification:")
            print(e)
            return {}