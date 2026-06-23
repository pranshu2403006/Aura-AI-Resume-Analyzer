def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    import pdfplumber

    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    
    return text.strip()
