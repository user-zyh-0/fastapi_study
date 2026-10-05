from fastapi import APIRouter

import service
from schemas import TodoCreate, TodoOut

router = APIRouter(prefix="/todos", tags=["待办"])


@router.post("", response_model=TodoOut)
def create_todo(payload: TodoCreate):
    return service.create_todo(payload.title, payload.done)


@router.get("", response_model=list[TodoOut])
def list_todos():
    return service.list_todos()


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int):
    return service.get_todo(todo_id)


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoCreate):
    return service.update_todo(todo_id, payload.title, payload.done)


@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    service.delete_todo(todo_id)
    return {"message": "删除成功"}
