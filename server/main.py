from application.errors import ApplicationError
from domain.errors import DomainError
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from infrastructure.errors import InfrastructureError
from presentation.handlers import (
    finish_walking_router,
    get_image_router,
    health_check_router,
    move_pedestrian_router,
    start_walking_router,
)
from starlette.requests import Request

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(get_image_router)
app.include_router(start_walking_router)
app.include_router(finish_walking_router)
app.include_router(move_pedestrian_router)
app.include_router(health_check_router)


@app.exception_handler(ApplicationError)
async def application_error_handler(
    _: Request,
    exc: ApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "type": exc.type.value,
        },
    )


@app.exception_handler(InfrastructureError)
async def infrastructure_error_handler(
    _: Request,
    exc: InfrastructureError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "type": exc.type.value,
        },
    )


@app.exception_handler(DomainError)
async def domain_error_handler(
    _: Request,
    exc: DomainError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "type": exc.type.value,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    _: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
