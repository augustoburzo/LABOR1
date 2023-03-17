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
import tkinter.messagebox
from tkinter import END

import pygubu

from customer_pick import CustomerPick
from db_functions import DataRetrieve, DataWrite, DataDelete
from pdf_functions import Prints
from single_order_view import SingleOrderView

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "order_view.ui"


class OrderView:
    def __init__(self, master=None):
        self.date = datetime.datetime.now()
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("full_order_window", master)
        builder.connect_callbacks(self)

        self.mainwindow.state('zoomed')

        self.code = "0"

        self.orders_tv = builder.get_object("orders_tv")
        self.orders_tv.bind("<Double-1>", self.on_treeview_press)
        self.query_entry = builder.get_object("query_entry")
        self.prd_name_entry = builder.get_object("prd_name_entry")
        self.sn_entry = builder.get_object("sn_entry")
        self.date_in_cal = builder.get_object("date_in_cal")
        self.malfunction_txt = builder.get_object("malfunction_txt")
        self.work_entry = builder.get_object("work_entry")
        self.notes_txt = builder.get_object("notes_txt")

        self.cust_code_entry = builder.get_object("cust_code_entry")
        self.company_entry = builder.get_object("company_entry")
        self.first_name_entry = builder.get_object("first_name_entry")
        self.last_name_entry = builder.get_object("last_name_entry")
        self.city_entry = builder.get_object("city_entry")
        self.cell_entry = builder.get_object("cell_entry")

        self.search_query_entry = builder.get_object("search_query_entry")

        self.orders_save_btn = builder.get_object("orders_save_btn")
        self.orders_save_btn.configure(style="warning.TButton")

        self.separator1 = builder.get_object("separator1")
        self.separator1.configure(orient='vertical', style='info.Vertical.TSeparator')

        self.separator2 = builder.get_object("separator2")
        self.separator2.configure(orient='vertical', style='info.Vertical.TSeparator')

        self.separator3 = builder.get_object("separator3")
        self.separator3.configure(orient='vertical', style='info.Vertical.TSeparator')

        self.delete_btn = builder.get_object("delete_btn")
        self.delete_btn.configure(style="danger.TButton")

        self.export_orders_btn = builder.get_object("export_orders_btn")

        self.view_order_btn = builder.get_object("view_order_btn")

        self.query_entry.bind("<Return>", self.on_search_press)
        self.search_query_entry.bind("<Return>", self.on_order_search_press)

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def on_load(self):
        self.date_in_cal.delete(0, END)
        date = self.date.strftime('%d/%m/%Y')
        self.date_in_cal.insert(0, date)
        self.orders_tv.delete(*self.orders_tv.get_children())
        orders = DataRetrieve
        all_orders = orders().all_orders()
        for order in all_orders:
            code = order[0]
            cust_code = order[1]
            status = order[2]
            product = order[3]
            date_in = order[4]
            date_out = order[5]
            malfunction = order[6]
            customer = DataRetrieve().single_customer_code(cust_code)
            company = ""
            first_name = ""
            last_name = ""
            if customer is not None:
                company = customer[1]
                first_name = customer[2]
                last_name = customer[3]

            values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction)

            self.orders_tv.insert("", END, values=values)
            self.orders_tv.focus_set()

    def on_search_press(self, event=None):
        query = self.query_entry.get().upper()
        customer_pick = CustomerPick
        customer_pick(query, self.cust_code_entry, self.company_entry, self.last_name_entry, self.first_name_entry,
                      self.cell_entry, self.city_entry).mainwindow.grab_set()
        self.mainwindow.focus_set()

    def on_order_save_press(self):
        cust_code = self.cust_code_entry.get()

        prd_name = f"{self.prd_name_entry.get()} | {self.sn_entry.get()}"
        date_in = self.date_in_cal.get()
        malfunction = self.malfunction_txt.get(1.0, END)
        work = self.work_entry.get()
        notes = self.notes_txt.get(1.0, END)

        insert_order = DataWrite
        insert_order().insert_order(cust_code, prd_name, date_in, malfunction, work, notes)

        self.on_load()

    def on_order_view_press(self):
        SingleOrderView(master=self.mainwindow, code=self.code).mainwindow.grab_set()

    def on_treeview_press(self, event):
        item = self.orders_tv.selection()
        for i in item:
            order_idx = self.orders_tv.item(i, "values")[0]
            self.code = order_idx
            order = DataRetrieve().single_order_code(order_idx)
            cust_code = order[1]
            status = order[2]
            product = order[3]
            date_in = order[4]
            date_out = order[5]
            malfunction = order[6]
            work = order[7]
            notes = order[8]
            customer = DataRetrieve().single_customer_code(cust_code)
            company = ""
            first_name = ""
            last_name = ""
            city = ""
            cell = ""
            if customer is not None:
                company = customer[1]
                first_name = customer[2]
                last_name = customer[3]
                city = customer[7]
                cell = customer[14]

            self.on_clear_press()
            self.cust_code_entry.configure(state="normal")
            self.cust_code_entry.insert(0, cust_code)
            self.cust_code_entry.configure(state="readonly")
            self.company_entry.configure(state="normal")
            self.company_entry.insert(0, company)
            self.company_entry.configure(state="readonly")
            self.first_name_entry.configure(state="normal")
            self.first_name_entry.insert(0, first_name)
            self.first_name_entry.configure(state="readonly")
            self.last_name_entry.configure(state="normal")
            self.last_name_entry.insert(0, last_name)
            self.last_name_entry.configure(state="readonly")
            self.city_entry.configure(state="normal")
            self.city_entry.insert(0, city)
            self.city_entry.configure(state="readonly")
            self.cell_entry.configure(state="normal")
            self.cell_entry.insert(0, cell)
            self.cell_entry.configure(state="readonly")
            product = product.split(" | ")
            self.prd_name_entry.insert(0, product[0])
            self.sn_entry.insert(0, product[1])
            self.date_in_cal.delete(0, END)
            self.date_in_cal.insert(0, date_in)
            self.malfunction_txt.insert(1.0, malfunction)
            self.work_entry.insert(0, work)
            self.notes_txt.insert(1.0, notes)
            self.orders_save_btn.configure(state="disabled")

            self.export_orders_btn.configure(state="normal")
            self.view_order_btn.configure(state="normal")

    def on_print_press(self):
        item = self.orders_tv.selection()
        order_idx = None
        for i in item:
            order_idx = self.orders_tv.item(i, "values")[0]
        cust_code = self.cust_code_entry.get()
        company = self.company_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        city = self.city_entry.get()
        cell = self.cell_entry.get()

        prd_name = f"{self.prd_name_entry.get()} | {self.sn_entry.get()}"
        date_in = self.date_in_cal.get()
        malfunction = self.malfunction_txt.get(1.0, END)
        work = self.work_entry.get()
        notes = self.notes_txt.get(1.0, END)

        Prints().single_order(order_idx, cust_code, company, first_name, last_name, city, cell, prd_name, date_in, work,
                              malfunction, notes)

        self.mainwindow.focus_set()

    def on_ord_list_press(self):
        orders = DataRetrieve
        all_orders = orders().all_working_orders()
        processed_orders = []
        for order in all_orders:
            code = order[0]
            cust_code = order[1]
            status = order[2]
            product = order[3]
            date_in = order[4]
            date_out = order[5]
            malfunction = order[6]
            customer = DataRetrieve().single_customer_code(cust_code)
            company = ""
            first_name = ""
            last_name = ""
            if customer is not None:
                company = customer[1]
                first_name = customer[2]
                last_name = customer[3]

            values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction)
            processed_orders.append(values)
        Prints().orders_list(processed_orders)

        self.mainwindow.focus_set()

    def on_clear_press(self):
        self.cust_code_entry.configure(state="normal")
        self.company_entry.configure(state="normal")
        self.first_name_entry.configure(state="normal")
        self.last_name_entry.configure(state="normal")
        self.city_entry.configure(state="normal")
        self.cell_entry.configure(state="normal")

        self.cust_code_entry.delete(0, END)
        self.company_entry.delete(0, END)
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.city_entry.delete(0, END)
        self.cell_entry.delete(0, END)

        self.cust_code_entry.configure(state="readonly")
        self.company_entry.configure(state="readonly")
        self.first_name_entry.configure(state="readonly")
        self.last_name_entry.configure(state="readonly")
        self.city_entry.configure(state="readonly")
        self.cell_entry.configure(state="readonly")

        self.prd_name_entry.delete(0, END)
        self.sn_entry.delete(0, END)
        self.date_in_cal.delete(0, END)
        date = self.date.strftime('%d/%m/%Y')
        self.date_in_cal.insert(0, date)
        self.malfunction_txt.delete(1.0, END)
        self.work_entry.delete(0, END)
        self.notes_txt.delete(1.0, END)

        self.orders_save_btn.configure(state="normal")
        self.export_orders_btn.configure(state="disabled")
        self.view_order_btn.configure(state="disabled")

    def on_delete_press(self):
        item = self.orders_tv.selection()
        for i in item:
            order_idx = self.orders_tv.item(i, "values")[0]
            askdelete = tkinter.messagebox.askyesno(parent=self.mainwindow,
                                                    title="Eliminare ordine?",
                                                    message=f"Sei sicuro di voler eliminare"
                                                            f" l'ordine N°{order_idx}?")
            if askdelete:
                DataDelete().delete_order(order_idx)
                self.on_load()
                self.mainwindow.focus_set()
            else:
                self.mainwindow.focus_set()

    def on_order_search_press(self, event=None):
        query = self.search_query_entry.get()
        orders = DataRetrieve().multiple_orders_code(query)
        if not orders:
            orders = DataRetrieve().multiple_orders_name(query)
        self.orders_tv.delete(*self.orders_tv.get_children())
        for order in orders:
            code = order[0]
            cust_code = order[1]
            status = order[2]
            product = order[3]
            date_in = order[4]
            date_out = order[5]
            malfunction = order[6]
            customer = DataRetrieve().single_customer_code(cust_code)
            company = ""
            first_name = ""
            last_name = ""
            if customer is not None:
                company = customer[1]
                first_name = customer[2]
                last_name = customer[3]

            values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction)
            self.orders_tv.insert("", END, values=values)


if __name__ == "__main__":
    app = OrderView()
    app.run()
