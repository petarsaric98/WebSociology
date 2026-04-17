import zipfile
import xml.etree.ElementTree as ET
import os
import glob

def extract_text_from_docx():
    # Use glob to find the file despite encoding issues in terminal
    pattern = 'Istra*ivanjeGlazba.docx'
    found_files = glob.glob(pattern)
    if not found_files:
        # try lowercase or other patterns
        found_files = glob.glob('*.docx')
    
    if not found_files:
        return "No .docx files found."
    
    docx_path = found_files[0]
    print(f"Extracting from: {docx_path}")
    
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            xml_content = zip_ref.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            # Namespaces
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            text_elements = tree.findall('.//w:t', ns)
            # Combine text with spaces, but keep some structure if possible
            # Actually, let's just extract all text and we can parse it
            text = " ".join([node.text for node in text_elements if node.text])
            return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    content = extract_text_from_docx()
    # Save content to a text file for easier manual inspection
    with open('extracted_content.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Extracted content saved to extracted_content.txt")
    print("Content preview (first 500 chars):")
    print(content[:500])
