from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import api

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="ff29aadd726675a2671da921a53d72e36ec043cdc80056f2f40e602107e6b0f7")
app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods={"OPTIONS", "GET", "POST"},
    allow_headers={"*"},
)


@app.on_event("startup")
def on_startup():
    from app import model
    from app.database import engine

    model.Base.metadata.create_all(bind=engine)


app.include_router(api.router)
