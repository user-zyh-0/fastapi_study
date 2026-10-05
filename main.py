from fastapi import FastAPI
from fastapi.responses import JSONResponse

import service
from api import todos
from service import TodoNotFoundError, TodoValidationError

app = FastAPI()

app.include_router(todos.router)

service.init_db()


@app.exception_handler(TodoNotFoundError)
def handler_not_found_exception(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(TodoValidationError)
def handler_validation_exception(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
