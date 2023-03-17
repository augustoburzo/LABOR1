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
import datetime
from tkinter import END

import pygubu

from customer_pick import CustomerPick
from customer_view import CustomerView
from db_functions import DataRetrieve, DataWrite

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "order_insert_window.ui"


class OrderInsertWindow:
    def __init__(self, code="", last_name="", first_name="", cellphone="", master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("order_insert_window", master)
        builder.connect_callbacks(self)

        self.mainwindow.state('zoomed')

        # Attivazione entry anagrafica cliente
        self.customer_cod_entry = builder.get_object("customer_cod_entry")
        self.customer_cod_entry.configure(state="enabled")
        self.customer_cod_entry.insert(0, code)
        self.customer_cod_entry.configure(state="readonly")

        self.customer_lastname_entry = builder.get_object("customer_lastname_entry")
        self.customer_lastname_entry.insert(0, last_name)
        self.customer_lastname_entry.bind("<Return>", self.on_return)
        self.customer_lastname_entry.focus_set()
        if last_name != '':
            self.customer_lastname_entry.configure(state="readonly")

        self.customer_firstname_entry = builder.get_object("customer_firstname_entry")
        self.customer_firstname_entry.insert(0, first_name)
        if first_name != '':
            self.customer_firstname_entry.configure(state="readonly")

        self.customer_phone_entry = builder.get_object("customer_phone_entry")
        self.customer_phone_entry.insert(0, cellphone)
        if cellphone != '':
            self.customer_phone_entry.configure(state="readonly")

        # Attivazione entry anagrafica prodotto
        self.product_name_entry = builder.get_object("product_name_entry")
        self.serial_number_entry = builder.get_object("serial_number_entry")
        self.malfunction_txt = builder.get_object("malfunction_txt")
        if first_name != '':
            self.product_name_entry.focus_set()

    def run(self):
        self.mainwindow.mainloop()

    def on_return(self, event):
        self.on_search_btn_press()

    def on_search_btn_press(self):
        lastname = self.customer_lastname_entry.get()
        if lastname == "":
            tkinter.messagebox.showwarning(title="Cognome mancante", message="Inserisci il cognome del cliente per "
                                                                             "procedere alla ricerca!")
            self.customer_lastname_entry.focus_set()
        else:
            lastname = lastname.upper()
            customers = DataRetrieve().customer(lastname)
            if not customers:
                question = tkinter.messagebox.askyesno(title="Cliente non censito", message="Il cliente non è censito, "
                                                                                            "procedere alla "
                                                                                            "registrazione?")
                if question:
                    customer_view = CustomerView(last_name=lastname, win=self.mainwindow)
                #self.mainwindow.destroy()
                else:
                    self.customer_lastname_entry.focus_set()
            else:
                customer_pick = CustomerPick(lastname, self.customer_cod_entry, self.customer_lastname_entry,
                                             self.customer_firstname_entry, self.customer_phone_entry)

    def on_insert_order_btn_press(self):
        code = self.customer_cod_entry.get()
        first_name = self.customer_firstname_entry.get()
        last_name = self.customer_lastname_entry.get()
        customer = f'{code} {last_name} {first_name}'
        product = self.product_name_entry.get()
        serial = self.serial_number_entry.get()
        malfunction = self.malfunction_txt.get("1.0", END)
        arrival = date.today()

        DataWrite().insert_order(customer, product, serial, arrival, malfunction)
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = OrderInsertWindow()
    app.run()
