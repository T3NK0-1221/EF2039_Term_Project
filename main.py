# main.py
# Project Main pipeline
# (OCR, AI Sentence Splitting, Dictionary Lookup, and Anki CSV Generation)

import csv
import os
import easyocr
import pysbd
import re
from dict_helper import get_jamdict

# (1. Global Configuration)
# 1: Context (Context Style) - Save to CSV O
# 2: Word (Word Style)       - Save to CSV O
# 3: Translator (Simple Translator) - No CSV Save (Display Only)
CURRENT_CARD_STYLE = '2' 

# (2. Load AI Models)
print("Loading AI models... (This may take a moment)")
try:
    from translate import translate_japanese_to_english
    from extract import extract_kanji_words
    
    OCR_READER = easyocr.Reader(['ja', 'en'], gpu=False) 
    SENTENCE_SPLITTER_NLP = pysbd.Segmenter(language="ja", clean=False)
    
    print("Loading Dictionary (Jamdict)...")
    JMD = get_jamdict()
    if JMD:
        print("✅ Dictionary loaded successfully.")
    else:
        print("⚠️ Dictionary failed to load.")
    
    print("All models loaded successfully.")

except Exception as e:
    print(f"Error loading models: {e}")
    exit()

# (3. File Configuration)
OUTPUT_CSV_FILE = "anki_deck.csv"
FIELDNAMES = ["Front", "Back"]

def initialize_csv():
    """Creates a new empty file if CSV doesn't exist (no header)."""
    if not os.path.exists(OUTPUT_CSV_FILE):
        with open(OUTPUT_CSV_FILE, mode='w', encoding='utf-8-sig') as f:
            pass 
        print(f"Created new file: {OUTPUT_CSV_FILE}")

