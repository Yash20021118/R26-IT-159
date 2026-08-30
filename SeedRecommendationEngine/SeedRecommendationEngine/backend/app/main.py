from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import chat_router, health_router, model_info_router, predict_router
from .utils.config import settings
from .utils.logger import configure_logging

configure_logging(settings.log_level)

app = FastAPI(title=settings.api_title, version=settings.api_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(predict_router)
app.include_router(model_info_router)
app.include_router(chat_router)

