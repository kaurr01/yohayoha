from typing import Optional

import nltk
import uvicorn

from fastapi import FastAPI, Form, Header, Request
from fastapi.templating import Jinja2Templates
from rake_nltk import Rake

app = FastAPI(title="FastAPI & HTMX")

templates = Jinja2Templates(directory="templates")

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

@app.get("/")
async def home(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request:
        return templates.TemplateResponse("age.html", context={"request": request, "age": 23})
    return templates.TemplateResponse("index.html", context={"request": request, "name": "Peter Pan"})

@app.post("/extract_key")
async def extract_key(request: Request, text: str = Form(...), hx_request: Optional[str] = Header(None)):
    r = Rake(include_repeated_phrases=False)
    r.extract_keywords_from_text(text)
    result = r.get_ranked_phrases()[:20]
    if hx_request:
        return templates.TemplateResponse("key.html", context={"request": request, "result": result})
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
