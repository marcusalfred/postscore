![logo](./logo.png)

# POSTScore
POSTScore is a simple REST API that allows golfers to track their scores.

## Installation
### Docker 

- clone repo
```
$ cd ./postscore
$  docker compose up --build -d
```

### Uvicorn
- install FastAPI - https://github.com/tiangolo/fastapi?tab=readme-ov-file#installation
- clone repo
```
$ cd ./postscore/app
$ pip install -r requirements.txt
$ uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555 
```

## Usage
### Documentation 
Once running, you can access the OpenAPI documention from http://localhost:5555/docs
