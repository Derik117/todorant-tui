from typing import TYPE_CHECKING, Optional

from rich.text import Text
from textual import widgets
from textual.views import GridView  # type: ignore

from todorant_tui import components, models

if TYPE_CHECKING:
    from todorant_tui.app import TodorantApp

import math


class PlanningView(GridView):
    app: 'TodorantApp'
    PAGE_SIZE: int = 7
    current_page = 1
    selected = 1
    show_completed: bool = False

    @property
    def total_pages(self):
        return math.ceil(len(self.app.api.todos) / self.PAGE_SIZE)

    @property
    def selected_todo(self) -> Optional[models.TodoBase]:
        if len(self.current_page_todos):
            return self.current_page_todos[self.selected - 1]

    async def on_mount(self):
        self.api = self.app.api  # type: ignore
        # await self.api.fetch_todos()
        grid = self.grid
        grid.set_align('center', 'center')
        grid.add_column(name='main_column', max_size=25, repeat=4)
        grid.add_row(name='tabs', fraction=2, max_size=1)
        grid.add_row(name='pagination', fraction=2, max_size=1)
        grid.add_row(name='todo_list', fraction=1, max_size=15, min_size=15)
        grid.add_row(name='controls', fraction=1, max_size=1)
        grid.add_areas(
            current_button=f'main_column1-start|main_column2-end,tabs',
            planning_button=f'main_column3-start|main_column4-end,tabs',
            show_hide_completed=f'main_column1-start|main_column2-end,pagination',
            pagination=f'main_column3-start|main_column4-end,pagination',
            todo_list=f'main_column1-start|main_column4-end,todo_list',
            done=f'main_column1,controls',
            edit=f'main_column2,controls',
            remove=f'main_column3,controls',
            create=f'main_column4,controls',
        )
        self.current_button = widgets.Button(
            'c[b]u[/b]rrent', style='')
        self.planning_button = widgets.Button(
            '[underline]planning[/underline]', style='')
        self.done_button = widgets.Button(
            '[underline][bold]d[/bold]one[/underline] selected',
            name='done',
            style='')
        self.edit_button = widgets.Button(
            '[underline][bold]e[/bold]dit[/underline] selected',
            name='edit',
            style='')
        self.remove_button = widgets.Button(
            '[underline][bold]r[/bold]emove[/underline] selected',
            name='remove',
            style='')
        self.create_button = widgets.Button(
            '[underline][bold]c[/bold]reate new todo[/underline]',
            name='create',
            style='')
        self.todo_list = components.TodoList(**self.todo_list_kwargs)
        self.pagination = widgets.Static(**self.pagination_kwargs)
        self.show_hide_completed = widgets.Static(
            **self.show_hide_completed_kwargs)
        grid.place(
            current_button=self.current_button,
            planning_button=self.planning_button,
            show_hide_completed=self.show_hide_completed,
            todo_list=self.todo_list,
            pagination=self.pagination,
            done=self.done_button,
            edit=self.edit_button,
            remove=self.remove_button,
            create=self.create_button,
        )

    @property
    def current_page_todos(self):
        return self.app.api.todos[(
            self.current_page - 1) * self.PAGE_SIZE:self.current_page * self.PAGE_SIZE]

    @property
    def todo_list_kwargs(self):
        return {'todos': self.current_page_todos, 'selected': self.selected}

    @property
    def show_hide_completed_kwargs(self):
        return {
            'renderable': f"[underline]{'[b]h[/b]ide' if self.show_completed else 's[b]h[/b]ow'}[/underline] completed"}

    @property
    def pagination_kwargs(self):
        return {
            'renderable': Text(
                f"Page {self.current_page} of {self.total_pages}",
                justify='left')}

    async def on_u(self):
        self.app.switch_view('CurrentView')

    async def on_q(self):
        await self.app.action_quit()

    async def on_h(self):
        self.show_completed = not self.show_completed
        await self.refresh_data()

    async def on_up(self):
        if self.selected - 1 > 0 and len(self.current_page_todos):
            self.selected -= 1
            self.update_kwargs()

    async def on_down(self):
        if self.selected + 1 <= len(self.current_page_todos):
            self.selected += 1
            self.update_kwargs()

    async def on_right(self):
        if self.current_page != self.total_pages:
            self.current_page += 1
            self.selected = 1
            self.update_kwargs()

    async def on_left(self):
        if self.current_page - 1 > 0:
            self.current_page -= 1
            self.selected = 1
            self.update_kwargs()

    def update_kwargs(self):
        for k, v in self.todo_list_kwargs.items():
            setattr(self.todo_list, k, v)
        self.todo_list.refresh()
        for k, v in self.show_hide_completed_kwargs.items():
            setattr(self.show_hide_completed, k, v)
        self.show_hide_completed.refresh()
        for k, v in self.pagination_kwargs.items():
            setattr(self.pagination, k, v)
        self.pagination.refresh()

    async def refresh_data(self):
        await self.api.fetch_todos(completed=self.show_completed)
        self.update_kwargs()

    async def watch_visible(self, val: bool):
        if val:
            self.page = 1
            self.selected = 1
            await self.refresh_data()

    async def on_c(self):
        self.app.switch_view('CreateTodoView')

    async def on_d(self):
        todo = self.selected_todo
        if todo:
            await self.app.api.done_todo(str(todo.id))
            await self.refresh_data()

    async def on_e(self):
        todo = self.selected_todo
        if todo:
            self.app.todo_to_update = todo
            self.app.switch_view('EditTodoView')

    async def on_r(self):
        todo = self.selected_todo
        if todo:
            await self.app.api.delete_todo(str(todo.id))
            await self.refresh_data()
