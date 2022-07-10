import pytest

from todorant_tui.config import settings
from todorant_tui.models import TodoCreate, TodoUpdate
from todorant_tui.todorant_client import TodorantApi


@pytest.mark.asyncio
async def test_client():
    access_token = settings.access_token
    c = TodorantApi(access_token)

    todo = TodoCreate(text='test todo', completed=False,
                      frog=False, monthAndYear="2022-08", date='7')

    await c.create_todo(todo)
    await c.fetch_todos()
    created_todo_from_server = [x for x in c.todos if x.text == todo.text]
    assert len(created_todo_from_server) == 1
    created_todo_from_server = created_todo_from_server[0]
    assert created_todo_from_server.id is not None

    update_todo = TodoUpdate(**created_todo_from_server.dict(by_alias=True))
    update_todo.frog = True
    update_todo.text = "Updated test todo"
    await c.update_todo(created_todo_from_server.id, update_todo)
    await c.fetch_todos()
    assert len([x for x in c.todos if x.text == update_todo.text]) == 1
    todo = [x for x in c.todos if x.text == update_todo.text][0]
    assert todo.frog == update_todo.frog
    await c.delete_todo(created_todo_from_server.id)
    await c.fetch_todos()
    assert len([x for x in c.todos if x.text == update_todo.text]) == 0
