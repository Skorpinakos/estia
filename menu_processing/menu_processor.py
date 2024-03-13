import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the provided PDF
    doc = fitz.open(pdf_path)
    
    # Initialize an empty list to store the text of each page
    text_per_page = []
    
    # Iterate through each page in the PDF
    for page in doc:
        # Extract text from the page
        text = page.get_text()
        # Append the text to our list, one string per page
        text_per_page.append(text)
        
    # Close the PDF after processing
    doc.close()
    
    # Return the list of text strings
    return text_per_page

# Example usage
pdf_path = 'menu_processing/monthly_menu.pdf'
text_per_page = extract_text_from_pdf(pdf_path)
print(text_per_page[0])
