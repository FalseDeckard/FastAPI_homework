from fastapi import FastAPI, Path
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse

app = FastAPI()

@app.get("/")
def root():
    return {'message': 'Hello, mate'}

@app.get("/add")
def add(x: int, y: int) -> int:
    return x + y

@app.get("/double/{number}")
def double(number: int) -> int:
    return number * 2

@app.get("/welcome/{name}/{surname}/{age}")
def welcome(name: str = Path(min_length=2, max_length=20)) -> str:
    return f'good luck, {name}!'


@app.get("/text")
def get_text():
    content = 'Lorem ipsum'
    return PlainTextResponse(content=content)


@app.get("/html")
def get_html():
    content = '<h2>WRYYYYY</h2>'
    return HTMLResponse(content=content)


@app.get("/file")
def get_file():
    content = 'index.html'
    return FileResponse(
        content,
        media_type='application/octet-stream',
        filename='index_2.html'
    )


@app.get("/html", response_class=HTMLResponse)
def get_html():
    content = '<h2>WRYYYYY</h2>'
    return content