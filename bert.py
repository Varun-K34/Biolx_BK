from transformers import pipeline, BertForTokenClassification, BertTokenizerFast
import pandas as pd


# Local file paths to the downloaded model files
model_path = "C:\\Users\\appuv\\backend2"
tokenizer_path = "C:\\Users\\appuv\\backend2\\tokenizer"

# Load tokenizer and model from local files
tokenizer = BertTokenizerFast.from_pretrained(tokenizer_path)
model = BertForTokenClassification.from_pretrained(model_path)

# Example biomedical text
text = "The role of the p53 gene in cancer has been extensively studied. Mutations in the p53 gene are commonly associated with various types of cancer, including breast cancer, lung cancer, and colorectal cancer. Understanding the mechanisms underlying p53 mutations and their implications for cancer development is crucial for the development of targeted therapies."

# Define NER pipeline
ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy='first')

# Perform NER
results = ner(text)

# Convert results to DataFrame for better visualization
df_results = pd.DataFrame.from_records(results)

# Print the DataFrame containing recognized entities
print(df_results)
