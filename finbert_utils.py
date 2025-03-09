# cited from https://www.youtube.com/watch?v=c9OjEThuJjY

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 

device = "cuda:0" if torch.cuda.is_available() else "cpu"

# load model once and reuse it (prevents redundant memory usage)
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news):
    if not news:
        print("WARNING: No news data received. Defaulting to neutral.")
        return 0, "neutral"  # prevents crashes

    tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

    # prevents memory overload
    with torch.no_grad():
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)

    probability = result[torch.argmax(result)]
    sentiment = labels[torch.argmax(result)]
    
    return probability, sentiment


if __name__ == "__main__":
    tensor, sentiment = estimate_sentiment(['markets responded negatively to the news!', 'traders were displeased!'])
    print(tensor, sentiment)
    print(torch.cuda.is_available())
