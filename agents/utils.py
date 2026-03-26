import pypdf
import os

def parse_pdf(file_path):
    """
    Parses a PDF file and returns the text content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None
        
    return text.strip()

def read_text_file(file_path):
    """
    Reads a text file and returns the content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r") as f:
        return f.read().strip()

def save_text_to_file(text, file_path):
    """
    Saves text to a file.
    """
    with open(file_path, "w") as f:
        f.write(text)
