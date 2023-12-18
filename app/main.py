'''
- OpenAPI description and tags
- Route Organization 
'''

from fastapi import FastAPI
from routes.players import playerrouter
from routes.courses import courserouter
from routes.rounds import roundrouter

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