def add_to_csv(front_text, back_text):
    """Function to append content to CSV file."""
    with open(OUTPUT_CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({"Front": front_text, "Back": back_text})

def lookup_word_meaning(word):
    """Dictionary lookup and tag removal."""
    if not JMD: return "Dictionary not loaded."
    try:
        result = JMD.lookup(word)
        if result.entries:
            raw_definition = str(result.entries[0].senses[0])
            clean_definition = raw_definition.split("((")[0].strip()
            return clean_definition
        else:
            return "No definition found."
    except Exception as e:
        return f"Error: {e}"

#Integrated Text Preprocessing Function
def preprocess_text(text):
    """
    Pre-processes the input text to clean it up.
    1. Remove brackets (「」『』) -> Improves translation quality.
    2. Fix sentence endings (Add '。' after 'ます'/'です' if missing).
    """
    # 1. Remove brackets
    cleaned = re.sub(r'[「」『』]', '', text)
    
    # 2. Fix period
    cleaned = re.sub(r'(ます|です)(?![。！？\n])', r'\1。', cleaned)
    
    return cleaned.strip()

def process_sentence(sentence):
    global CURRENT_CARD_STYLE

    try:
        # --- [Style 3] Simple Translator Mode (No CSV Save) ---
        if CURRENT_CARD_STYLE == '3':
            print("Translating...")
            translation = translate_japanese_to_english(sentence)
            
            # Output to screen only (No Save)
            print("\n" + "="*20 + " [Translator Result] " + "="*20)
            print(f"🇯🇵 Original: {sentence}")
            print(f"🇺🇸 English : {translation}")
            print("="*60 + "\n")
            return True

        # --- [Style 1 & 2] Card Generation Mode ---
        print("Extracting Kanji words...")
        kanji_words = extract_kanji_words(sentence)
        
        if not kanji_words:
            print("No meaningful Kanji words found.")
            return False
            
        print(f"Found {len(kanji_words)} words: {', '.join(kanji_words)}")
        
        # Translation needed only for Style 1
        translation = ""
        if CURRENT_CARD_STYLE == '1':
            print("Translating for context...")
            translation = translate_japanese_to_english(sentence)

        for word in kanji_words:
            definition = lookup_word_meaning(word)
            print(f" - {word}: {definition}")
            
            # --- [Style 1] Context Style ---
            if CURRENT_CARD_STYLE == '1':
                try:
                    # Front: Highlight word in sentence
                    front_text = sentence.replace(word, f"<b>{word}</b>")
                except:
                    front_text = sentence
                
                back_text = (
                    f"<b>[Meaning]</b> {definition}<br><hr>"
                    f"<b>[Trans]</b> {translation}"
                )
                add_to_csv(front_text, back_text)

            # --- [Style 2] Word Style ---
            elif CURRENT_CARD_STYLE == '2':
                add_to_csv(word, definition)
        
        print(f"✅ Added {len(kanji_words)} cards to CSV.")
        return True

    except Exception as e:
        print(f"Error processing sentence: {e}")
        return False

# --- Execution Modes ---
def run_text_mode():
    print("\n--- 📝 Text Input Mode ---")
    print("Enter a Japanese sentence. ('q' to quit)")
    while True:
        sentence_block = input("\nSentence: ").strip()
        if sentence_block.lower() in ['q', 'exit']: break
        if not sentence_block: continue

        #Use integrated preprocessing function
        sentence_block = preprocess_text(sentence_block)
        
        sentences_list = SENTENCE_SPLITTER_NLP.segment(sentence_block)

        for sentence in sentences_list:
            cleaned = str(sentence).strip()
            if cleaned:
                if CURRENT_CARD_STYLE != '3':
                    print(f"\n--- Processing: [{cleaned}] ---")
                process_sentence(cleaned)

def run_ocr_mode():
    print("\n--- 🖼️ Image (OCR) Mode ---")
    print("Enter image path. ('q' to quit)")
    while True:
        image_path = input("\nImage Path: ").strip().strip('"')
        if image_path.lower() in ['q', 'exit']: break
        if not os.path.exists(image_path):
            print("File not found.")
            continue
            
        print("Reading image...")
        results = OCR_READER.readtext(image_path, paragraph=True)
        if not results:
            print("No text detected.")
            continue
        
        full_text = " ".join([res[1] for res in results])
        print(f"--- OCR Result --- \n{full_text}\n--------------------")

        #Use integrated preprocessing function
        sentence_block = preprocess_text(full_text)
        
        sentences_list = SENTENCE_SPLITTER_NLP.segment(sentence_block)
        
        for sentence in sentences_list:
            cleaned = str(sentence).strip()
            if cleaned:
                if CURRENT_CARD_STYLE != '3':
                    print(f"\n--- Processing: [{cleaned}] ---")
                process_sentence(cleaned)

def select_card_style():
    global CURRENT_CARD_STYLE
    print("\n" + "="*55)
    print("📇 Select Mode")
    print("  [1] Context Card (Front: Sentence / Back: Detail) -> Save CSV")
    print("  [2] Word Card    (Front: Word     / Back: Meaning) -> Save CSV")
    print("  [3] Translator   (No CSV, Just Translate)          -> Display Only")
    print("="*55)
    
    choice = input("Choice (1, 2, or 3): ").strip()
    if choice in ['1', '2', '3']:
        CURRENT_CARD_STYLE = choice
        styles = {'1': 'Context Card', '2': 'Word Card', '3': 'Translator Tool'}
        print(f"✅ Mode set to: {styles[choice]}")
    else:
        print("⚠️ Invalid choice. Defaulting to [2] Word Card.")
        CURRENT_CARD_STYLE = '2'

def main():
    initialize_csv()
    
    print("--- 🎌 Anki Kanji Card Builder 🎌 ---")
    
    select_card_style()
    
    try:
        while True:
            print("\n" + "-"*30)
            styles = {'1': 'Context Card', '2': 'Word Card', '3': 'Translator Tool'}
            print(f"Current Mode: [{styles[CURRENT_CARD_STYLE]}]")
            print("Select Input Mode:")
            print("  [1] Type text manually")
            print("  [2] Use image (OCR)")
            print("  [c] Change Mode")
            print("  [q] Quit")
            
            mode = input("Choice: ").strip().lower()

            if mode == '1':
                run_text_mode()
            elif mode == '2':
                run_ocr_mode()
            elif mode == 'c':
                select_card_style()
            elif mode == 'q':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")

if __name__ == "__main__":
    main()