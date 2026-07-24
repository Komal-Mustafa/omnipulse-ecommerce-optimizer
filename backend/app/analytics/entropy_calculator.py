import math
from collections import Counter

def calculate_shannon_entropy(text: str) -> float:
    """
    Calculates the Shannon entropy of a string to measure its structural randomness/vagueness.
    Low entropy indicates repetitive patterns or very short strings.
    High entropy indicates high vocabulary density and length (structured address).
    """
    if not text:
        return 0.0
    
    # Calculate word frequency instead of char frequency for semantic address entropy
    words = text.lower().split()
    total_words = len(words)
    
    if total_words <= 1:
        return 0.0
    
    word_counts = Counter(words)
    entropy = -sum((count / total_words) * math.log2(count / total_words) for count in word_counts.values())
    
    # Normalize by address length to penalize ultra-short text (e.g. "Riyadh near mosque")
    length_penalty = min(1.0, len(text) / 45.0)
    return entropy * length_penalty
