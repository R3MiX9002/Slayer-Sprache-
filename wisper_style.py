import json, re
from pathlib import Path

IN  = Path("lexicon.json")
OUT = Path("lexicon_styled.json")

def style_token(token):
    t = "h" + re.sub(r"s(?=.)", "sch", token) + "s"
    return t

def style_ipa(ipa):
    return ipa.replace("s", "ʃ", 1) + "s̺"

lex = json.loads(IN.read_text(encoding="utf8"))
styled = {}
for k, v in lex.items():
    s_tok = style_token(k)
    styled[s_tok] = {**v, "styled_token": s_tok, "ipa": style_ipa(v["ipa"])}

OUT.write_text(json.dumps(styled, indent=2, ensure_ascii=False), encoding="utf8")
