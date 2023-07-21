from fastapi import FastAPI, APIRouter
from .routers import notes, users, auth
from .database import get_db, SessionLocal, engine
from .import models

import uvicorn
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# users = [
#     {'name': 'prince', 'age': 32},
#     {'name': 'jack', 'age': 23}
# ]


@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)
    