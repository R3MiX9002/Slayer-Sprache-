import re, os
from pathlib import Path

TEXT_DIR   = Path("source_texts")
BLOCKS_DIR = Path("blocks")
BLOCK_SIZE = 50

def extract_words():
    words = []
    for file in TEXT_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf8").lower()
        tokens = re.findall(r"[a-zäöüß]+", text)
        words += tokens
    return list(dict.fromkeys(words))  # unique

def create_blocks(words):
    BLOCKS_DIR.mkdir(exist_ok=True)
    for i in range(0, min(len(words), 999*BLOCK_SIZE), BLOCK_SIZE):
        block = words[i:i+BLOCK_SIZE]
        fn = BLOCKS_DIR / f"block_{i//BLOCK_SIZE+1:03d}.txt"
        fn.write_text("\n".join(block), encoding="utf8")
        print(f"✅ {fn.name} mit {len(block)} Wörtern")

if __name__ == "__main__":
    words = extract_words()
    print(f"🔤 {len(words)} eindeutige Wörter gefunden.")
    create_blocks(words)
