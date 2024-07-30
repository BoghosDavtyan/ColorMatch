from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
import random

class ColorDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.target_color = [0, 0, 0]
        self.current_color = [0, 0, 0]
        self.bind(size=self.update_rect, pos=self.update_rect)

        with self.canvas:
            self.target_rect = Rectangle(pos=self.pos, size=(self.width/2, self.height))
            self.current_rect = Rectangle(pos=(self.width/2, self.y), size=(self.width/2, self.height))

    def update_rect(self, *args):
        self.target_rect.pos = self.pos
        self.target_rect.size = (self.width/2, self.height)
        self.current_rect.pos = (self.x + self.width/2, self.y)
        self.current_rect.size = (self.width/2, self.height)

    def update_colors(self, target_color, current_color):
        self.target_color = target_color
        self.current_color = current_color
        self.canvas.clear()
        with self.canvas:
            Color(*[x/255 for x in self.target_color])
            self.target_rect = Rectangle(pos=self.pos, size=(self.width/2, self.height))
            Color(*[x/255 for x in self.current_color])
            self.current_rect = Rectangle(pos=(self.x + self.width/2, self.y), size=(self.width/2, self.height))

class ColorMixingGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.target_color = [0, 0, 0]
        self.current_color = [0, 0, 0]

        self.color_display = ColorDisplay(size_hint=(1, 0.3))
        self.add_widget(self.color_display)

        self.target_label = Label(text="Match the color!", size_hint=(1, 0.1))
        self.add_widget(self.target_label)

        self.sliders = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        self.red_slider = Slider(min=0, max=255, value=0)
        self.green_slider = Slider(min=0, max=255, value=0)
        self.blue_slider = Slider(min=0, max=255, value=0)

        for slider, color in zip([self.red_slider, self.green_slider, self.blue_slider], ['Red', 'Green', 'Blue']):
            slider_layout = BoxLayout()
            slider_layout.add_widget(Label(text=color, size_hint=(0.2, 1)))
            slider_layout.add_widget(slider)
            self.sliders.add_widget(slider_layout)
            slider.bind(value=self.on_slider_change)

        self.add_widget(self.sliders)

        self.start_button = Button(text="Start", size_hint=(1, 0.1))
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)

        self.submit_button = Button(text="Submit", size_hint=(1, 0.1))
        self.submit_button.bind(on_press=self.check_color)
        self.add_widget(self.submit_button)

        self.result_label = Label(text="", size_hint=(1, 0.1))
        self.add_widget(self.result_label)

        Clock.schedule_once(self.update_color_display, 0)

    def on_slider_change(self, instance, value):
        self.current_color = [int(self.red_slider.value), int(self.green_slider.value), int(self.blue_slider.value)]
        self.update_color_display()

    def update_color_display(self, *args):
        self.color_display.update_colors(self.target_color, self.current_color)

    def start_game(self, instance):
        self.target_color = [random.randint(0, 255) for _ in range(3)]
        self.update_color_display()
        self.result_label.text = "Try to match the color on the left!"

    def check_color(self, instance):
        diff = sum(abs(t - c) for t, c in zip(self.target_color, self.current_color))
        max_diff = 255 * 3
        similarity = (1 - diff / max_diff) * 100
        self.result_label.text = f"Your match is {similarity:.2f}% accurate!"

class ColorMixingApp(App):
    def build(self):
        return ColorMixingGame()

if __name__ == '__main__':
    Window.size = (400, 600)
    ColorMixingApp().run()