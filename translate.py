# translate.py
# (Program description: Japanese -> English translation pipeline 
#  using Hugging Face MarianMT model with Hallucination Filter)

from transformers import MarianMTModel, MarianTokenizer

# 1. Model Configuration (Model & Tokenizer Load)
# Load as global variables to avoid reloading overhead on every function call.
MODEL_NAME = "Helsinki-NLP/opus-mt-ja-en"

print(f"Loading translation model: {MODEL_NAME}...")
try:
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)
    print("✅ Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit()

# 2. Noise Filter List
# Filters out subtitle tags/artifacts (hallucinations) that the AI sometimes 
# outputs instead of a translation (common in models trained on subtitles).
NOISE_WORDS = [
    "(Laughter)", "(Applause)", "(Music)", "(Cheering)", 
    "(Video)", "(Audio)", "(Silence)", "(laughter)", "(applause)"
]

def translate_japanese_to_english(text_to_translate):
    """
    Translate Japanese text to English.
    Includes a filter for AI hallucinations (e.g., "(Laughter)").
    
    Args:
        text_to_translate (str): The Japanese sentence to translate.
        
    Returns:
        str: The translated English sentence or an error message.
    """
    
    # Check for empty input
    if not text_to_translate or not text_to_translate.strip():
        return ""

    try:
        # (Translation pipeline)
        
        # 1. Tokenization 
        # (Added `truncation=True` to prevent errors with overly long sequences)
        tokenized_text = tokenizer(text_to_translate, return_tensors="pt", padding=True, truncation=True)
        
        # 2. Inference (Generate translation)
        translated_tokens = model.generate(**tokenized_text)
        
        # 3. Decoding (Convert tokens back to text)
        translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        
        # --- [Noise Filtering Logic] ---
        clean_result = translation.strip()
        
        # Case 1: If the result is ONLY a noise word (e.g., "(Laughter)")
        # Treat it as a failure and return the context error with original text.
        if clean_result in NOISE_WORDS:
            return f"[Context Error] {text_to_translate}"
            
        # Case 2: If noise is mixed within a valid sentence -> Remove the noise.
        for noise in NOISE_WORDS:
            clean_result = clean_result.replace(noise, "")
            
        return clean_result.strip()

    except Exception as e:
        print(f"Translation logic error: {e}")
        return "[Translation Failed]"

# --- Test Block ---
if __name__ == "__main__":
    test_sentences = [
        "私は学生です。",
        "忘れるべきことを忘れることができない者にとって、忘れることは病気ではない。",
        "そして、前世の記憶が蘇った日", # Test sentence that caused errors previously
    ]
    
    print("--- Translation Test Start ---")
    for sent in test_sentences:
        print(f"JP: {sent}")
        result = translate_japanese_to_english(sent)
        print(f"EN: {result}")
        print("-" * 20)
    print("--- Translation Test End ---")