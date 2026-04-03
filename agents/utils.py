import pypdf
import os
import json

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

def parse_agent_output(result, model_class):
    """
    Parses CrewAI result into a specific Pydantic model.
    Handles pydantic, json_dict, and raw string fallback.
    """
    # Try pydantic first (works with OpenAI native)
    if hasattr(result, 'pydantic') and result.pydantic:
        return result.pydantic
    
    # Try json_dict (works with some providers)
    if hasattr(result, 'json_dict') and result.json_dict:
        return model_class(**result.json_dict)
    
    # Fallback: parse the raw string output as JSON
    raw = str(result.raw) if hasattr(result, 'raw') else str(result)
    # Find JSON in the output (might be wrapped in markdown code blocks)
    raw = raw.strip()
    if raw.startswith("```"):
        # Remove markdown wrapper
        lines = raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    
    # Final cleanup for any potential prefix/suffix garbage before/after JSON
    try:
        return model_class(**json.loads(raw))
    except json.JSONDecodeError:
        # If it still fails, try to find the first '{' and last '}'
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start != -1 and end != 0:
            return model_class(**json.loads(raw[start:end]))
        raise
