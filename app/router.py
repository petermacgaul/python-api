import logging

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


from .models.util import HealthCheck
from .validators.error_schema import ErrorSchema
from .validators.validator_schema import ValidatorSchema
from .routes.users import router as user_router
from .routes.databases import router as database_router
from .routes.authorization import router as auth_router
from .db import get_db

api_router = APIRouter(
    responses={
        "400": {"model": ValidatorSchema, "description": "Bad Request"},
        "500": {"model": ErrorSchema, "description": "Internal Server Error"},
    },
)

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(database_router)


@api_router.get("/health", tags=["Healthcheck"])
async def healthcheck(db: AsyncSession = Depends(get_db)) -> HealthCheck:
    try:
        result = await db.exec(select(1))
        logging.debug("DB healthcheck result: %d", result.one())
        return HealthCheck(message="Alive")
    except Exception as e:
        return HealthCheck(message=f"Database connection error: {e}")
