# Slayer-Sprache-
Es geht um eine Sprache die Vorwärts und Rückwarts zu lesen ist um die Bedeutung Vorwärts und Rückwärts im Gegensatz zu lesenfrom epitran import Epitran
import json, os

epi = Epitran("deu-Latn")

def make_block(words, block_num):
    lines = []
    for w in words:
        token = w.lower()[::-1]
        ipa = epi.transliterate(w.lower())
        lines.append(f"{token:10} | {w:12} | {ipa:9} | Bedeutung {w} | {w[::-1]} | Substantiv")
    fn = f"blocks/block_{block_num:03d}.txt"
    os.makedirs("blocks", exist_ok=True)
    with open(fn, "w", encoding="utf8") as f:
        f.write("\n".join(lines))
    print(f"✅ {fn} gespeichert.")

# Beispiel:
wortliste = ["Aal", "Baum", "Sonne", "Hund", "Wasser"]
make_block(wortliste, 1) 
