from typing import TYPE_CHECKING

from textual import log, widgets
from textual.views import GridView  # type: ignore

from todorant_tui import components

if TYPE_CHECKING:
    from todorant_tui.app import TodorantApp


class CurrentView(GridView):
    app: 'TodorantApp'

    async def on_mount(self):
        self.api = self.app.api  # type: ignore
        grid = self.grid
        grid.set_align('center', 'center')
        grid.add_column(name='main_column', max_size=25, repeat=4)
        grid.add_row(name='tabs', fraction=2, max_size=1)
        grid.add_row(name='progress', fraction=1, max_size=2, min_size=2)
        grid.add_row(name='current_task', fraction=8, max_size=14)
        grid.add_row(name='buttons', fraction=1, max_size=1, min_size=1)
        grid.add_areas(
            current_button=f'main_column1-start|main_column2-end,tabs',
            planning_button=f'main_column3-start|main_column4-end,tabs',
            area1=f'main_column1-start|main_column4-end,progress',
            area2=f'main_column1-start|main_column4-end,current_task',
            area30=f'main_column1,buttons',
            area31=f'main_column2,buttons',
            area32=f'main_column3,buttons',
            area33=f'main_column4,buttons',
        )
        self.current_button = widgets.Button(
            '[underline]current[/underline]', style='')
        self.planning_button = widgets.Button('[b]p[/b]lanning', style='')
        self.done_button = widgets.Button(
            '[underline][bold]d[/bold]one[/underline]', name='done', style='')
        self.edit_button = widgets.Button(
            '[underline][bold]e[/bold]dit[/underline]', name='edit', style='')
        self.remove_button = widgets.Button(
            '[underline][bold]r[/bold]emove[/underline]', name='remove', style='')
        self.create_button = widgets.Button(
            '[underline][bold]c[/bold]reate new todo[/underline]',
            name='create',
            style='')
        self.progress = components.Progress(**self.progress_kwargs)
        self.current_task = components.CurrentTask(**self.current_task_kwargs)
        grid.place(
            current_button=self.current_button,
            planning_button=self.planning_button,
            area1=self.progress,
            area2=self.current_task,
            area30=self.done_button,
            area31=self.edit_button,
            area32=self.remove_button,
            area33=self.create_button,
        )

    @property
    def progress_kwargs(self):
        return {
            'current': self.api.current.todos_count - self.api.current.incomplete_todos_count,
            'total': self.api.current.todos_count}

    @property
    def current_task_kwargs(self):
        return {'todo': self.api.current.todo}

    def update_kwargs(self):
        for k, v in self.progress_kwargs.items():
            setattr(self.progress, k, v)
            self.progress.refresh()
        for k, v in self.current_task_kwargs.items():
            setattr(self.current_task, k, v)
            self.current_task.refresh()

    async def refresh_data(self):
        await self.api.fetch_current()
        self.update_kwargs()

    async def watch_visible(self, val):
        if val:
            await self.refresh_data()

    async def on_c(self):
        self.app.switch_view('CreateTodoView')

    async def on_r(self):
        todo = self.api.current.todo
        if todo and todo.id:
            await self.api.delete_todo(todo.id)
            await self.refresh_data()

    async def on_d(self):
        todo = self.api.current.todo
        if todo and todo.id:
            await self.api.done_todo(todo.id)
            await self.refresh_data()

    async def on_q(self):
        await self.app.action_quit()

    async def on_e(self):
        self.app.todo_to_update = self.api.current.todo
        self.app.switch_view('EditTodoView')

    async def on_p(self):
        self.app.switch_view('PlanningView')
