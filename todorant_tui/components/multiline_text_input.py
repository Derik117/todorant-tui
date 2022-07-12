from typing import Any, Optional, Union

import textual_inputs
from rich import box
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from textual import events, log

EOL_MOCK_CHAR = '∂'


class MultilineTextInput(textual_inputs.TextInput):
    def __init__(
            self,
            *,
            name: Optional[str] = None,
            value: str = "",
            placeholder: str = "",
            title: str = "",
            password: bool = False,
            syntax: Optional[str] = None,
            lines_count: int = 1,
            **kwargs: Any) -> None:
        super().__init__(
            name=name,
            value=value,
            placeholder=placeholder,
            title=title,
            password=password,
            syntax=syntax,
            **kwargs)
        self.lines_count = lines_count

    async def on_focus(self, event: events.Focus) -> None:
        self._cursor_position = len(self.value)
        return await super().on_focus(event)

    def _modify_text(self, segment: str) -> Union[str, Text]:
        return super()._modify_text(segment.replace('\\n', '\n'))

    def render(self) -> RenderableType:
        """
        Produce a Panel object containing placeholder text or value
        and cursor.
        """
        if self.has_focus:
            segments = self._render_text_with_cursor()
        else:
            if len(self.value) == 0:
                if self.title and not self.placeholder:
                    segments = [self.title]
                else:
                    segments = [self.placeholder]
            else:
                segments = [self._modify_text(self.value)]

        text = Text.assemble(*segments)

        if (
            self.title
            and not self.placeholder
            and len(self.value) == 0
            and not self.has_focus
        ):
            title = ""
        else:
            title = self.title

        return Panel(
            text,
            title=title,
            title_align="left",
            height=self.lines_count + 2,
            style=self.style or "",
            border_style=self.border_style or Style(color="blue"),
            box=box.DOUBLE if self.has_focus else box.SQUARE,
        )

    def _cursor_up(self):
        """Handle key press Up"""
        lines = self.value.split('\n')
        # + 1 beacuse split remove invisible \n char
        lines_lengths = [len(line) + 1 for line in lines]
        lines_lengths_sum = [sum(lines_lengths[:line_index + 1])
                             for line_index in range(len(lines))]
        cursor_line_index = 0
        for i in range(len(lines)):
            if i == 0:
                continue
            if self._cursor_position + \
                    1 >= lines_lengths_sum[i - 1] and self._cursor_position + 1 <= lines_lengths_sum[i]:
                cursor_line_index = i
                break

        if cursor_line_index > 0:
            cursor_right_offset = self._cursor_position - \
                lines_lengths_sum[cursor_line_index - 1]
            prev_line_length = lines_lengths[cursor_line_index - 1]
            new_cursor_position = self._cursor_position - \
                cursor_right_offset - prev_line_length
            new_cursor_position += min([cursor_right_offset,
                                       prev_line_length - 1])
            self._cursor_position = new_cursor_position
            self._update_offset_right()

    def _cursor_down(self):
        lines = self.value.split('\n')
        # + 1 beacuse split remove invisible \n char
        lines_lengths = [len(line) + 1 for line in lines]
        lines_lengths_sum = [sum(lines_lengths[:line_index + 1])
                             for line_index in range(len(lines))]
        cursor_line_index = 0
        for i in range(len(lines)):
            if i == 0:
                continue
            if self._cursor_position + \
                    1 >= lines_lengths_sum[i - 1] and self._cursor_position + 1 <= lines_lengths_sum[i]:
                cursor_line_index = i
                break

        if cursor_line_index < len(lines) - 1:
            cursor_right_offset = self._cursor_position - \
                lines_lengths_sum[cursor_line_index - 1]
            curr_line_length = lines_lengths[cursor_line_index]
            next_line_length = lines_lengths[cursor_line_index - 1]
            new_cursor_position = self._cursor_position - cursor_right_offset + \
                curr_line_length + min([cursor_right_offset, next_line_length])
            self._cursor_position = new_cursor_position
            self._update_offset_right()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "up":
            self._cursor_up()
        elif event.key == "down":
            self._cursor_down()
        elif event.key == 'escape':
            await self.app.set_focus(None)
        elif event.key == 'enter':
            if self.lines_count > 1:
                chars = list(self.value.replace('\n', EOL_MOCK_CHAR))
                prev_symbol = chars[self._cursor_position -
                                    1] if self._cursor_position > 0 else None
                prev_prev_symbol = chars[self._cursor_position - \
                    2] if self._cursor_position > 1 else None
                if (prev_prev_symbol != '\n' and prev_symbol == '\n') or (
                        prev_prev_symbol == '\n' and prev_symbol == '\n'):
                    offset = 2
                else:
                    offset = 1
                chars.insert(self._cursor_position, '\n')
                self._cursor_position += offset
                self.value = ''.join(chars).replace(EOL_MOCK_CHAR, '\n')
            else:
                await self.app.set_focus(None)
        log(self._cursor_position)
