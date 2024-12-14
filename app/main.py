'''
- OpenAPI description and tags
- Route Organization
'''

from fastapi import FastAPI, APIRouter, __version__
from routes.players import playerrouter
from routes.courses import courserouter
from routes.rounds import roundrouter
from time import time
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


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
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}
