# main.py
# Project Main pipeline
# import the functions of translate.py and extract.py
# process the sentences that user input
# create csv file for anki

# (1. Necessary module import)
import csv
import os
from translate import translate_japanese_to_english # translation function in the translate.py
from extract import extract_kanji_words   # extract funcion in the extract.py

# (2. Constant Definition)
# Declaration of csv file name
OUTPUT_CSV_FILE = "anki_deck.csv"
FIELDNAMES = ["Front", "Back"] # Anki Card 'Front', 'Back'

def initialize_csv():
    """If there is no previous csv file, add Header for Front and Back."""
    if not os.path.exists(OUTPUT_CSV_FILE):
        with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"Created new file: {OUTPUT_CSV_FILE}")

def add_to_csv(word, example_sentence, translation):
    """
    Append the Anki card data into the CSV file.
    """
    # (3. Formation of Anki card csv file)
    # Front: Kanji
    # Back: Original sentence(jp) (<br>) Translated sentence(en)
    front_text = word
    back_text = f"{example_sentence}<br>{translation}"
    
    # (4. Put data in the CSV file.)
    # mode='a' -> append data not overwrite
    with open(OUTPUT_CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({"Front": front_text, "Back": back_text})

def main():
    """main function"""
    # 0. If there is no previous csv file, add Header for Front and Back.
    initialize_csv()
    
    print("--- 🎌 Anki Kanji Card Builder 🎌 ---")
    print(f"Cards will be saved to: {OUTPUT_CSV_FILE}")
    print("Enter a Japanese sentence. (Type 'q' or 'exit' to quit)")
    
    # (5. Loop for the User input)
    while True:
        try:
            # 1. User input(Japanese Sentence)
            sentence = input("\nSentence: ")
            
            # 2. Check Command for quit
            if sentence.lower() in ['q', 'exit']:
                print("Exiting program. Goodbye!")
                break
                
            if not sentence:
                continue

            # (6. Excution of AI model pipeline)
            # 3. 2nd module calling -> translation
            print("Translating...")
            translation = translate_japanese_to_english(sentence)
            
            # 4. 3rd module calling -> extract kanji
            print("Extracting Kanji words...")
            kanji_words = extract_kanji_words(sentence)
            
            # 5. Result
            if not kanji_words:
                print("No meaningful Kanji words found in this sentence.")
                continue
                
            print(f"Found {len(kanji_words)} words: {', '.join(kanji_words)}")
            
            # 6. Save in the CSV
            for word in kanji_words:
                add_to_csv(word, sentence, translation)
            
            print(f"Successfully added {len(kanji_words)} card(s) to {OUTPUT_CSV_FILE}.")

        except KeyboardInterrupt:
            # (Quit by Ctrl+C)
            print("\nExiting program. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")

# --- Enable the main() function to operate only when this script is executed directly ---
if __name__ == "__main__":
    main()