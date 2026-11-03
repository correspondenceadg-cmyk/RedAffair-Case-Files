from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from ..session import WorkshopSession
from ..scripts.playthrough import run_scripted

class WorkshopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = WorkshopSession()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.title = Label(text="Case Workshop", font_size='24sp', size_hint_y=None, height=50)
        layout.add_widget(self.title)
        
        self.seed_input = TextInput(text="1", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.seed_input)
        
        btn_gen = Button(text="Generate", size_hint_y=None, height=50)
        btn_gen.bind(on_press=self._on_generate)
        layout.add_widget(btn_gen)
        
        self.status = Label(text="Ready", size_hint_y=None, height=50)
        layout.add_widget(self.status)
        
        btn_back = Button(text="Back", size_hint_y=None, height=50)
        btn_back.bind(on_press=self._go_back)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def _on_generate(self, instance):
        try:
            seed = int(self.seed_input.text)
            draft = self.session.generate(seed)
            valid = run_scripted(draft)
            self.status.text = f"Generated seed {seed}. Killer: {draft.killer_key}. Valid: {valid}"
        except Exception as e:
            self.status.text = f"Error: {e}"

    def _go_back(self, instance):
        self.manager.current = 'menu'
