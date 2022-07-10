from typing import List, Literal, Optional, Type, Union

from textual import events, log
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget

from . import models, views
from .config import settings
from .todorant_client import TodorantApi


class Sections:
    TABS = 'tabs'
    TODOS = 'todos'
    PROGRESS = 'progress'
    CURRENT_TASK = 'current_task'
    BUTTONS = 'buttons'


VIEW_CLASS = Union[
    Type[views.CurrentView],
    Type[views.CreateTodoView],
    Type[views.EditTodoView],
    Type[views.PlanningView],
    Literal['CurrentView',
            'CreateTodoView',
            'EditTodoView',
            'PlanningView',
            ]
]


class TodorantApp(App):
    api: TodorantApi = TodorantApi(settings.access_token)
    loading = Reactive(False)
    views: List[Widget]
    current_view: Widget
    previous_view: Widget
    todo_to_update: Optional[models.TodoBase] = None

    def switch_view(self, view_class: VIEW_CLASS):
        if isinstance(view_class, str):
            view_class = getattr(views, view_class)
        for view in self.views:
            visible = view.__class__.__name__ == view_class.__name__
            view.visible = visible
            if visible:
                log(f"switch_view to {view_class} {view}")
                self.previous_view = self.current_view or view
                self.current_view = view

    def switch_to_previous_view(self):
        self.switch_view(self.previous_view.__class__)

    async def on_mount(self) -> None:
        self.views = [
            views.CurrentView(),
            views.CreateTodoView(),
            views.EditTodoView(),
            views.PlanningView(),
        ]
        self.previous_view = self.views[0]
        self.current_view = self.views[0]
        for view in self.views:
            await self.view.dock(view)
        self.switch_view(views.CurrentView)

    async def on_key(self, event: events.Key) -> None:
        func = getattr(self.current_view, f"on_{event.key}", None)
        if func:
            await func()

    async def on_load(self, _):
        ...
