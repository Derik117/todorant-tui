from typing import TYPE_CHECKING

from rich.text import Text
from textual import log, widgets
from textual.views import GridView  # type: ignore

from todorant_tui import components, models

if TYPE_CHECKING:
    from todorant_tui.app import TodorantApp


class CreateTodoView(GridView):
    app: 'TodorantApp'
    title: str = 'Create new todo'
    save_or_update_button_text: str = '[underline][b]c[/b]reate[/underline]'

    async def on_mount(self):
        self.text = components.TextInput(
            title="Task [bold]t[/bold]ext", placeholder=' ')
        self.date = components.DateInput(
            title="Task [b]d[/b]ate (YYYY-MM-DD)",
            placeholder="Enter task date in format YYYY-MM-DD",
            value=str(
                self.app.api.date))  # type: ignore
        self.year_and_month = components.YearMonthInput(
            title="[b]or[/b] task year and [b]m[/b]onth (YYYY-MM)",
            placeholder="Enter task year and month in format YYYY-MM")
        self.is_frog = components.BoolInput(
            title="[b]f[/b]rog", value=str(False))
        self.is_completed = components.BoolInput(
            title="C[b]o[/b]mpleted", value=str(False))
        self.grid.set_align('center', 'center')
        self.grid.add_column("col1", max_size=25)
        self.grid.add_column("col2", max_size=25)
        self.grid.add_column("col3", max_size=25)
        self.grid.add_column("col4", max_size=25)
        self.grid.add_row("title", max_size=3)
        self.grid.add_row('text', max_size=3)
        self.grid.add_row('others', max_size=3)
        self.grid.add_row('buttons', max_size=3)
        self.grid.add_areas(
            title='col1-start|col4-end,title',
            text='col1-start|col4-end,text',
            date='col1-start|col2-end,others',
            year_month='col3-start|col4-end,others',
            frog='col1,buttons',
            completed='col2,buttons',
            back_button='col3,buttons',
            create_button='col4,buttons',
        )
        self.grid.add_widget(widgets.Static(
            Text(self.title, justify='center', style='bold')), area='title')
        self.grid.add_widget(self.text, area='text')
        self.grid.add_widget(self.date, area='date')
        self.grid.add_widget(self.year_and_month, area='year_month')
        self.grid.add_widget(self.is_frog, area='frog')
        self.grid.add_widget(self.is_completed, area='completed')
        self.grid.add_widget(
            widgets.Static(
                widgets.Button(
                    '[underline][b]b[/b]ack[/underline]',
                    style='red')),
            area='back_button')
        self.grid.add_widget(
            widgets.Static(
                widgets.Button(
                    self.save_or_update_button_text,
                    style='green')),
            area='create_button')

    async def watch_visible(self, val: bool):
        log("SHOW", val)
        if val:
            self.reset_inputs()
            self.refresh()

    def reset_inputs(self):
        self.text.value = ''
        self.date.value = str(self.app.api.date)
        self.year_and_month.value = ''
        self.is_frog.value = 'False'
        self.is_completed.value = 'False'

    async def create_todo(self):
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
        todo = models.TodoCreate(text=text,
                                 completed=self.is_completed.bool_value,
                                 frog=self.is_frog.bool_value,
                                 monthAndYear=month_and_year,
                                 date=date)
        await self.app.api.create_todo(todo)
        self.app.switch_to_previous_view()

    async def on_t(self):
        await self.app.set_focus(self.text)

    async def on_d(self):
        await self.app.set_focus(self.date)

    async def on_y(self):
        await self.app.set_focus(self.year_and_month)

    async def on_f(self):
        self.is_frog.toggle()

    async def on_o(self):
        self.is_completed.toggle()

    async def on_c(self):
        await self.create_todo()

    async def on_b(self):
        self.app.switch_to_previous_view()
