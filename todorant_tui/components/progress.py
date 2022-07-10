from rich.console import Group, RenderableType
from rich.progress_bar import ProgressBar
from rich.text import Text
from textual.widget import Widget


class Progress(Widget):
    def __init__(self, current: int, total: int) -> None:
        super().__init__(name='progress')
        self.current = current
        self.total = total

    def render(self) -> RenderableType:
        return Group(
            Text(f"Progress {self.current} of {self.total}",
                 justify='center'),
            ProgressBar(total=self.total, completed=self.current,),
        )
