import json
from pydantic import BaseModel, ValidationError, Field
from datetime import datetime
from memory.shared_memory import log_entry

class InvoiceSchema(BaseModel):
    invoice_id: str
    date: str
    amount: float
    vendor: str
    items: list

class JSONAgent:
    def __init__(self):
        pass

    def process(self, json_path, metadata):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return {"error": f"Failed to read JSON: {e}"}

        try:
            validated = InvoiceSchema(**data)
            status = "Valid"
        except ValidationError as ve:
            validated = None
            status = "Invalid"
            error_detail = ve.errors()

        result = {
            "status": status,
            "format": metadata.get("format", "JSON"),   # add format here explicitly
            "source": metadata.get("source", ""),
            "intent": metadata.get("intent", "Unknown"),
            "timestamp": datetime.utcnow().isoformat()
        }


        if validated:
            result["validated_data"] = validated.dict()
        else:
            result["errors"] = error_detail

        log_entry(result)
        return result
