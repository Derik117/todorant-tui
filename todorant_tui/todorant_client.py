import datetime as dt
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from httpx import AsyncClient, Response

from .models import Current, State, TodoBase, TodoCreate, TodoUpdate


@dataclass
class TodorantApi:
    access_token: str
    _client: AsyncClient = field(default_factory=AsyncClient)
    todos: List[TodoBase] = field(default_factory=list)
    current = Current(todosCount=0, incompleteTodosCount=0, todo=None)

    def __post_init__(self) -> None:
        self._client.headers['token'] = self.access_token
        self._client.headers['User-Agent'] = "httpx: TUI client"
        self._client.base_url = "https://backend.todorant.com"

    @property
    def date(self) -> str:
        return dt.date.today().strftime("%Y-%m-%d")

    @property
    def time(self) -> str:
        return dt.datetime.now().strftime("%HH-%MM")

    async def _get(self, path: str, params: Dict[str, Any] = None) -> Dict[Any, Any]:
        response = await self._client.get(
            path, params=params)
        if response.is_error:
            raise AttributeError(
                f"Error get {response.request.url}. {params=}. status_code={response.status_code}. text={response.text}")
        return response.json()

    async def _post(self, path: str, data) -> Response:
        response = await self._client.post(
            path, json=data)
        if response.is_error:
            raise AttributeError(
                f"Error post {response.request.url}. {data=}. status_code={response.status_code}. text={response.text}")
        return response

    async def _put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Response:
        if data is None:
            data = {}
        for col in ['updatedAt', 'createdAt']:
            if col in data:
                del data[col]
        response = await self._client.put(
            path, json=data)
        if response.is_error:
            raise AttributeError(
                f"Error put {response.request.url}. {data=}. status_code={response.status_code}. text={response.text}")
        return response

    def _delete(self, path: str):
        return self._client.delete(path)

    async def delete_todo(self, todo_id: str) -> None:
        await self._delete(f'/todo/{todo_id}')

    async def done_todo(self, todo_id: str) -> None:
        await self._put(f'/todo/{todo_id}/done')

    async def update_todo(self, todo_id: str, todo: TodoUpdate) -> None:
        await self._put(f'/todo/{todo_id}?date={self.date}&time={self.time}',
                        data={"today": self.date, **todo.dict(by_alias=True, )}, )

    async def fetch_todos(self, completed: bool = False):
        data = await self._get(
            '/todo', {'date': self.date, 'today': self.date, "time": self.time, 'completed': completed})
        self.todos = [TodoBase(**x)
                      for x in data['todos']]

    async def fetch_current(self):
        self.current = Current(**await self._get('/todo/current', params={'date': self.date}))

    async def state(self) -> State:
        return State(**await self._get('/state/', {'date': self.date, 'today': self.date, "time": self.time}))

    async def create_todo(self, todo: TodoCreate):
        await self._post('/todo/', todo.dict(by_alias=True))
