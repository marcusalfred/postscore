'''
- OpenAPI description and tags
- Route Organization
'''
from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter, __version__
from .routes.players import playerrouter
from .routes.courses import courserouter
from .routes.rounds import roundrouter
from time import time
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
import markdown



app = FastAPI(title='POSTscore',
    description='An API to record you scores at different golf courses',
    version='0.1.0',
    openapi_tags=[
        {
            'name': 'Players',
            'description': 'Players of the Game'
        },
        {
            'name': 'Courses',
            'description': 'Where the players play Golf'
        },
        {
            'name': 'Rounds',
            'description': 'Rounds of Golf'
        }
    ]
)
app.include_router(playerrouter)
app.include_router(courserouter)
app.include_router(roundrouter)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/static/example.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
    md_html = markdown.markdown(text)

    return HTMLResponse(md_html)

#@app.get("/")
#async def root():
#    return HTMLResponse(html)


@app.get('/ping')
async def hello(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'res': 'pong', 'version': __version__, "time": time(), "token": token}
