from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

LEATHER = (0.10, 0.04, 0.02, 1)
AMBER = (0.85, 0.65, 0.30, 1)
PAPER = (0.90, 0.85, 0.72, 1)

class RevealScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20), size_hint=(0.9, 0.85), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        with self.layout.canvas.before:
            Color(*LEATHER)
            self.bg = Rectangle(pos=self.layout.pos, size=self.layout.size)
            Color(0.30, 0.22, 0.12, 1)
            self.page = Rectangle(pos=(self.layout.pos[0]+dp(10), self.layout.pos[1]+dp(10)), size=(self.layout.size[0]-dp(20), self.layout.size[1]-dp(20)))
            
        self.layout.bind(size=self._update_rects, pos=self._update_rects)
        self.add_widget(self.layout)
        
        self.layout.add_widget(Widget(size_hint=(1, 0.15)))
        
        self.prose_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.2), spacing=dp(1))
        self.layout.add_widget(self.prose_box)
        
        self.mech_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.2), spacing=dp(1))
        self.layout.add_widget(self.mech_box)
        
        self.layout.add_widget(Widget(size_hint=(1, 0.2)))
        
        self.continue_btn = Button(text="Return to Flock", size_hint=(None, None), size=(dp(200), dp(50)), pos_hint={'center_x': 0.5}, opacity=0, background_color=(0.2, 0.15, 0.1, 1))
        self.continue_btn.bind(on_release=self._finish)
        self.layout.add_widget(self.continue_btn)

    def _update_rects(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size
        self.page.pos = (self.layout.pos[0]+dp(10), self.layout.pos[1]+dp(10))
        self.page.size = (self.layout.size[0]-dp(20), self.layout.size[1]-dp(20))

    def play_animation(self, doctrine, on_complete_callback):
        self.on_complete_callback = on_complete_callback
        self.prose_box.clear_widgets()
        self.mech_box.clear_widgets()
        
        prose_text = doctrine['verse']
        mech_text = f"{doctrine['verb']} {doctrine['action']} {doctrine['object']} ({doctrine['condition']})"
        
        self.prose_labels = []
        self.mech_labels = []

        for char in prose_text:
            lbl = Label(text=char, font_size="16sp", size_hint=(None, 1), width=dp(12), 
                        color=(1, 0, 0, 1), outline_color=(1, 0, 0, 1), outline_width=6, opacity=0)
            self.prose_box.add_widget(lbl)
            self.prose_labels.append(lbl)

        for char in mech_text:
            lbl = Label(text=char, font_size="18sp", size_hint=(None, 1), width=dp(14), 
                        color=(1, 0, 0, 1), outline_color=(1, 0, 0, 1), outline_width=8, opacity=0, bold=True)
            self.mech_box.add_widget(lbl)
            self.mech_labels.append(lbl)

        self.continue_btn.opacity = 0
        self.continue_btn.disabled = True
        
        self.delay = 0.15 
        Clock.schedule_once(lambda dt: self._reveal_next(0, 0), 0.5)

    def _reveal_next(self, p_idx, m_idx):
        if p_idx < len(self.prose_labels):
            lbl = self.prose_labels[p_idx]
            lbl.opacity = 1
            
            anim_y = Animation(y=dp(10), duration=0.1, t='out_quad') + Animation(y=0, duration=0.2, t='in_quad')
            anim_y.start(lbl)
            
            anim_c = Animation(color=(0.1, 0.05, 0.02, 1), outline_width=0, duration=0.8)
            anim_c.start(lbl)
            
            Clock.schedule_once(lambda dt: self._reveal_next(p_idx + 1, m_idx), self.delay)
            
        elif m_idx < len(self.mech_labels):
            lbl = self.mech_labels[m_idx]
            lbl.opacity = 1
            
            anim_y = Animation(y=dp(15), duration=0.1, t='out_quad') + Animation(y=0, duration=0.2, t='in_quad')
            anim_y.start(lbl)
            
            anim_c = Animation(color=AMBER, outline_width=4, duration=0.8)
            anim_c.start(lbl)
            
            Clock.schedule_once(lambda dt: self._reveal_next(p_idx, m_idx + 1), self.delay)
            
        else:
            self._show_button()

    def _show_button(self):
        anim = Animation(opacity=1, duration=1.0)
        anim.start(self.continue_btn)
        self.continue_btn.disabled = False

    def _finish(self, instance):
        self.continue_btn.disabled = True
        self.on_complete_callback()
        self.manager.current = "main"
