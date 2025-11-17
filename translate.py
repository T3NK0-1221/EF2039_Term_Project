# translate.py
# (Program description: Using Hugging Face MarianMT model 
#  Ja -> En translation

# 1. Import necessary library
from transformers import MarianMTModel, MarianTokenizer

# (Declare model, model and tokenizer load)
# 'Helsinki-NLP/opus-mt-ja-en': Pre-trained model / ja -> en
try:
    print("Loading model and tokenizer...")
    MODEL_NAME = "Helsinki-NLP/opus-mt-ja-en"
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

def translate_japanese_to_english(text_to_translate):
    """
    Translate Japanese text to English

    Args:
        text_to_translate (str): japanese sentence

    Returns:
        str: translated english sentence
    """
    
    # (Translation pipeline)
    # 1. 텍스트를 모델이 이해할 수 있는 숫자(토큰)로 변환 (토크나이징)
    #    return_tensors="pt"는 PyTorch 텐서(데이터 묶음)로 반환하라는 의미입니다.
    tokenized_text = tokenizer(text_to_translate, return_tensors="pt", padding=True)
    
    # 2. 모델을 사용해 번역된 토큰 생성 (추론)
    translated_tokens = model.generate(**tokenized_text)
    
    # 3. 번역된 숫자(토큰)를 다시 사람이 읽을 수 있는 텍스트로 변환 (디코딩)
    translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    
    return translation

# --- test ---
if __name__ == "__main__":
    # Example
    test_sentence_1 = "私は学生です。"
    test_sentence_2 = "忘れるべきことを忘れることができない者にとって、忘れることは病気ではない。"
    
    print("--- Translation Test Start ---")
    
    # Test 1
    translated_1 = translate_japanese_to_english(test_sentence_1)
    print(f"Original (ja): {test_sentence_1}")
    print(f"Translated (en): {translated_1}")
    print("-" * 20)
    
    # Test 2
    translated_2 = translate_japanese_to_english(test_sentence_2)
    print(f"Original (ja): {test_sentence_2}")
    print(f"Translated (en): {translated_2}")
    
    print("--- Translation Test End ---")