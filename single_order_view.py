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
import ttkbootstrap as ttk

import pygubu

from db_functions import DataRetrieve, DataWrite
from pdf_functions import Prints
from work_pick import WorkPick

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "single_order_view.ui"


class SingleOrderView:
    def __init__(self, code=None, master=None):
        self.date = datetime.datetime.now()
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.edit = False
        # Main widget
        self.mainwindow = builder.get_object("single_order_view", master)
        builder.connect_callbacks(self)
        self.mainwindow.focus_set()

        self.mainwindow.state('zoomed')

        self.code = code

        self.productvar = None
        builder.import_variables(self, ['productvar'])
        self.productvar.trace("w", lambda name, index, mode, sv=self.productvar: self.retrieve_products())

        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_close)
        # Importa widget
        # Area cliente
        self.customer_code_entry = builder.get_object("customer_code_entry")
        self.company_entry = builder.get_object("company_entry")
        self.customer_name_entry = builder.get_object("customer_name_entry")
        self.customer_lname_entry = builder.get_object("customer_lname_entry")
        self.customer_city_entry = builder.get_object("customer_city_entry")
        self.customer_phone_entry = builder.get_object("customer_phone_entry")

        # Area prodotto
        self.product_name_entry = builder.get_object("product_name_entry")
        self.status_progressbar = builder.get_object("status_progressbar")
        self.status_progressbar.configure(bootstyle="success-striped")
        self.product_date_in_entry = builder.get_object("product_date_in_entry")
        self.product_date_out_entry = builder.get_object("product_date_out_entry")
        self.product_diagnosis_entry = builder.get_object("product_diagnosis_entry")
        self.product_malfunction_txt = builder.get_object("product_malfunction_txt")
        self.repair_tv = builder.get_object("repair_tv")
        self.repair_insert_btn = builder.get_object("repair_insert_btn")  # TASTO DISATTIVATO DI DEFAULT, DA ATTIVARE
        self.newline_btn = builder.get_object("newline_btn")              # TASTO DISATTIVATO DI DEFAULT, DA ATTIVARE
        self.work_delete_btn = builder.get_object("work_delete_btn")      # TASTO DISATTIVATO DI DEFALUT, DA ATTIVARE
        self.product_notes_txt = builder.get_object("product_notes_txt")

        # Frame laterale
        self.side_frame = builder.get_object("side_frame")
        self.query_entry = builder.get_object("query_entry")
        self.product_tv = builder.get_object("product_tv")
        self.product_tv.bind("<Double-1>", self.on_product_click)
        self.product_code_entry = builder.get_object("product_code_entry")
        self.product_desc_entry = builder.get_object("product_desc_entry")
        self.price_entry = builder.get_object("price_entry")

        # Toolbar
        self.in_progress_btn = builder.get_object("in_progress_btn")
        self.done_btn = builder.get_object("done_btn")
        self.delivered_btn = builder.get_object("delivered_btn")

        self.on_load(code=code)

    def run(self):
        self.mainwindow.mainloop()

    def on_close(self, event=None):
        if self.edit:
            ask = tkinter.messagebox.askyesno(parent=self.mainwindow, title="Salvare il lavoro?",
                                              message="Ci sono modifiche non salvate, si intende salvarle?")
            if ask:
                self.on_order_update_press()
        self.mainwindow.destroy()

    def retrieve_products(self, event=None):
        self.product_tv.delete(*self.product_tv.get_children())
        query = self.query_entry.get()
        products = DataRetrieve().single_product_code(query)
        if not products:
            products = DataRetrieve().single_product_name(query)

        for product in products:
            product = (product[0], product[2], product[9])
            self.product_tv.insert("", END, values=product)

    def on_load(self, code):
        order = DataRetrieve().single_order_code(code=code)
        customer = DataRetrieve().single_customer_code(order[1])
        self.customer_code_entry.insert(0, order[1])
        self.customer_code_entry.configure(state="readonly")
        self.company_entry.insert(0, customer[1])
        self.company_entry.configure(state="readonly")
        self.customer_name_entry.insert(0, customer[2])
        self.customer_name_entry.configure(state="readonly")
        self.customer_lname_entry.insert(0, customer[3])
        self.customer_lname_entry.configure(state="readonly")
        self.customer_city_entry.insert(0, f"{customer[7]} ({customer[6]})")
        self.customer_city_entry.configure(state="readonly")
        self.customer_phone_entry.insert(0, customer[14])
        if self.customer_phone_entry.get() == "":
            self.customer_phone_entry.delete(0, END)
            self.customer_phone_entry.insert(0, customer[13])
        self.customer_phone_entry.configure(state="readonly")
        self.product_name_entry.insert(0, order[3])
        self.product_name_entry.configure(state="readonly")
        self.product_date_in_entry.insert(0, order[4])
        self.product_date_in_entry.configure(state="readonly")
        self.product_date_out_entry.insert(0, str(order[5]))
        self.product_date_out_entry.configure(state="readonly")
        self.product_malfunction_txt.delete(1.0, END)
        self.product_malfunction_txt.insert(1.0, order[6][:-1])
        self.product_diagnosis_entry.delete(0, END)
        self.product_diagnosis_entry.insert(0, order[7])
        self.product_notes_txt.delete(1.0, END)
        self.product_notes_txt.insert(1.0, order[8][:-1])
        status = int(order[2]) + 1
        self.status_progressbar.configure(value=status)
        self.repair_tv.delete(*self.repair_tv.get_children())

        try:
            interventions = order[9].split("], [")
            for intervention in interventions:
                intervention = intervention.split(",")
                intervention_code = str(intervention[0]).replace("[[", "")
                intervention_name = str(intervention[1]).replace("'", "")
                if intervention_name[0] == " ":
                    intervention_name = intervention_name[1:]
                intervention_price = str(intervention[2]).replace("'", "")
                intervention_price = str(intervention_price)
                if intervention_price[0] == " ":
                    intervention_price = intervention_price[1:]
                intervention_date = str(intervention[3]).replace("'", "")
                intervention_date = intervention_date.replace("]]", "")
                if intervention_date[0]:
                    intervention_date = intervention_date[1:]
                intervention = (intervention_code, intervention_name, intervention_price, intervention_date)
                self.repair_tv.insert("", END, values=intervention)

        except TypeError:
            pass
        except IndexError:
            pass
        except AttributeError:
            pass

        if order[2] == 1:
            self.repair_insert_btn.configure(state="normal")
            self.work_delete_btn.configure(state="normal")
            self.newline_btn.configure(state="normal")
            self.status_progressbar.configure(bootstyle="warning-striped")
        if order[2] == 0:
            self.status_progressbar.configure(bootstyle="danger-striped")

    def on_repair_insert_press(self):
        WorkPick(treeview=self.repair_tv, validate=self.on_order_update_press, master=self.mainwindow).\
            mainwindow.grab_set()

    def on_order_update_press(self):
        malfunction = self.product_malfunction_txt.get(1.0, END)
        diagnosis = self.product_diagnosis_entry.get()
        notes = self.product_notes_txt.get(1.0, END)
        intervention = []
        for child in self.repair_tv.get_children():
            intervention.append(self.repair_tv.item(child)["values"])
        DataWrite().order_full_update(malfunction, diagnosis, notes, str(intervention), self.code)
        self.on_load(self.code)
        self.edit = False

    def on_wkdelete_press(self):
        item = self.repair_tv.selection()
        self.repair_tv.delete(item)
        self.edit = True
        self.on_order_update_press()

    def on_inprogress_press(self):
        DataWrite().order_update(code=self.code, status=1)
        self.on_load(self.code)

    def on_done_press(self):
        DataWrite().order_update(code=self.code, status=2)
        self.on_load(self.code)

    def on_delivered_press(self):
        DataWrite().order_update(code=self.code, status=3)
        self.on_load(self.code)

    def on_export_press(self):
        customer_code = self.customer_code_entry.get()
        company = self.company_entry.get()
        customer_name = self.customer_name_entry.get()
        customer_lname = self.customer_lname_entry.get()
        customer_city = self.customer_city_entry.get()
        customer_phone = self.customer_phone_entry.get()
        product = self.product_name_entry.get()
        date_in = self.product_date_in_entry.get()
        date_out = self.product_date_out_entry.get()
        malfunction = self.product_malfunction_txt.get(1.0, END)
        works = []
        for child in self.repair_tv.get_children():
            works.append(self.repair_tv.item(child)["values"])
        notes = self.product_notes_txt.get(1.0, END)

        Prints().order_invoice(order_cod=self.code, customer_code=customer_code, company=company,
                               customer_name=customer_name, customer_lname=customer_lname, customer_city=customer_city,
                               customer_phone=customer_phone, product=product, date_in=date_in, date_out=date_out,
                               malfunction=malfunction, works=works, notes=notes)

    def on_newline_press(self):
        self.retrieve_products()
        if self.side_frame.winfo_reqwidth() == 400:
            self.side_frame.configure(width=0)
        else:
            self.side_frame.configure(width=400)

    def on_product_click(self, event=None):
        self.product_code_entry.configure(state="normal")
        self.product_code_entry.delete(0, END)
        self.product_desc_entry.delete(0, END)
        self.price_entry.delete(0, END)
        item = self.product_tv.selection()
        for i in item:
            product_idx = self.product_tv.item(i, "values")[0]
            product_name = self.product_tv.item(i, "values")[1]
            product_price = self.product_tv.item(i, "values")[2]
            self.product_code_entry.insert(0, product_idx)
            self.product_code_entry.configure(state="readonly")
            self.product_desc_entry.insert(0, product_name)
            self.price_entry.insert(0, product_price)

    def on_insert_press(self):
        product_idx = self.product_code_entry.get()
        if product_idx == "":
            product_idx = 0
        product_name = self.product_desc_entry.get()
        product_price = self.price_entry.get()
        if product_price != "":
            product_price = "%.2f" % float(product_price)
        date = self.date.strftime('%d/%m/%Y')
        product_row = (product_idx, product_name, product_price, date)
        if product_name != "":
            self.repair_tv.insert("", END, values=product_row)
            self.on_order_update_press()
            self.side_frame.configure(width=0)
        else:
            self.product_desc_entry.configure(bootstyle="danger")

    def on_undo_press(self):
        self.side_frame.configure(width=0)


if __name__ == "__main__":
    app = SingleOrderView()
    app.run()
