# EF2039_Term_Project

# Japanese Anki Card Builder/ Translator

A powerful tool that automates the creation of Anki cards from Japanese text or images. It utilizes AI for translation, OCR for image recognition, and a dictionary for accurate definitions.

## ✨ Features

This program supports 3 distinct modes depending on your learning style:

1.  **Context Mode (Sentence Study)**
    * **Front:** Japanese sentence (Target word highlighted).
    * **Back:** English translation + Word definition.
2.  **Word Mode (Vocabulary Drill)**
    * **Front:** Japanese word.
    * **Back:** Dictionary definition.
3.  **Translator Tool**
    * Displays the translation on the screen without saving to CSV. Just translating!

### Tech Stack
* **OCR:** EasyOCR (Image-to-Text)
* **Translation:** Hugging Face MarianMT (JP -> EN)
* **Dictionary:** Jamdict (JMDict based)
* **Processing:** Automatic sentence splitting and noise filtering (e.g., removing brackets).

---

## How to install

### 1. Clone & Install Dependencies
Requires Python 3.8+.

```bash
git clone <your-repo-url>
cd japanese-anki-builder
pip install -r requirements.txt
````

### 2\. [IMPORTANT] Manual Dictionary Setup

Due to GitHub file size limits, the dictionary database (`jamdict.db`) is not included. **You must download it manually.**

1.  Visit the [PyPI jamdict-data page](https://www.google.com/search?q=https://pypi.org/project/jamdict-data/%23files).
2.  Download the latest `.tar.gz` file and extract it.
3.  Locate the **`jamdict.db`** file inside the extracted folder (usually under `jamdict_data/`).
      * *Note: If the file is `jamdict.db.xz`, extract it once more to get the `.db` file.*
4.  **Copy `jamdict.db` into the root directory of this project** (where `main.py` is located).

-----

## How to use

### 1\. Run the Program

```bash
python main.py
```

### 2\. Select Card Style

  * `[1] Context Card`: Generates cards with full sentences and translations.
  * `[2] Word Card`: Generates simple word/definition cards.
  * `[3] Translator`: Only displays the translation (No CSV generated).

### 3\. Select Input Method

  * `[1] Type text manually`: Input Japanese text directly.
  * `[2] Use image (OCR)`: Provide the file path to an image containing Japanese text.

-----

## Importing to Anki

1.  Open Anki on your desktop.
2.  Click **File** -\> **Import**.
3.  Select the generated **`anki_deck.csv`** file.
4.  Ensure the following settings:
      * **Field Separator:** Comma
      * **Allow HTML in fields:** ✅ **Checked** (Required for bold formatting).
5.  Click **Import**.
