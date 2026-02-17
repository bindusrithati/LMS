from fastapi import FastAPI

from app.routes import setup_routes
from app.utils.life_cycle_handler import setup_event_handlers
from app.utils.middlewares import setup_middlewares
from app.connectors.database_connector import Base, engine


from app.routes.ws_chat import router as ws_chat_router
from app.routes.dashboard_route import router as dashboard_router

app = FastAPI()
app.include_router(ws_chat_router)
app.include_router(dashboard_router)


setup_routes(app)
setup_middlewares(app)
setup_event_handlers(app)
