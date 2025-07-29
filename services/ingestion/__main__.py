from services.ingestion.main import main

if __name__ == "__main__":
    event = {"bucket": "auditoria-folha-input-pdfs", "name": "exemplo.pdf"}
    context = None
    main(event, context)
