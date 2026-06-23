"""Picker window for the "Run World Tests" launcher component; selecting a world runs its tests scoped via AP_TEST_WORLDS."""
import os
import subprocess
import sys
import threading


def main() -> None:
    from worlds import AutoWorldRegister

    folders = {}
    for game, world_type in AutoWorldRegister.world_types.items():
        path = getattr(world_type, "__file__", None)
        if path:
            folders[game] = os.path.split(os.path.dirname(path))[1]

    from kvui import ThemedApp, ScrollBox  # must precede any kivy import
    from kivy.clock import Clock
    from kivy.uix.textinput import TextInput
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.button import MDButton, MDButtonText
    from kivymd.uix.label import MDLabel
    from kivymd.uix.screen import MDScreen
    from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldLeadingIcon

    class PickerApp(ThemedApp):
        def build(self):
            self.set_colors()
            self.title = "Run World Tests"
            screen = MDScreen(md_bg_color=self.theme_cls.backgroundColor)
            self.container = MDBoxLayout(orientation="vertical", padding="12dp", spacing="8dp")
            screen.add_widget(self.container)
            self.show_picker()
            return screen

        def show_picker(self):
            self.container.clear_widgets()
            search = MDTextField(MDTextFieldLeadingIcon(icon="magnify"),
                                 MDTextFieldHintText(text="Search worlds"), mode="outlined")
            scroll = ScrollBox()
            scroll.box_height = 0
            scroll.layout.padding = ["12dp", 0, "12dp", 0]
            search.bind(text=lambda _instance, value: self.populate(scroll, value))
            self.container.add_widget(search)
            self.container.add_widget(scroll)
            self.populate(scroll, "")

        def populate(self, scroll, needle):
            scroll.layout.clear_widgets()
            needle = needle.lower()
            for game in sorted(folders):
                if needle in game.lower():
                    button = MDButton(MDButtonText(text=game, pos_hint={"x": 0, "center_y": 0.5}),
                                      style="text", theme_width="Custom",
                                      size_hint_x=1, size_hint_y=None, height="48dp")
                    button.bind(on_release=lambda _b, chosen=game: self.run_tests(chosen))
                    scroll.layout.add_widget(button)

        def run_tests(self, game):
            self.container.clear_widgets()
            self.status = MDLabel(text=f"Running generic test suite for {game}…",
                                  adaptive_height=True)
            self.output = TextInput(readonly=True, font_name="RobotoMono-Regular",
                                    background_color=(0.11, 0.12, 0.14, 1),
                                    foreground_color=(0.86, 0.87, 0.89, 1),
                                    cursor_color=(0.86, 0.87, 0.89, 1),
                                    selection_color=(0.3, 0.5, 0.8, 0.4))
            back = MDButton(MDButtonText(text="Back"), style="text")
            back.bind(on_release=lambda _b: self.show_picker())
            self.container.add_widget(self.status)
            self.container.add_widget(self.output)
            self.container.add_widget(back)
            threading.Thread(target=self._worker, args=(game, folders[game]), daemon=True).start()

        def _worker(self, game, folder):
            env = os.environ.copy()
            env["AP_TEST_WORLDS"] = folder
            targets = [os.path.join("test", "general")]
            world_tests = os.path.join("worlds", folder, "test")
            if os.path.isdir(world_tests):
                targets.append(world_tests)
            proc = subprocess.Popen([sys.executable, "-m", "pytest", *targets, "-q"],
                                    env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, bufsize=1)
            for line in proc.stdout:
                Clock.schedule_once(lambda _dt, text=line: self._append(text))
            code = proc.wait()
            result = f"Tests passed for {game}." if code == 0 else f"Tests failed for {game} (exit {code})."
            Clock.schedule_once(lambda _dt: setattr(self.status, "text", result))

        def _append(self, text):
            self.output.text += text

    PickerApp().run()


if __name__ == "__main__":
    main()
