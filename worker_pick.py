#!/usr/bin/python3
########################################################################################################################
# Augusto Burzo - Labor1                                                                                               #
# Software gestionale ideato per centri riparazione e vendita di ricambi. Il software include (includerà) funzioni per #
# l'inserimento a sistema di Clienti, Fornitori, Documenti di acquisto e di vendita, Pratiche di assistenza.           #
#                                                                                                                      #
# Il progetto si pone come traguardo fondamentale la semplicità d'uso, l'aspetto gradevole e l'affidabilità, si è      #
# puntato di proposito sulla semplicità di codice e interfaccia. Si è scelto anche d'indicare per quasi ogni tasto     #
# del programma la sua funzione.                                                                                       #
########################################################################################################################

__author__ = "Augusto Burzo"
__copyright__ = "Copyright 2023 - Augusto Burzo"
__credits__ = ["Augusto Burzo"]
__license__ = "Proprietary"
__version__ = "1.2.0"
__maintainer__ = "Augusto Burzo"
__email__ = "info@augustoburzo.com"
__status__ = "Beta"

import pathlib
from configparser import ConfigParser
from tkinter import END

import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "worker_pick.ui"


class WorkerPick:
    def __init__(self, entry=None, validate=None, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.validate = validate
        self.entry = entry
        # Main widget
        self.mainwindow = builder.get_object("worker_pick", master)
        builder.connect_callbacks(self)

        self.work_tv = builder.get_object("work_tv")
        self.work_tv.bind("<Double-1>", self.on_select_press)

        self.mainwindow.focus_set()

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def on_load(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}workers.dat"
        with open(filename, "r") as file:
            works = file.readlines()
            for work in works:
                work = work.split(",")
                self.work_tv.insert("", 0, values=work)

    def on_select_press(self, event=None):
        item = self.work_tv.selection()
        for i in item:
            work_id = self.work_tv.item(i, "values")[0]
            work_name = self.work_tv.item(i, "values")[1][:-1]
            work_values = [work_id, work_name]
            self.entry.configure(state="normal")
            self.entry.delete(0, END)
            self.entry.insert(0, work_name)
            self.entry.configure(state="readonly")
            try:
                self.validate()
            except TypeError:
                pass
            self.mainwindow.destroy()


if __name__ == "__main__":
    app = WorkerPick()
    app.run()
