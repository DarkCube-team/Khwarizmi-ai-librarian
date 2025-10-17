# Phase 1: Preprocessing (Simplified — Fixed Language Mapping)
import os
import re
import pandas as pd


files = [
    ("کتاب فارسی.xls", "Persian"),
    ("1838.xls", "English"),
]

for file_name, lang in files:
    file_path = os.path.join(folder_path, file_name)
    print(f"Processing {lang} file: {file_path}")

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"  Excel read failed ({e}), trying XML mode...")
        try:
            df = pd.read_xml(file_path)
        except Exception as e2:
            print(f"  XML read also failed: {e2}")
            continue

    print(f"  Successfully read {len(df)} rows and {len(df.columns)} columns.")
    print(df.head(3))



# Arabic → Persian replacements
ARABIC_TO_PERSIAN = {
    "ي": "ی",
    "ك": "ک",
    "ة": "ه",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
    "ئ": "ی"
}

# Arabic diacritics (harakat)
DIACRITICS_PATTERN = re.compile(r"[\u0610-\u061A\u064B-\u065F\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]")

# Unwanted symbols (ZWNJ, bullets, dashes, underscores, quotes, etc.)
EXTRA_SYMBOLS_PATTERN = re.compile(r"[\u200c\u200f\u200e◀▶■▪•\-\_\~\*\#\@\%\^\=\+\|\[\]\{\}\"“”‘’«»<>]")


def normalize_text(text: str) -> str:
    """Clean and normalize both Persian and English text."""
    if not isinstance(text, str):
        return text

    # Arabic → Persian mapping
    for ar, fa in ARABIC_TO_PERSIAN.items():
        text = text.replace(ar, fa)

    # Remove Tatweel
    text = text.replace("ـ", "")

    # Remove diacritics
    text = DIACRITICS_PATTERN.sub("", text)

    # Remove special symbols
    text = EXTRA_SYMBOLS_PATTERN.sub(" ", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Lowercase (for English)
    text = text.lower()

    return text


def normalize_excel(input_path: str, output_path: str):
    """Normalize a single Excel file and save it."""
    print(f"\nProcessing: {input_path}")

    # Choose proper engine
    engine = "openpyxl" if input_path.endswith(".xlsx") else "xlrd"

    # Read Excel
    try:
        df = pd.read_excel(input_path, engine=engine)
    except Exception as e:
        print(f" Error reading {input_path}: {e}")
        return

    # Normalize all text columns
    for col in df.columns:
        df[col] = df[col].apply(normalize_text)

    # Save cleaned file
    df.to_excel(output_path, index=False)
    print(f"Saved normalized file to: {output_path}")


# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    # Input file paths
    persian_input = r"" #address of the file
    english_input = r"" #address of the file

    # Output file paths
    persian_output = r"" #address of the file
    english_output = r"" #address of the file

    # Normalize each file separately
    normalize_excel(persian_input, persian_output)
    normalize_excel(english_input, english_output)
