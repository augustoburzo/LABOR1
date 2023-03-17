#!/usr/bin/python3
import pathlib
import pygubu
import webbrowser
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "credits.ui"


class Credits:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("credits_window", master)
        builder.connect_callbacks(self)

        self.mainwindow.focus_set()

    def run(self):
        self.mainwindow.mainloop()

    def callback(self, event=None):
        webbrowser.open_new("https://icons8.com")


if __name__ == "__main__":
    app = Credits()
    app.run()
