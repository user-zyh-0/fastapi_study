import repository

MAX_TITLE_LEN = 100


class TodoValidationError(Exception):
    """业务校验不通过时抛出"""


class TodoNotFoundError(Exception):
    """待办不存在时抛出"""


def init_db():
    """启动时初始化数据库，转发给数据层"""
    repository.init_db()


def _clean_title(title: str) -> str:
    """清洗并校验标题，返回处理后的标题"""
    title = title.strip()
    if not title:
        raise TodoValidationError("标题不能为空")
    if len(title) > MAX_TITLE_LEN:
        raise TodoValidationError(f"标题不能超过 {MAX_TITLE_LEN} 个字符")
    return title


def create_todo(title: str, done: bool = False):
    return repository.create_todo(_clean_title(title), done)


def list_todos():
    return repository.list_todos()


def get_todo(todo_id: int):
    todo = repository.get_todo(todo_id)
    if not todo:
        raise TodoNotFoundError(f"待办 {todo_id} 不存在")
    return todo


def update_todo(todo_id: int, title: str, done: bool):
    result = repository.update_todo(todo_id, _clean_title(title), done)
    if not result:
        raise TodoNotFoundError(f"待办 {todo_id} 不存在")
    return result


def delete_todo(todo_id: int):
    result = repository.delete_todo(todo_id)
    if not result:
        raise TodoNotFoundError(f"待办 {todo_id} 不存在")
    return True
