![logo](./postscore.svg)

# POSTScore
POSTScore is a simple REST API that allows golfers to track their scores.

## Installation
### Docker 
Install docker and docker-compose 
cd into project directory 
docker compose up --build -d 
### Uvicorn
install FastAPI - https://github.com/tiangolo/fastapi?tab=readme-ov-file#installation
cd into {projectdirectory}/app
uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555

## Usage
### Documentation 
Once running, you can access the OpenAPI documention from "localhost:5555/docs"
