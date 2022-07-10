from typing import Optional

from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual.widget import Widget

from todorant_tui import models
from todorant_tui.todorant_client import TodorantApi


class CurrentTask(Widget):

    def __init__(self, todo: Optional[models.TodoBase]) -> None:
        super().__init__(name='current_task')
        self.todo = todo
        self.api: TodorantApi = self.app.api  # type: ignore

    def render(self) -> RenderableType:
        if self.todo:
            todo_text_components = []
            if self.todo.frog:
                todo_text_components.append(':frog:')
                for _ in range(self.todo.frog_fails):
                    todo_text_components.append(
                        '[rgb(255,127,80)]*[/rgb(255,127,80)]')
                if self.todo.frog_fails:
                    todo_text_components.append(' ')
            todo_text_components.append('\n' + self.todo.text)
            text = ''.join(todo_text_components)
        elif self.api.current.todos_count == 0:

            text = Text(
                '\n'.join(
                    ('🐝',
                     'To infinity!',
                     'You don\'t have any todos for today. If you want to work — add a new todo for today or take the todos from future days.')),
                justify='center')
            text = Align(text, vertical='middle', align='center')
        else:
            text = Text(
                '\n'.join(
                    ('🎉',
                     'Congratulations!',
                     '🥳 You did it! All the tasks for today are done, go get rest or maybe dance a little 💃',
                     ),
                ),
                justify='center')
            text = Align(text, vertical='middle', align='center')
        return Panel(text,
                     title="Current task")
