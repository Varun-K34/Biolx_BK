from transformers import pipeline, BertForTokenClassification, BertTokenizerFast
import pandas as pd


# Local file paths to the downloaded model files
model_path = "C:\\Users\\appuv\\backend2"
tokenizer_path = "C:\\Users\\appuv\\backend2\\tokenizer"

# Load tokenizer and model from local files
tokenizer = BertTokenizerFast.from_pretrained(tokenizer_path)
model = BertForTokenClassification.from_pretrained(model_path)

# Example biomedical text
text = """
Influenza, commonly known as "the flu" or just "flu", is an infectious disease caused by influenza viruses. Symptoms range from mild to severe and often include fever, runny nose, sore throat, muscle pain, headache, coughing, and fatigue. These symptoms begin one to four (typically two) days after exposure to the virus and last for about two to eight days. Diarrhea and vomiting can occur, particularly in children. Influenza may progress to pneumonia from the virus or a subsequent bacterial infection. Other complications include acute respiratory distress syndrome, meningitis, encephalitis, and worsening of pre-existing health problems such as asthma and cardiovascular disease.

There are four types of influenza virus: A, B, C, and D. Aquatic birds are the primary source of Influenza A virus (IAV), which is also widespread in various mammals, including humans and pigs. Influenza B virus (IBV) and influenza C virus (ICV) primarily infect humans, and influenza D virus (IDV) is found in cattle and pigs. IAV and IBV circulate in humans and cause seasonal epidemics, and ICV causes a mild infection, primarily in children. IDV can infect humans but is not known to cause illness. In humans, influenza viruses are primarily transmitted through respiratory droplets from coughing and sneezing. Transmission through aerosols and surfaces contaminated by the virus also occur.

Frequent hand washing and covering one's mouth and nose when coughing and sneezing reduce transmission. Annual vaccination can help to provide protection against influenza. Influenza viruses, particularly IAV, evolve quickly, so flu vaccines are updated regularly to match which influenza strains are in circulation. Vaccines provide protection against IAV subtypes H1N1 and H3N2 and one or two IBV subtypes. Influenza infection is diagnosed with laboratory methods such as antibody or antigen tests and a polymerase chain reaction (PCR) to identify viral nucleic acid. The disease can be treated with supportive measures and, in severe cases, with antiviral drugs such as oseltamivir. In healthy individuals, influenza is typically self-limiting and rarely fatal, but it can be deadly in high-risk groups.


"""
# Define NER pipeline
ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy='first')

# Perform NER
results = ner(text)

# Convert results to DataFrame for better visualization
df_results = pd.DataFrame.from_records(results)

# Print the DataFrame containing recognized entities
print(df_results)
