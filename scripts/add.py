import os
import pdfplumber
import pandas as pd

current_directory = os.getcwd()
print("Current directory:", current_directory)

folder_path = "google_document/"  # 修改为你的文件夹路径
output_csv = 'google_segmentation.csv'

if os.path.exists(output_csv):
    df = pd.read_csv(output_csv)
else:
    columns = ["FileName", "TextBlock"] + [f'l{i}' for i in range(1, 30)]
    df = pd.DataFrame(columns=columns)

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

                if not any(df["TextBlock"] == text_block):
                    pdf_texts.append([filename, text_block] + [None]*29)  

if pdf_texts:
    new_df = pd.DataFrame(pdf_texts, columns=["FileName", "TextBlock"] + [f'l{i}' for i in range(1, 30)])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(output_csv, index=False, encoding='utf-8')

print(f"Text from PDF files has been added to {output_csv}")
