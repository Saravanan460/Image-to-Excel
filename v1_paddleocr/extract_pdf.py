import fitz

def extract_pdf():
    doc = fitz.open('Index-cards-project-Instructions-LVeronneau.pdf')
    with open('pdf_text.txt', 'w', encoding='utf-8') as f:
        f.write('\n---PAGE---\n'.join([page.get_text() for page in doc]))

if __name__ == "__main__":
    extract_pdf()
