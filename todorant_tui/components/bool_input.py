from textual.reactive import Reactive

from .text_input import TextInput


class BoolInput(TextInput):
    is_correct = Reactive(True)

    async def on_focus(self, _) -> None:
        self.toggle()
        await self.app.set_focus(None)

    def toggle(self):
        if self.value.lower() == 'true':
            self.value = 'False'
        elif self.value.lower() == 'false':
            self.value = 'True'

    @property
    def bool_value(self) -> bool:
        return self.value.lower() == 'true'
