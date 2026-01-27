from fastapi import FastAPI

from app.routes import setup_routes
from app.utils.life_cycle_handler import setup_event_handlers
from app.utils.middlewares import setup_middlewares
from app.connectors.database_connector import Base, engine

from app.routes.router import router as chat_router

app = FastAPI()
app.include_router(chat_router)


setup_routes(app)
setup_middlewares(app)
setup_event_handlers(app)
