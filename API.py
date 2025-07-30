from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI(title="Slayer-Lexikon API")
lex = json.load(open("lexicon.json", encoding="utf8"))

@app.get("/api/v1.0/token/{token}")
def get_token(token: str):
    return JSONResponse(lex.get(token, {"error": "Token nicht gefunden"}))

@app.get("/api/v1.0/search")
def search(query: str):
    result = {k:v for k,v in lex.items() if query in k or query in v["deutsch"]}
    return JSONResponse(result)
