import os
import pdfplumber
import pandas as pd

current_directory = os.getcwd()
print("Current directory:", current_directory)

folder_path = "google_document/"  # 修改为你的文件夹路径
output_csv = 'google_segmentation.csv'

pdf_texts = []

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        
        with pdfplumber.open(file_path) as pdf:
            paragraphs = []
            for page_num in range(len(pdf.pages)):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                page_paragraphs = text.split('\n\n')  
                paragraphs.extend(page_paragraphs)
            
            for i in range(0, len(paragraphs), 10):
                text_block = '\n\n'.join(paragraphs[i:i+10])  
                text_block = f'"{text_block.strip()}"'
                pdf_texts.append([filename, text_block])

df = pd.DataFrame(pdf_texts, columns=["FileName", "TextBlock"])
df.to_csv(output_csv, index=False, encoding='utf-8')

print(f"Text from PDF files has been saved to {output_csv}")
