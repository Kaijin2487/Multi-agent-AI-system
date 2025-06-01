from agents.classifier_agent import ClassifierAgent
from agents.email_agent import EmailAgent
from agents.json_agent import JSONAgent
from memory.shared_memory import get_all_logs

def main():
    input_path = "data/sample_invoice.pdf"  # Change to sample_email.txt or sample_document.pdf to test

    classifier = ClassifierAgent()
    classification = classifier.classify(input_path)

    # ✅ Handle any errors or unexpected outputs
    if not classification or "format" not in classification:
        print("❌ Error during classification:")
        print(classification.get("error", "Unknown error"))
        return

    result = None
    format_type = classification["format"]

    if format_type == "Email":
        with open(input_path, "r", encoding="utf-8") as f:
            email_text = f.read()

        email_agent = EmailAgent()
        result = email_agent.process(email_text, classification)
        print("=== Email Agent Output ===")
        print(result)

    elif format_type == "JSON":
        json_agent = JSONAgent()
        result = json_agent.process(input_path, classification)
        print("=== JSON Agent Output ===")
        print(result)

    elif format_type == "PDF":
        print("=== PDF File Detected ===")
        print("Intent:", classification.get("intent", "Unknown"))
        print("Content excerpt:", classification.get("content_excerpt", "")[:300])
        print("📌 PDF routing not yet implemented.")

    else:
        print("⚠️ Unknown format:", format_type)

    print("\n=== Shared Memory Logs ===")
    for log in get_all_logs():
        print(log)

if __name__ == "__main__":
    main()
