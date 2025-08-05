
import re

def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

def evaluate_f1(gold_answer, predicted_answer):
    gold_tokens = set(tokenize(gold_answer))
    pred_tokens = set(tokenize(predicted_answer))

    tp = len(gold_tokens & pred_tokens)
    precision = tp / len(pred_tokens) if pred_tokens else 0
    recall = tp / len(gold_tokens) if gold_tokens else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return round(precision, 2), round(recall, 2), round(f1, 2)

