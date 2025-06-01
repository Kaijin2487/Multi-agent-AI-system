import re
from datetime import datetime
from memory.shared_memory import log_entry

class EmailAgent:
    def __init__(self):
        pass

    def process(self, email_text, metadata):

    # Extract sender from header
        sender_match = re.search(r"From:\s*(.*)", email_text, re.IGNORECASE)
        sender = sender_match.group(1).strip() if sender_match else "Unknown"

        # Intent detection
        text_lower = email_text.lower()
        if "invoice" in text_lower:
            intent = "Invoice"
        elif "complaint" in text_lower:
            intent = "Complaint"
        elif "rfq" in text_lower or "request for quotation" in text_lower:
            intent = "RFQ"
        else:
            intent = metadata.get("intent", "Unknown")

        # Urgency detection
        urgency = "Normal"
        if any(word in text_lower for word in ["urgent", "asap", "immediately", "priority"]):
            urgency = "High"

        result = {
            "sender": sender,
            "intent": intent,
            "urgency": urgency,
            "format": metadata.get("format", "Email"),   # ✅ FIXED
            "source": metadata.get("source", ""),
            "timestamp": datetime.utcnow().isoformat()
        }

        log_entry(result)
        return result
