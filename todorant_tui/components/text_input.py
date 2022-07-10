import textual_inputs
from textual import events


class TextInput(textual_inputs.TextInput):

    async def on_key(self, event: events.Key) -> None:
        if event.key == 'escape':
            await self.app.set_focus(None)
        elif event.key == 'enter':
            await self.app.set_focus(None)

    async def on_focus(self, event: events.Focus) -> None:
        self._cursor_position = len(self.value)
        return await super().on_focus(event)
