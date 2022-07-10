from typing import TYPE_CHECKING

from todorant_tui import models

from .create_todo import CreateTodoView

if TYPE_CHECKING:
    from todorant_tui.app import TodorantApp


class EditTodoView(CreateTodoView):
    app: 'TodorantApp'
    todo: models.TodoBase
    title: str = 'Update todo'
    save_or_update_button_text: str = '[underline][b]u[/b]pdate[/underline]'

    async def watch_visible(self, val: bool):
        if val:
            if not self.app.todo_to_update:
                self.app.switch_view('CurrentView')
                return
            self.todo = self.app.todo_to_update
            self.reset_inputs()
            self.refresh()

    def reset_inputs(self):
        self.text.value = self.todo.text
        self.date.value = self.todo.get_full_date() or ''
        self.year_and_month.value = self.todo.month_and_year
        self.is_frog.value = 'True' if self.todo.frog else 'False'
        self.is_completed.value = 'True' if self.todo.completed else 'False'

    async def update_todo(self):
        if not self.date.is_correct or not self.year_and_month.is_correct or not self.text.value:
            return
        date = None
        month_and_year = None
        if self.date.value:
            month_and_year = self.date.value[:7]
            date = self.date.value[8:]
        elif self.year_and_month.value:
            month_and_year = self.year_and_month.value
        if month_and_year is None:
            return
        text = self.text.value
        text = '\n'.join(text.split(r'\n'))
        todo = models.TodoUpdate(**self.todo.dict(by_alias=True))
        todo.text = text
        todo.completed = self.is_completed.bool_value
        todo.frog = self.is_frog.bool_value
        todo.date = date
        todo.month_and_year = month_and_year
        await self.app.api.update_todo(todo=todo,
                                       todo_id=str(self.todo.id))
        self.app.switch_to_previous_view()

    async def on_c(self):
        ...

    async def on_u(self):
        await self.update_todo()
