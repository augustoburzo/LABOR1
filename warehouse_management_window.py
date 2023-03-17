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
import tkinter
from tkinter import END, messagebox

import pygubu

from db_functions import DataRetrieve
from single_product_view import SingleProductView

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "warehouse_management_window.ui"


class WarehouseManagementWindow:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object(
            "warehouse_management_window", master)
        builder.connect_callbacks(self)
        self.mainwindow.focus_set()

        self.warehouse_tv = builder.get_object("warehouse_tv")
        self.warehouse_tv.bind("<Double-1>", self.on_click)
        self.product_code_entry = builder.get_object("product_code_entry")
        self.product_name_entry = builder.get_object("product_name_entry")
        self.product_code_entry.bind("<Return>", self.on_code_return)
        self.product_code_entry.bind("<FocusIn>", self.focus_in1)
        self.product_name_entry.bind("<Return>", self.on_name_return)
        self.product_name_entry.bind("<FocusIn>", self.focus_in2)

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def on_click(self, event=None):
        product_idx = "0"
        item = self.warehouse_tv.selection()
        for i in item:
            product_idx = self.warehouse_tv.item(i, "values")[0]
        SingleProductView(master=self.mainwindow, code=product_idx, function=self.on_load).mainwindow.grab_set()

    def focus_in1(self, event):
        self.product_name_entry.delete(0, END)

    def focus_in2(self, event):
        self.product_code_entry.delete(0, END)

    def on_load(self):
        self.warehouse_tv.delete(*self.warehouse_tv.get_children())
        warehouse = DataRetrieve().warehouse_status()
        for product in warehouse:
            self.warehouse_tv.insert("", END, values=product)

    def on_code_return(self, event=None):
        self.warehouse_tv.delete(*self.warehouse_tv.get_children())
        code = self.product_code_entry.get()
        products = DataRetrieve().single_product_code(code)
        for product in products:
            self.warehouse_tv.insert("", END, values=product)

    def on_name_return(self, event=None):
        self.warehouse_tv.delete(*self.warehouse_tv.get_children())
        name = self.product_name_entry.get()
        products = DataRetrieve().single_product_name(name)
        for product in products:
            self.warehouse_tv.insert("", END, values=product)

    def on_search_btn_press(self):
        code = self.product_code_entry.get()
        name = self.product_name_entry.get()
        if code == "" and name != "":
            self.on_name_return()
        elif code != "" and name == "":
            self.on_code_return()


if __name__ == "__main__":
    app = WarehouseManagementWindow()
    app.run()
