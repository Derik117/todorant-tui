import datetime as dt
from typing import Any, Optional

from textual.reactive import Reactive

from .text_input import TextInput


class YearMonthInput(TextInput):
    is_correct = Reactive(True)

    def __init__(
            self,
            *,
            allow_none=True,
            name: Optional[str] = None,
            value: str = "",
            placeholder: str = "",
            title: str = "",
            password: bool = False,
            syntax: Optional[str] = None,
            **kwargs: Any) -> None:
        super().__init__(
            name=name,
            value=value,
            placeholder=placeholder,
            title=title,
            password=password,
            syntax=syntax,
            **kwargs)
        self.original_title = title
        self.allow_none = allow_none
        self.update_title()

    def watch_value(self, val: str):
        self.is_correct = False
        if len(val) > 7:
            self.value = self.value[:7]
            self._cursor_position = self._cursor_position - 1
        if len(val) == 7 and val.count('-') == 1:
            try:
                dt.datetime.strptime(val + '-01', '%Y-%m-%d')
                self.is_correct = True
            except ValueError:
                ...
        if self.allow_none and len(val) == 0:
            self.is_correct = True
        self.update_title()

    def update_title(self):
        status = f"[bold][{'OK' if self.is_correct else 'ERR'}][/bold]"
        if self.original_title:
            status += ' '
        self.title = f"{status}{self.original_title}"
        self.refresh()
