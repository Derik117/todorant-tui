from typing import TYPE_CHECKING, List

from rich.console import Group, RenderableType
from rich.text import Text
from textual.widget import Widget

from todorant_tui import models

if TYPE_CHECKING:
    from todorant_tui.app import TodorantApp


class TodoList(Widget):
    app: 'TodorantApp'

    def __init__(self,
                 todos: List[models.TodoBase],
                 selected: int = 1) -> None:
        super().__init__(name='progress')
        self.todos = todos
        self.selected = selected

    def render(self) -> RenderableType:
        texts = []
        prev_todo = None
        for i, todo in enumerate(self.todos):
            style = ''
            todo_number = i + 1
            if todo_number == self.selected:
                style = 'underline'
            prev_todo_date = None
            if prev_todo:
                prev_todo_date = prev_todo.get_full_date() or prev_todo.month_and_year
            date = todo.get_full_date() or todo.month_and_year
            if prev_todo_date != date:
                date_text = Text(date, justify='left', style='bold')
                if date == self.app.api.date:
                    date_text.append(' TODAY')
                texts.append(date_text)
            todo_text_components = []
            todo_text_components.append(f"{todo_number}. ")
            if todo.completed:
                todo_text_components.append('✅')
            if todo.frog:
                todo_text_components.append(':frog:')
                for _ in range(todo.frog_fails):
                    todo_text_components.append(
                        '[rgb(255,127,80)]*[/rgb(255,127,80)]')
            if todo.frog or todo.completed:
                todo_text_components.append(' ')
            todo_text_components.append(todo.text)
            todo_text = ''.join(todo_text_components)
            if style:
                todo_text = f"[{style}]{todo_text}[/{style}]"
            todo_text = '\t' + todo_text
            texts.append(todo_text)
            prev_todo = todo

        return Group(*texts)
