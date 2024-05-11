'''
- OpenAPI description and tags
- Route Organization
'''

from fastapi import FastAPI, APIRouter
from routes.players import playerrouter
from routes.courses import courserouter
from routes.rounds import roundrouter
from fastui import AnyComponent, FastUI
from fastui import components as c


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


'''
# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://10.0.1.45:*"
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
app.include_router(playerrouter)
app.include_router(courserouter)
app.include_router(roundrouter)

router = APIRouter()

@router.get('/', response_model=FastUI, response_model_exclude_none=True)
def api_index() -> list[AnyComponent]:
    # language=markdown
    markdown = """\
This site provides a demo of [FastUI](https://github.com/pydantic/FastUI), the code for the demo
is [here](https://github.com/pydantic/FastUI/tree/main/demo).

The following components are demonstrated:

* `Markdown` — that's me :-)
* `Text`— example [here](/components#text)
* `Paragraph` — example [here](/components#paragraph)
* `PageTitle` — you'll see the title in the browser tab change when you navigate through the site
* `Heading` — example [here](/components#heading)
* `Code` — example [here](/components#code)
* `Button` — example [here](/components#button-and-modal)
* `Link` — example [here](/components#link-list)
* `LinkList` — example [here](/components#link-list)
* `Navbar` — see the top of this page
* `Footer` — see the bottom of this page
* `Modal` — static example [here](/components#button-and-modal), dynamic content example [here](/components#dynamic-modal)
* `ServerLoad` — see [dynamic modal example](/components#dynamic-modal) and [SSE example](/components#server-load-sse)
* `Image` - example [here](/components#image)
* `Iframe` - example [here](/components#iframe)
* `Video` - example [here](/components#video)
* `Table` — See [cities table](/table/cities) and [users table](/table/users)
* `Pagination` — See the bottom of the [cities table](/table/cities)
* `ModelForm` — See [forms](/forms/login)

Authentication is supported via:
* token based authentication — see [here](/auth/login/password) for an example of password authentication
* GitHub OAuth — see [here](/auth/login/github) for an example of GitHub OAuth login
"""


@router.get('/{path:path}', status_code=404)
async def api_404():
    # so we don't fall through to the index page
    return {'message': 'Not Found'}

