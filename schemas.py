from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    done: bool = False


class TodoOut(TodoCreate):
    id: int

# todos = []
# next_id = 1
