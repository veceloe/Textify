from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aiohttp

app = FastAPI()
templates = Jinja2Templates(directory="templates")

YOUR_API_KEY = "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"
YOUR_API_URL = "https://api.openai.com/v1/chat/completions"


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/translate", response_class=HTMLResponse)
async def post_translate(request: Request):
    form_data = await request.form()
    text = form_data["text"]
    language = form_data["language"]  # Получение выбранного языка из списка

    headers = {"Authorization": f"Bearer {YOUR_API_KEY}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text + f"\ntranslate this text to {language}"}]  # Использование выбранного языка в запросе
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(YOUR_API_URL, json=data, headers=headers) as response:
            result = await response.json()
            print(result)
            translated_text = result["choices"][0]["message"]["content"].strip()

    return templates.TemplateResponse("index.html", {"request": request, "translated_text": translated_text})


@app.post("/summary", response_class=HTMLResponse)
async def post_summarize(request: Request):
    form_data = await request.form()
    text = form_data["text"]

    headers = {"Authorization": f"Bearer {YOUR_API_KEY}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text + "\nanswer in the russian language, write a summary of the source text by compressing up to 70% of the source text, while retaining the main idea"}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(YOUR_API_URL, json=data, headers=headers) as response:
            result = await response.json()
            print(result)
            summarized_text = result["choices"][0]["message"]["content"].strip()

    return templates.TemplateResponse("index.html", {"request": request, "summarized_text": summarized_text})


@app.post("/generator_code", response_class=HTMLResponse)
async def post_generate_code(request: Request):
    form_data = await request.form()
    text = form_data["text"]
    language = form_data["language"]  # Получение выбранного языка из списка
    headers = {"Authorization": f"Bearer {YOUR_API_KEY}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text + f"\nwrite only the code that performs this task in a programming language to {language}"}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(YOUR_API_URL, json=data, headers=headers) as response:
            result = await response.json()
            print(result)
            generated_code = result["choices"][0]["message"]["content"].strip()

    return templates.TemplateResponse("index.html", {"request": request, "generated_code": generated_code})


@app.post("/synonymizer", response_class=HTMLResponse)
async def post_synonymizer(request: Request):
    form_data = await request.form()
    text = form_data["text"]
    headers = {"Authorization": f"Bearer {YOUR_API_KEY}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text + f"\nнапиши этот же текст но префразировав и заменяя слова синонимами"}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(YOUR_API_URL, json=data, headers=headers) as response:
            result = await response.json()
            print(result)
            paraphrased_text = result["choices"][0]["message"]["content"].strip()

    return templates.TemplateResponse("index.html", {"request": request, "paraphrased_text": paraphrased_text})


@app.post("/essay_generator", response_class=HTMLResponse)
async def post_essay_generator(request: Request):
    form_data = await request.form()
    text = form_data["text"]
    headers = {"Authorization": f"Bearer {YOUR_API_KEY}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text + f"\nнапиши только ээсе по написанному выше описанию"}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(YOUR_API_URL, json=data, headers=headers) as response:
            result = await response.json()
            print(result)
            generated_text = result["choices"][0]["message"]["content"].strip()

    return templates.TemplateResponse("index.html", {"request": request, "generated_text": generated_text})