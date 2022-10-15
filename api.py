from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.db import Base, engine
from routes.channels import app as channels_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Routes
app.include_router(channels_router, prefix='/channels', tags=['channels'])

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://klasinky.github.io/karmaland-ui/",
    "https://klasinky.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "Hello World"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("api:app", host='localhost', port=8000, debug=True, reload=True)
