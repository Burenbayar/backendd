from fastapi import FastAPI
from app.core.cors import setup_cors
from app.api.api import api_router
from app.db.session import Base, engine

def create_app():
    app = FastAPI(title="Quiz API")
    setup_cors(app)

    # tables create
    Base.metadata.create_all(bind=engine)

    app.include_router(api_router)

    @app.get("/")
    async def root():
        return {"message": "Quiz API working"}

    return app

app = create_app()
