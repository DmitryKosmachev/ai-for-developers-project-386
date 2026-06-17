"""FastAPI-приложение «Запись на звонок». Реализация контракта из spec/."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.errors import ApiException
from app.routers import bookings, event_types, owner

app = FastAPI(title="Запись на звонок API", version="1.0.0")

# Фронтенд — отдельный клиент; для разработки разрешаем любые источники.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ApiException)
def handle_api_exception(_request: Request, exc: ApiException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


@app.exception_handler(RequestValidationError)
def handle_validation_error(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Приводим ошибки валидации тела запроса к формату контракта."""
    errors = exc.errors()
    if errors:
        first = errors[0]
        location = ".".join(str(p) for p in first.get("loc", []) if p != "body")
        message = first.get("msg", "Некорректные данные")
        if location:
            message = f"{location}: {message}"
    else:
        message = "Некорректные данные"
    return JSONResponse(
        status_code=422,
        content={"code": "validation_error", "message": message},
    )


app.include_router(owner.router)
app.include_router(event_types.router)
app.include_router(bookings.router)
