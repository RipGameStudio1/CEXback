from .exchanges import router as exchanges_router
from .coins import router as coins_router
from .pairs import router as pairs_router
from .users import router as users_router

__all__ = ['exchanges_router', 'coins_router', 'pairs_router', 'users_router']
