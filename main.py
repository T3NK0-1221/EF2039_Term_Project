# main.py
# Project Main pipeline
# (OCR, AI Sentence Splitting, and Pre-processing Rules Applied)
# import the functions of translate.py and extract.py
# process the sentences that user input
# create csv file for anki

# (1. Necessary module import)
import csv
import os
import easyocr
import pysbd  # Use independent pysbd
import re     # Use regex for pre-processing

# (1-1. Load AI Models) 
# Load all heavy AI models once at the start
print("Loading AI models... (This may take a moment)")
try:
    from translate import translate_japanese_to_english # translation function
    from extract import extract_kanji_words   # extract funcion
    
    # Load OCR model (Reader)
    # 'ja' (Japanese) and 'en' (English)
    # gpu=False (Using CPU)
    OCR_READER = easyocr.Reader(['ja', 'en'], gpu=False) 
    
    # Load independent 'pysbd' segmenter
    SENTENCE_SPLITTER_NLP = pysbd.Segmenter(language="ja", clean=False)
    
    print("All models loaded successfully.")

except ImportError as e:
    print(f"Error importing module: {e}")
    print("Please check your 'requirements.txt' and installations.")
    exit()
except Exception as e:
    print(f"Error loading models: {e}")
    exit()


# (2. Constant Definition)
# (This section is unchanged)
# Declaration of csv file name
OUTPUT_CSV_FILE = "anki_deck.csv"
FIELDNAMES = ["Front", "Back"] # Anki Card 'Front', 'Back'

def initialize_csv():
    """If there is no previous csv file, add Header for Front and Back."""
    # (This function is unchanged)
    if not os.path.exists(OUTPUT_CSV_FILE):
        with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"Created new file: {OUTPUT_CSV_FILE}")

def add_to_csv(word, example_sentence, translation):
    # (This function is unchanged)
    
    # (3. Formation of Anki card)
    # Front: Kanji word (ex: 書籍)
    front_text = word

    # (3-1. Bold Text)
    # (example_sentence) -> (word) <b> tagging
    # ex: "本電子書籍は..." -> "本電子<b>書籍</b>は..."
    try:
        highlighted_sentence = example_sentence.replace(word, f"<b>{word}</b>")
    except:
        highlighted_sentence = example_sentence # error -> Using Original sentence

    # Back: Bold Original Sentence (<br>) Translated Sentence
    back_text = f"{highlighted_sentence}<br>{translation}"

    # (4. data file CSV append)
    with open(OUTPUT_CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({"Front": front_text, "Back": back_text})

# (5. Core Processing Function)
def process_sentence(sentence):
    """
    Process one sentence: translate, extract, and save to CSV.
    This is a shared function used by both text and OCR modes.
    """
    try:
        # (5-1. Excution of AI model pipeline)
        
        # 1. 2nd module calling -> translation
        print("Translating...")
        translation = translate_japanese_to_english(sentence)

        # (Print translation result to console)
        print(f"Translation: {translation}")
        
        # 2. 3rd module calling -> extract kanji
        print("Extracting Kanji words...")
        kanji_words = extract_kanji_words(sentence)
        
        # 3. Result
        if not kanji_words:
            print("No meaningful Kanji words found in this sentence.")
            return False
            
        print(f"Found {len(kanji_words)} words: {', '.join(kanji_words)}")
        
        # 4. Save in the CSV
        for word in kanji_words:
            add_to_csv(word, sentence, translation)
        
        print(f"Successfully added {len(kanji_words)} card(s) to {OUTPUT_CSV_FILE}.")
        return True
        
    except Exception as e:
        print(f"\nAn error occurred during processing: {e}")
        return False

# (6. Mode 1: Text Input)
def run_text_mode():
    """Handles the loop for manual text input."""
    print("\n--- 📝 Text Input Mode ---")
    print("Enter a Japanese sentence. (Type 'q' or 'exit' to quit)")
    
    while True:
        try:
            # 1. User input(Japanese Sentence block)
            sentence_block = input("\nSentence: ")
            
            # 2. Check Command for quit
            if sentence_block.lower() in ['q', 'exit']: break
            if not sentence_block: continue

            # (3. Pre-processing: Add '。' after 'ます' or 'です' if missing)
            # This rule helps the AI split conversational text correctly.
            sentence_block = re.sub(r'(ます|です)(?![。！？\n])', r'\1。', sentence_block)
            
            # (4. Split using 'pysbd.segment()' method)
            sentences_list = SENTENCE_SPLITTER_NLP.segment(sentence_block)

            # (5. Process each sentence found by the AI)
            for sentence in sentences_list:
                cleaned_sent = str(sentence).strip()
                if cleaned_sent:
                    print(f"\n--- Processing Sub-sentence: [{cleaned_sent}] ---")
                    process_sentence(cleaned_sent)
            
        except KeyboardInterrupt:
            print("\nExiting program. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")

# (7. Mode 2: Image (OCR) Input)
def run_ocr_mode():
    """Handles the loop for image path input and OCR processing."""
    print("\n--- 🖼️ Image (OCR) Mode ---")
    print("Enter the path to your image. (Type 'q' or 'exit' to quit)")
    
    while True:
        try:
            # 1. User input(Image Path)
            image_path = input("\nImage Path: ").strip().strip('"')
            
            # 2. Check Command for quit
            if image_path.lower() in ['q', 'exit']: break
            if not os.path.exists(image_path):
                print("Error: File not found. Please check the path.")
                continue
            
            # 3. Excution of OCR
            results = OCR_READER.readtext(image_path, paragraph=True)
            if not results:
                print("No text detected in the image.")
                continue
            
            full_text = " ".join([res[1] for res in results])
            print(f"--- OCR Result --- \n{full_text}\n--------------------")

            # (4. Pre-processing: Add '。' after 'ます' or 'です' if missing)
            sentence_block = re.sub(r'(ます|です)(?![。！？\n])', r'\1。', full_text)
            
            # (5. Split using 'pysbd.segment()' method)
            sentences_list = SENTENCE_SPLITTER_NLP.segment(sentence_block)
            
            # (6. Process each sentence found by the AI)
            for sentence in sentences_list:
                cleaned_sent = str(sentence).strip()
                if cleaned_sent:
                    print(f"\n--- Processing Sub-sentence: [{cleaned_sent}] ---")
                    process_sentence(cleaned_sent)
            
        except KeyboardInterrupt:
            print("\nExiting program. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred in OCR mode: {e}")

def main():
    """main function (now a mode selector)"""
    # If there is no previous csv file, add Header for Front and Back.
    initialize_csv()
    
    print("--- 🎌 Anki Kanji Card Builder 🎌 ---")
    print(f"Cards will be saved to: {OUTPUT_CSV_FILE}")
    
    # (8. Mode Selection Loop)
    try:
        while True:
            print("\n" + "="*30)
            print("Select mode:")
            print("  [1] Type text manually")
            print("  [2] Use image (OCR)")
            print("  [q] Quit")
            mode = input("Choice (1, 2, or q): ").strip().lower()

            if mode == '1':
                run_text_mode()
            elif mode == '2':
                run_ocr_mode()
            elif mode == 'q':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or q.")
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")

# --- Enable the main() function to operate only when this script is executed directly ---
if __name__ == "__main__":
    main()