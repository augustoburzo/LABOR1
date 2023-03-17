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

import datetime
import pathlib
import tkinter
from configparser import ConfigParser
from tkinter import END
import tkinter.messagebox

import pygubu
from ttkbootstrap.toast import ToastNotification

from db_functions import DataRetrieve, DataWrite


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "product_insert.ui"


class ProductInsert:
    def __init__(self, status=None, treeview=None, function=None, single=False, freerow=False,
                 report=False, supplier=None, list=None, master=None):
        self.date = datetime.datetime.now()
        self.status = status
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.function = function
        self.mainwindow = builder.get_object("new_product_window", master)
        self.mainwindow.focus_set()

        self.treeview = treeview
        self.report = report
        self.supplier = supplier
        self.updated = False

        self.codevar = None
        self.qtyvar = None
        self.unitvar = None
        self.taxvar = None
        self.namevar = None
        builder.import_variables(self, ['codevar', 'qtyvar', 'unitvar', 'taxvar', 'namevar'])
        # self.codevar.trace("w", lambda name, index, mode, sv=self.codevar: self.callback())

        self.qtyvar.trace("w", lambda name, index, mode, sv=self.qtyvar: self.price_calculator())

        self.unitvar.trace("w", lambda name, index, mode, sv=self.unitvar: self.price_calculator())

        self.taxvar.trace("w", lambda name, index, mode, sv=self.taxvar: self.price_calculator())

        self.namevar.trace("w", lambda name, index, mode, sv=self.taxvar: self.price_calculator())

        builder.connect_callbacks(self)

        self.search_tv = builder.get_object("search_tv")
        self.cod_entry = builder.get_object("cod_entry")
        self.cat_combo = builder.get_object("cat_combo")
        self.ean_entry = builder.get_object("ean_entry")
        self.product_entry = builder.get_object("product_entry")
        self.unit_entry = builder.get_object("unit_entry")
        self.qty_entry = builder.get_object("qty_entry")
        self.unit_price_entry = builder.get_object("unit_price_entry")
        self.discount1_entry = builder.get_object("discount1_entry")
        self.discount2_entry = builder.get_object("discount2_entry")
        self.price_entry = builder.get_object("price_entry")
        self.iva_entry = builder.get_object("iva_entry")
        self.total_entry = builder.get_object("total_entry")
        self.selling_entry = builder.get_object("selling_entry")
        self.top_notebook = builder.get_object("top_notebook")
        self.history_tv = builder.get_object("history_tv")
        self.supplier_entry = builder.get_object("supplier_entry")

        self.top_frame = builder.get_object("top_frame")
        self.separator2 = builder.get_object("separator2")
        self.save_btn = builder.get_object("save_btn")
        self.update_btn = builder.get_object("update_btn")
        self.separator3 = builder.get_object("separator3")

        self.select_btn = builder.get_object("select_btn")
        self.separator4 = builder.get_object("separator4")

        self.query_entry = builder.get_object("query_entry")
        self.query_entry.bind("<Return>", self.on_search_press)

        self.search_tv.bind("<Double-1>", self.on_search_click)

        categories = []
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}cat.dat"
        with open(filename, "r") as f:
            cats = f.readlines()
            for cat in cats:
                cat = cat.split(",")
                categories.append(cat[1].replace("\n", ""))

        self.cat_combo.configure(values=categories, state="readonly")
        self.cat_combo.current(0)

        if single:
            self.select_btn.destroy()
            self.separator4.destroy()
            self.qty_entry.delete(0, END)
            self.qty_entry.insert(0, "0")

        if freerow:
            self.mainwindow.geometry("800x600")
            self.mainwindow.title("Riga libera")
            self.top_notebook.tab(0, state="disabled")
            self.top_notebook.tab(1, state="disabled")
            self.supplier_entry.configure(state="disabled")
            self.separator2.destroy()
            self.save_btn.destroy()
            self.update_btn.destroy()
            self.separator3.destroy()
            self.select_btn.configure(text="Inserisci prodotto...")

        taxes = []
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}tax.dat"
        with open(filename, "r") as taxfile:
            for line in taxfile:
                line = line.strip()
                taxes.append(line)

        taxlines = []
        for tax in taxes:
            tax = tax.split(",")
            tax = " - ".join(tax)
            taxlines.append(tax)
        self.iva_entry.configure(values=taxlines, state="readonly")
        self.iva_entry.current(0)

        self.iva_entry.bind("<<ComboboxSelected>>", self.price_calculator)
        if supplier is not None:
            self.supplier_entry.insert(0, supplier)
        if not freerow:
            self.on_search_press()

    def run(self):
        self.mainwindow.mainloop()

    def on_search_press(self, event=None):
        self.search_tv.delete(*self.search_tv.get_children())
        query = self.query_entry.get()
        products = DataRetrieve().single_product_code(query)
        if not products:
            products = DataRetrieve().single_product_name(query)

        for product in products:
            product = (product[0], product[1], product[2])
            self.search_tv.insert("", END, values=product)

    def on_clear(self):
        # Svuota le entries
        self.cod_entry.delete(0, END)
        self.cat_combo.delete(0, END)
        self.product_entry.delete(0, END)
        self.unit_price_entry.delete(0, END)
        self.discount1_entry.delete(0, END)
        self.discount2_entry.delete(0, END)
        self.iva_entry.delete(0, END)
        self.ean_entry.delete(0, END)
        self.total_entry.delete(0, END)
        self.qty_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.qty_entry.insert(0, 1)
        self.selling_entry.delete(0, END)
        self.supplier_entry.delete(0, END)
        self.history_tv.delete(*self.history_tv.get_children())

    def on_save_press(self):
        # Salva il nuovo articolo popolando le variabili dalle entries
        cod = self.cod_entry.get()
        category = self.cat_combo.get()
        product = self.product_entry.get()
        ean = self.ean_entry.get()
        unit = self.unit_entry.get()
        quantity = self.qty_entry.get()
        price = self.unit_price_entry.get()
        discount1 = self.discount1_entry.get()
        discount2 = self.discount2_entry.get()
        total_price = self.price_entry.get()
        iva = self.iva_entry.get()
        total_taxed = self.total_entry.get()
        selling = self.selling_entry.get()
        # Verifica che i campi necessari siano indicati
        if cod or ean or selling != "":
            # Inserisce i dati acquisiti attraverso le entries a database
            check = DataWrite().insert_product(cod, category, product, ean, unit, quantity, price, discount1, discount2,
                                               selling, iva)
            toast = ToastNotification(
                title="Prodotto salvato",
                message="Il prodotto è stato salvato con successo!",
                duration=3000,
                icon="💾",
                bootstyle="success"
            )
            toast.show_toast()
            self.updated = True
            self.on_clear()
            if not check:
                # Riporta un messaggio d'errore in caso di prodotto già presente a database
                tkinter.messagebox.showerror(parent=self.mainwindow, title="Codice o EAN già esistente",
                                             message="Il codice o l'EAN fornito sono già esistenti, si prega di "
                                                     "verificare")
                self.mainwindow.focus_set()
        else:
            # Riporta un messaggio d'errore in caso di dati mancanti
            tkinter.messagebox.showwarning(parent=self.mainwindow, title="Codice, EAN o Prezzo nulli",
                                           message="Il codice prodotto, l'EAN e il prezzo di vendita"
                                                   " non possono essere nulli.")

    def on_select_press(self):
        code = self.cod_entry.get()
        cat = self.cat_combo.get()
        product = self.product_entry.get()
        unit = self.unit_entry.get()
        qty = self.qty_entry.get()
        unit_price = self.unit_price_entry.get()
        discount1 = self.discount1_entry.get()
        discount2 = self.discount2_entry.get()
        price = self.price_entry.get()
        iva = self.iva_entry.get()
        total = self.total_entry.get()
        selling = self.selling_entry.get()
        try:
            if self.status == "in":
                values = (code, cat, product, unit, qty, unit_price, discount1, discount2, price, iva, total)
                self.on_update_press()
            else:
                iva = iva.split(" - ")[2]
                tax_coeff = f"1.{iva}"
                tax_coeff = float(tax_coeff)
                unit_selling = float(selling) / tax_coeff
                selling_tot = float(selling) * float(qty)
                sell_price = float(unit_selling) * float(qty)
                values = (code, cat, product, unit, qty, "%.2f" % unit_selling, discount1, discount2,
                          "%.2f" % sell_price, iva, "%.2f" % selling_tot)
                if self.report:
                    values = (code, product, "%.2f" % selling_tot)

            self.treeview.insert("", END, values=values)
            try:
                self.function()
            except TypeError:
                pass
            self.mainwindow.destroy()
        except ValueError:
            tkinter.messagebox.showerror(parent=self.mainwindow, title="Dati incompleti o errati",
                                         message="Verificare i dati e riprovare. Il prezzo di vendita è stato"
                                                 " indicato?")

    def on_update_press(self):
        code = self.cod_entry.get()
        cat = self.cat_combo.get()
        product = self.product_entry.get()
        ean = self.ean_entry.get()
        unit = self.unit_entry.get()
        qty = self.qty_entry.get()
        unit_price = self.unit_price_entry.get()
        discount1 = self.discount1_entry.get()
        discount2 = self.discount2_entry.get()
        price = self.price_entry.get()
        iva = self.iva_entry.get()
        total = self.total_entry.get()
        selling = self.selling_entry.get()
        supplier = self.supplier_entry.get()
        if supplier != "":
            row = (supplier, unit_price, self.date.strftime('%d/%m/%Y'))
            self.history_tv.insert("", END, values=row)
        buffer = ""
        for child in self.history_tv.get_children():
            value = self.history_tv.item(child)["values"]
            value = f"{value[0]},{value[1]},{value[2]};"
            buffer = buffer + value

        check = DataWrite().update_product(code, cat, product, ean, unit, qty, price, discount1, discount2, selling,
                                           iva, buffer)
        if check:
            toast = ToastNotification(
                title="Prodotto aggiornato",
                message="Il prodotto è stato salvato con successo!",
                duration=3000,
                icon="💾",
                bootstyle="success"
            )
            toast.show_toast()
            self.updated = True
        self.on_clear()

    def callback(self):
        code = self.cod_entry.get()
        products = DataRetrieve().single_product_code(code)
        self.search_tv.delete(*self.search_tv.get_children())
        for product in products:
            self.search_tv.insert("", END, values=product)

    def product_find(self, event=None):
        product_name = self.product_entry.get(0, END)
        products = DataRetrieve().single_product_name()

    def price_calculator(self, event=None):
        try:
            # Corregge la forma dei dati inseriti e li rende computabili
            qty = int(float(self.qty_entry.get()))
            unit_price = self.unit_price_entry.get()
            unit_price.replace(",", ".")
            unit_price = float(unit_price)
            # Moltiplica il prezzo unitario per la quantità
            price = qty * unit_price
            self.price_entry.delete(0, END)
            self.price_entry.insert(0, "%.2f" % price)
            iva_perc = self.iva_entry.get()
            iva_perc = iva_perc.split(" - ")[-1]
            if int(iva_perc) < 10:
                iva_perc = f"0{iva_perc}"
            iva_eval = f"1.{iva_perc}"
            iva_coeff = float(iva_eval)
            self.total_entry.delete(0, END)
            # Moltiplica il prezzo per il coefficiente IVA
            total_price = iva_coeff * price
            self.total_entry.insert(0, "%.2f" % total_price)
        except ValueError:
            # Raccoglie l'errore dovuto alla entry vuota
            pass

    def on_search_click(self, event):
        # Popola le entries con quanto ottenuto dalla treeview prima e dal database dopo
        item = self.search_tv.selection()
        for i in item:
            product_idx = self.search_tv.item(i, "values")[0]

            # Ricerca il singolo prodotto in database
            product = DataRetrieve().single_product_code(product_idx)
            product = product[0]
            self.cod_entry.delete(0, END)
            self.cod_entry.insert(0, product[0])
            self.cat_combo.delete(0, END)
            self.cat_combo.insert(0, product[1])
            self.product_entry.delete(0, END)
            self.product_entry.insert(0, product[2])
            self.ean_entry.delete(0, END)
            self.ean_entry.insert(0, product[3])
            self.unit_entry.delete(0, END)
            self.unit_entry.insert(0, product[4])
            unit_price = str(product[6]).replace(",", ".")
            unit_price = float(unit_price)
            self.unit_price_entry.delete(0, END)
            self.unit_price_entry.insert(0, "%.2f" % unit_price)
            self.discount1_entry.delete(0, END)
            self.discount1_entry.insert(0, product[7])
            self.discount2_entry.delete(0, END)
            self.discount2_entry.insert(0, product[8])
            self.iva_entry.delete(0, END)
            self.iva_entry.insert(0, product[10])
            self.selling_entry.delete(0, END)
            self.selling_entry.insert(0, product[9])
            self.history_tv.delete(*self.history_tv.get_children())
            history = product[11]
            history = history.split(";")
            for line in history[:-1]:
                line = line.split(",")
                self.history_tv.insert("", 0, values=line)

            # Calcola i prezzi aggiornati in base all'ultimo prodotto inserito
            self.price_calculator()


if __name__ == "__main__":
    app = ProductInsert()
    app.run()
