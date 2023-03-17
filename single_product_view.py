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
import tkinter.messagebox
from configparser import ConfigParser
from tkinter import END

import pygubu

from db_functions import DataRetrieve, DataDelete, DataWrite

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "single_product_view.ui"


class SingleProductView:
    def __init__(self, code=None, function=None, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("new_product_window", master)

        self.function = function

        self.codevar = None
        self.namevar = None
        self.qtyvar = None
        self.unitvar = None
        self.taxvar = None
        builder.import_variables(
            self, ['codevar', 'namevar', 'qtyvar', 'unitvar', 'taxvar'])

        builder.connect_callbacks(self)
        self.history_tv = builder.get_object("history_tv")
        self.cod_entry = builder.get_object("cod_entry")
        self.cat_combo = builder.get_object("cat_combo")
        self.product_entry = builder.get_object("product_entry")
        self.ean_entry = builder.get_object("ean_entry")
        self.unit_entry = builder.get_object("unit_entry")
        self.qty_entry = builder.get_object("qty_entry")
        self.unit_price_entry = builder.get_object("unit_price_entry")
        self.discount1_entry = builder.get_object("discount1_entry")
        self.discount2_entry = builder.get_object("discount2_entry")
        self.iva_entry = builder.get_object("iva_entry")
        self.selling_entry = builder.get_object("selling_entry")
        self.mainwindow.focus_set()

        self.on_load(code)

    def run(self):
        self.mainwindow.mainloop()

    def on_load(self, code):
        cat = []
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}cat.dat"
        with open(filename, "r") as file:
            categories = file.readlines()
            for category in categories:
                category = category.split(",")
                cat.append(category[1][:-1])
        self.cat_combo.configure(values=cat)
        product = DataRetrieve().single_product_code_NOLIST(code)
        product = product[0]
        self.cod_entry.insert(0, product[0])
        self.cod_entry.configure(state="readonly")
        self.cat_combo.insert(0, product[1])
        self.cat_combo.configure(state="readonly")
        self.product_entry.insert(0, product[2])
        self.ean_entry.insert(0, product[3])
        self.unit_entry.insert(0, product[4])
        self.qty_entry.delete(0, END)
        self.qty_entry.insert(0, product[5])
        self.unit_price_entry.insert(0, product[6])
        self.discount1_entry.insert(0, product[7])
        self.discount2_entry.insert(0, product[8])
        self.selling_entry.insert(0, product[9])
        self.selling_entry.configure(bootstyle="success")
        self.iva_entry.insert(0, product[10])
        history = product[11]
        history = history.split(";")
        for line in history[:-1]:
            line = line.split(",")
            self.history_tv.insert("", 0, values=line)

    def on_delete_press(self):
        code = self.cod_entry.get()
        ask = tkinter.messagebox.askyesno(parent=self.mainwindow, title="Eliminare prodotto?",
                                          message=f"Vuoi davvero eliminare il prodotto {code}?")
        if ask:
            DataDelete().delete_product(code)
            self.function()
            self.mainwindow.destroy()

    def on_clear_press(self):
        self.cod_entry.delete(0, END)
        self.cat_combo.delete(0, END)
        self.product_entry.delete(0, END)
        self.ean_entry.delete(0, END)
        self.unit_entry.delete(0, END)
        self.qty_entry.delete(0, END)
        self.unit_price_entry.delete(0, END)
        self.discount1_entry.delete(0, END)
        self.discount2_entry.delete(0, END)
        self.selling_entry.delete(0, END)
        self.iva_entry.delete(0, END)

    def on_update_press(self):
        code = self.cod_entry.get()
        category = self.cat_combo.get()
        product = self.product_entry.get()
        ean = self.ean_entry.get()
        unit = self.unit_entry.get()
        qty = self.qty_entry.get()
        price = self.unit_price_entry.get()
        discount1 = self.discount1_entry.get()
        discount2 = self.discount2_entry.get()
        selling = self.selling_entry.get()
        iva = self.iva_entry.get()
        buffer = ""
        for child in self.history_tv.get_children():
            value = self.history_tv.item(child)["values"]
            value = f"{value[0]},{value[1]},{value[2]};"
            buffer = buffer + value
        DataWrite().update_product(code, category, product, ean, unit, qty, price, discount1, discount2, selling, iva,
                                   buffer)
        self.function()
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = SingleProductView()
    app.run()
