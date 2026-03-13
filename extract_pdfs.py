import pdfplumber
import json
import os

pdf_files = [
    'documents/policy-1.pdf',
    'documents/policy-2.pdf',
    'documents/policy-3.pdf'
]

results = {}

for pdf_file in pdf_files:
    if not os.path.exists(pdf_file):
        print(f"File not found: {pdf_file}")
        continue
    
    print(f"\n{'='*80}")
    print(f"Extracting: {pdf_file}")
    print('='*80)
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            full_text = ""
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- Page {page_num} ---\n{text}"
            
            results[pdf_file] = full_text
            print(f"Successfully extracted {len(pdf.pages)} pages from {pdf_file}")
            print("\nFirst 1000 characters of extracted text:")
            print(full_text[:1000])
            
    except Exception as e:
        print(f"Error extracting {pdf_file}: {e}")
        results[pdf_file] = f"Error: {e}"

# Save results to a file for analysis
with open('documents/pdf_extractions.txt', 'w', encoding='utf-8') as f:
    for pdf_file, text in results.items():
        f.write(f"\n{'='*80}\n{pdf_file}\n{'='*80}\n\n")
        f.write(text)
        f.write("\n\n")

print("\n" + "="*80)
print("Extraction complete. Results saved to documents/pdf_extractions.txt")
print("="*80)
