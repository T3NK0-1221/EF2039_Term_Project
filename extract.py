# extract.py 
# (GiNZA(spaCy) model: extract meaningful kanji(noun, verb))

import spacy
import re 

# (1. Load GiNZA AI model)
MODEL_NAME = "ja_ginza"
try:
    print(f"Loading GiNZA model ({MODEL_NAME})...")
    nlp = spacy.load(MODEL_NAME)
    print("Model loaded successfully.")
except OSError:
    # (OSError: Can not find model)
    print(f"Error: Could not find model '{MODEL_NAME}'.")
    print("Please make sure 'ginza' is installed correctly via 'pip install ginza'")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()


# (2. Finding Kanji in the sentence)
# CJK Unified Ideographs (Chinese/Japanese/Korean Kanji)
KANJI_REGEX = re.compile(r'[\u4e00-\u9faf]')

def extract_kanji_words(text_to_extract):
    """
    GiNZA model extrat the 'lemma' of kanji that includes mean.

    Args:
        text_to_extract (str): Japanese sentence

    Returns:
        list: Kanji list
    """
    
    # (3. Analyze text with AI model)
    doc = nlp(text_to_extract)
    
    # Automatically eradicate duplication words ; set()
    kanji_words_set = set()
    
    # (4. 분석된 토큰(token)들을 순회)
    for token in doc:
        # 4-1. Check the quality of words Anki card로 만들지 결정 (nouns, proper nouns, verbs, adjectives)
        is_meaningful_pos = token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ']
        
        # 4-2. Check that the text of the word contains at least one Chinese character
        has_kanji = bool(KANJI_REGEX.search(token.text))

        if is_meaningful_pos and has_kanji:
            # (5. append '(lemma_)' in the list)
            kanji_words_set.add(token.lemma_)
            
    # set -> list
    return list(kanji_words_set)

# --- test ---
if __name__ == "__main__":
    test_sentence = "私の部屋に腐ったみかんがあります。"
    
    print("--- Kanji Extraction Test Start ---")
    print(f"Original: {test_sentence}")
    
    extracted_words = extract_kanji_words(test_sentence)
    
    print(f"Extracted Kanji Words (Lemmas): {extracted_words}")
    print("--- Kanji Extraction Test End ---")