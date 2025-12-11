# AI-Ethics-Analytic-Model

## Project Overview

This project aims to evaluate the policies related to Large Language Models (LLMs) developed by OpenAI and Google. We assess whether these policies align with a set of pre-defined Policy Compliance Indicators.
We use a combination of Automated Document Analysis, Manual Sampling Verification, and Background Research to ensure a comprehensive and reliable assessment.

## 🔍 Methodology
1. Automated Document Analysis

The policies of both companies are analyzed using automated text processing, including document chunking, keyword matching, and comparison with predefined indicators.

2. Human Sampling Verification

To ensure the accuracy and consistency of the automated output, we conduct manual sampling to verify the results.

3. Background Research

We perform background research and cross-check policy content with publicly available sources to ensure a thorough and objective evaluation.

## 📁 Project Structure

project/  
│  
├── data/  
│   ├── google_document_scores.csv     
│   ├── google_segmentation.csv      
│   ├── openai_document_scores.csv   
│   └── openai_segmentation.csv     
│  
├── scripts/  
│   ├── add.py                      
│   ├── scraping.py                  
│   ├── visualization_google.ipynb  
│   └── visualization_openai.ipynb   
│  
└── README.md  



## 📚 Reference Materials

For more detailed reference documents, please visit:
https://drive.google.com/drive/u/1/folders/1qAuQaz2P6zvHn1UttUM1K4M5PtElpwmk

## 📊 Outputs

The project outputs include:
The final compliance scores for OpenAI and Google, based on the selected indicators.
Statistical analysis of the policies across various dimensions.
Visualizations showing the differences and overall trends across the policies.
