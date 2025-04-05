import pandas as pd
from evaluate import load 
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Read the generated summary dataset
file_path = "summaries_dataset_bart.xlsx"  
data = pd.read_excel(file_path)

# Ensure column presence
if "review_full" not in data.columns or "summary" not in data.columns:
    raise ValueError("The dataset must contain 'review_full' (reference summary) and 'summary' (generated summary) columns")

# Taking out reference summaries and generating summaries
references = data["review_full"].astype(str).tolist()  # True Abstracts
predictions = data["summary"].astype(str).tolist()  # Generate a summary

# Loading ROUGE assessment indicators
rouge = load("rouge")

# Calculating the ROUGE score
rouge_scores = rouge.compute(predictions=predictions, references=references)

# Print ROUGE results
print("\nROUGE Scores:")
for key, value in rouge_scores.items():
    print(f"{key}: {value:.4f}")



# Define the BLEU score calculation function
def calculate_bleu(references, predictions):
    smoothie = SmoothingFunction().method4  # Smooth function to prevent 0-gram miscalculations
    bleu1 = sum([sentence_bleu([ref.split()], pred.split(), weights=(1, 0, 0, 0), smoothing_function=smoothie) for ref, pred in zip(references, predictions)]) / len(references)
    bleu2 = sum([sentence_bleu([ref.split()], pred.split(), weights=(0.5, 0.5, 0, 0), smoothing_function=smoothie) for ref, pred in zip(references, predictions)]) / len(references)
    bleu3 = sum([sentence_bleu([ref.split()], pred.split(), weights=(0.33, 0.33, 0.33, 0), smoothing_function=smoothie) for ref, pred in zip(references, predictions)]) / len(references)
    bleu4 = sum([sentence_bleu([ref.split()], pred.split(), weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothie) for ref, pred in zip(references, predictions)]) / len(references)
    
    return {"BLEU-1": bleu1, "BLEU-2": bleu2, "BLEU-3": bleu3, "BLEU-4": bleu4}

# Calculating the BLEU score
bleu_scores = calculate_bleu(references, predictions)

# Print BLEU results
print("\nBLEU Scores:")
for key, value in bleu_scores.items():
    print(f"{key}: {value:.4f}")
