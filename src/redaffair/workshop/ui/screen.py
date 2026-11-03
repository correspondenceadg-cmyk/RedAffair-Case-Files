from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from ...case import flavor

class WorkshopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        header = Label(text="Case Workshop", font_size='30sp', color=(1, 0, 0, 1), size_hint_y=None, height=80)
        layout.add_widget(header)
        
        btn_flavor = Button(text="Flavor Editor", font_size='24sp', background_color=(0.2, 0, 0, 1), size_hint_y=None, height=100)
        btn_flavor.bind(on_press=self._open_flavor)
        layout.add_widget(btn_flavor)

        btn_back = Button(text="Back to Menu", font_size='24sp', background_color=(0.2, 0, 0, 1), size_hint_y=None, height=100)
        btn_back.bind(on_press=self._go_back)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _open_flavor(self, instance):
        self.manager.current = 'flavoredit'

    def _go_back(self, instance):
        self.manager.current = 'menu'

class FlavorEditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_flavor = dict(flavor.FLAVOR)
        self.inputs = {}
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.header = Label(text="Flavor Editor (0%)", font_size='24sp', color=(1, 0, 0, 1), size_hint_y=None, height=50)
        layout.add_widget(self.header)

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        form_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        for key, val in self.original_flavor.items():
            lbl = Label(text=key, font_size='16sp', color=(1, 0, 0, 1), size_hint_y=None, height=30)
            form_layout.add_widget(lbl)
            
            txt = TextInput(text=val, multiline=True, size_hint_y=None, height=80, background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1))
            if val == self.original_flavor[key]:
                txt.background_color = (0.2, 0.2, 0, 1)
                txt.text = f"[FLAVOR] {val}"
                
            txt.bind(text=lambda instance, value, k=key: self._on_edit(k, instance, value))
            form_layout.add_widget(txt)
            self.inputs[key] = txt

        scroll.add_widget(form_layout)
        layout.add_widget(scroll)

        btn_save = Button(text="Save Changes", font_size='24sp', background_color=(0.2, 0, 0, 1), size_hint_y=None, height=80)
        btn_save.bind(on_press=self._save)
        layout.add_widget(btn_save)

        btn_back = Button(text="Back to Workshop", font_size='24sp', background_color=(0.2, 0, 0, 1), size_hint_y=None, height=80)
        btn_back.bind(on_press=self._go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _on_edit(self, key, instance, value):
        if value.startswith("[FLAVOR] "):
            value = value[9:]
        
        edited_count = 0
        for k, original in self.original_flavor.items():
            current = self.inputs[k].text
            if current.startswith("[FLAVOR] "):
                current = current[9:]
            if current != original:
                edited_count += 1
                
        total = len(self.original_flavor)
        pct = int((edited_count / total) * 100) if total > 0 else 0
        self.header.text = f"Flavor Editor ({pct}%)"

    def _save(self, instance):
        for k, txt in self.inputs.items():
            val = txt.text
            if val.startswith("[FLAVOR] "):
                val = val[9:]
            flavor.FLAVOR[k] = val
        self.header.text = "Flavor Editor (Saved!)"

    def _go_back(self, instance):
        self.manager.current = 'workshop'
