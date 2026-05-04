from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.quiz import router as quiz_router
from app.api.endpoints.results import router as results_router
from app.api.endpoints.profile import router as profile_router

api_router = APIRouter()
api_router.include_router(auth_router)     # /login, /register гэх мэт
api_router.include_router(quiz_router)     # /generate-quiz
api_router.include_router(results_router)  # /results
api_router.include_router(profile_router)  # /profile-data
