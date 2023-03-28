#!/usr/bin/python3
# Labor1 - Augusto Burzo

import datetime
import os
import pathlib
import sys
import threading
import time
import tkinter.messagebox
from configparser import ConfigParser
import shutil
from zipfile import ZipFile

from ttkbootstrap.toast import ToastNotification

from agenda import Agenda
from company_config import CompanyConfig
from credits import Credits
from customer_view import CustomerView
from db_functions import DataRetrieve, DBInit, DataDelete, DataWrite
from document_view import DocumentView

from order_insert_window import OrderInsertWindow

import pygubu

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from ttkbootstrap.tooltip import ToolTip

from order_view import OrderView
from pdf_functions import Prints
from preferences_window import PreferencesWindow
from product_insert import ProductInsert
from single_order_view import SingleOrderView
from single_product_view import SingleProductView
from supplier_view import SupplierView
from warehouse_management_window import WarehouseManagementWindow
from new_document import NewDocument
from work_report import WorkReport
from xl_functions import XLSaver

if getattr(sys, 'frozen', False):
    import pyi_splash

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "main_window.ui"


class MainWindow:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        config_object = ConfigParser()
        config_object.read("company.ini")
        companyinfo = config_object["COMPANYINFO"]

        # Main widget
        self.mainwindow = builder.get_object("main_window", master)
        builder.connect_callbacks(self)
        self.mainwindow.title(f"Labor1 | {companyinfo['company']} - {companyinfo['city']}"
                              f" ({companyinfo['prov']})")

        Style('labor')

        self.mainwindow.state("zoomed")

        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_close)

        DBInit()

        # Inizializza le treeview della sezione ordini
        self.waiting_tv = builder.get_object("waiting_tv")
        self.waiting_tv.bind("<Double-1>", self.on_order_click)
        self.progress_tv = builder.get_object("progress_tv")
        self.progress_tv.bind("<Double-1>", self.on_order_click)
        self.done_tv = builder.get_object("done_tv")
        self.done_tv.bind("<Double-1>", self.on_order_click)

        # Inizializza le funzioni della sezione magazzino
        self.in_stock_tv = builder.get_object("in_stock_tv")
        self.in_stock_tv.bind("<Double-1>", self.on_product_tv_press)
        self.ending_tv = builder.get_object("ending_tv")
        self.ending_tv.bind("<Double-1>", self.on_product_tv_press)
        self.wh_search_entry = builder.get_object("wh_search_entry")
        self.wh_search_entry.bind("<Return>", self.on_search_btn_press)

        self.separator1 = builder.get_object("separator1")
        self.separator1.configure(orient='vertical', style='info.Vertical.TSeparator')

        # Binding dei ToolTip sui tasti d'interfaccia
        self.customers_list_btn = builder.get_object("customers_list_btn")
        ToolTip(self.customers_list_btn, text="Consulta anagrafiche clienti", bootstyle=PRIMARY)

        self.suppliers_list_btn = builder.get_object("suppliers_list_btn")
        ToolTip(self.suppliers_list_btn, text="Consulta anagrafiche fornitori", bootstyle=PRIMARY)

        self.btn_orders = builder.get_object("btn_orders")
        ToolTip(self.btn_orders, text="Consulta lista ordini", bootstyle=PRIMARY)

        self.new_document_btn = builder.get_object("new_document_btn")
        ToolTip(self.new_document_btn, text="Inserisci nuovo documento", bootstyle=PRIMARY)

        self.new_prev_btn = builder.get_object("new_prev_btn")
        ToolTip(self.new_prev_btn, text="Genera nuovo preventivo", bootstyle=PRIMARY)

        self.add_prd_btn = builder.get_object("add_prd_btn")
        ToolTip(self.add_prd_btn, text="Inserisci nuovo prodotto", bootstyle=PRIMARY)

        self.report_btn = builder.get_object("report_btn")
        ToolTip(self.report_btn, text="Inserisci o gestisci i rapportini", bootstyle=PRIMARY)

        self.settings_btn = builder.get_object("settings_btn")
        ToolTip(self.settings_btn, text="Gestisci le impostazioni", bootstyle=PRIMARY)

        self.delete_btn = builder.get_object("delete_btn")
        self.delete_btn.configure(style="danger.TButton")
        ToolTip(self.delete_btn, text="Elimina l'ordine", bootstyle=DANGER)

        self.in_progress_btn = builder.get_object("in_progress_btn")
        self.in_progress_btn.configure(bootstyle="success")
        ToolTip(self.in_progress_btn, text="Metti l'ordine in lavorazione", bootstyle=PRIMARY)

        self.done_btn = builder.get_object("done_btn")
        self.done_btn.configure(style="warning.TButton")
        ToolTip(self.done_btn, text="Contrassegna l'ordine come lavorato", bootstyle=PRIMARY)

        self.delivered_btn = builder.get_object("delivered_btn")
        self.delivered_btn.configure(bootstyle="info")
        ToolTip(self.delivered_btn, text="Contrassegna l'ordine come restituito", bootstyle=PRIMARY)

        # Carica i dati dal db per popolare le tabelle della schermata principale
        self.waiting_orders = DataRetrieve().waiting_orders()
        self.in_progress_orders = DataRetrieve().in_progress_orders()
        self.done_orders = DataRetrieve().done_orders()
        self.products = DataRetrieve().warehouse_status()

        self.warehouse_lf = builder.get_object("warehouse_lf")
        self.overview_lf = builder.get_object("overview_lf")

        self.overview_notebook = builder.get_object("overview_notebook")
        self.warehouse_notebook = builder.get_object("warehouse_notebook")

        self.auto_update_daemon()

    def run(self):
        if getattr(sys, 'frozen', False):
            pyi_splash.close()
        self.mainwindow.mainloop()

    def on_load(self):
        DBInit()

        self.waiting_tv.delete(*self.waiting_tv.get_children())
        self.progress_tv.delete(*self.progress_tv.get_children())
        self.done_tv.delete(*self.done_tv.get_children())

        # Attiva la ricerca del database e la consultazione delle tabelle ordini

        # Ordini in attesa
        for order in self.waiting_orders:
            code = order[0]
            cust_code = order[1]
            status = order[2]
            product = order[3]
            date_in = order[4]
            date_out = order[5]
            malfunction = order[6]
            customer = DataRetrieve().single_customer_code(cust_code)
            company = customer[1]
            first_name = customer[2]
            last_name = customer[3]

            values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction)
            self.waiting_tv.insert("", END, values=values)

        # Ordini in corso
        for order in self.in_progress_orders:
            code = order[0]
            cust_code = order[1]
            status = order[2]
            product = order[3]
            date_in = order[4]
            date_out = order[5]
            malfunction = order[6]
            customer = DataRetrieve().single_customer_code(cust_code)
            company = customer[1]
            first_name = customer[2]
            last_name = customer[3]

            values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction)
            self.progress_tv.insert("", END, values=values)

        # Ordini completati
        for order in self.done_orders:
            code = order[0]
            cust_code = order[1]
            status = order[2]
            product = order[3]
            date_in = order[4]
            date_out = order[5]
            malfunction = order[6]
            customer = DataRetrieve().single_customer_code(cust_code)
            company = customer[1]
            first_name = customer[2]
            last_name = customer[3]

            values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction)
            self.done_tv.insert("", END, values=values)

        # Attiva la ricerca del database e la consultazione della tabella magazzino
        self.in_stock_tv.delete(*self.in_stock_tv.get_children())
        wharehouse = DataRetrieve().warehouse_status()
        for product in wharehouse:
            self.in_stock_tv.insert("", END, values=product)

        products_low = DataRetrieve().warehouse_low_qty()
        self.ending_tv.delete(*self.ending_tv.get_children())
        for productl in products_low:
            self.ending_tv.insert("", END, values=productl)

    def on_close(self):
        # Chiede conferma per chiusura programma
        answer = tkinter.messagebox.askyesno(title="Chiusura programma", message="Sei sicuro di voler chiudere Labor1?")
        if answer:
            self.mainwindow.destroy()

    def update_lookup(self):
        # Carica i dati all'apertura del programma
        self.on_load()
        # Funzione di ricerca aggiornamenti lavorazioni in loop
        while 1:
            time.sleep(1)
            waiting_orders = DataRetrieve().waiting_orders()
            in_progress_orders = DataRetrieve().in_progress_orders()
            done_orders = DataRetrieve().done_orders()
            products = DataRetrieve().warehouse_status()

            if waiting_orders != self.waiting_orders:
                self.waiting_orders = waiting_orders
                self.on_load()
                time.sleep(1)
            elif in_progress_orders != self.in_progress_orders:
                self.in_progress_orders = in_progress_orders
                self.on_load()
                time.sleep(1)
            elif done_orders != self.done_orders:
                self.done_orders = done_orders
                self.on_load()
                time.sleep(1)
            elif products != self.products:
                self.products = products
                self.on_load()
                time.sleep(1)
            else:
                time.sleep(1)

    def auto_update_daemon(self):
        # Attiva il daemon di ricerca
        newthread = threading.Thread(target=self.update_lookup)
        newthread.daemon = True
        newthread.start()
        print("Daemon STARTED\n")

    def on_order_click(self, event=None):
        # Ricava l'ordine su cui si è cliccatto a seconda della tab in cui ci si trova
        order_idx = "0"
        tab = self.overview_notebook.index("current")

        if tab == 0:
            item = self.waiting_tv.selection()
            for i in item:
                order_idx = self.waiting_tv.item(i, "values")[0]

        elif tab == 1:
            item = self.progress_tv.selection()
            for i in item:
                order_idx = self.progress_tv.item(i, "values")[0]

        elif tab == 2:
            item = self.done_tv.selection()
            for i in item:
                order_idx = self.done_tv.item(i, "values")[0]

        if order_idx != "0":
            # Controlla che sia stato selezionato almeno un ordine
            SingleOrderView(code=order_idx, master=self.mainwindow).mainwindow.grab_set()

    def on_preferences_press(self):
        # Apre la finestra impostazioni
        PreferencesWindow(master=self.mainwindow).mainwindow.grab_set()

    def on_new_product_press(self):
        # Apre la finestra di inserimento singolo prodotto
        ProductInsert(single=True, status="in", treeview=None, function=None, master=self.mainwindow). \
            mainwindow.grab_set()

    def on_new_document_press(self):
        # Apre la finestra di inserimento documento
        NewDocument(master=self.mainwindow).mainwindow.grab_set()

    def on_customers_print_press(self):
        # Esporta file *.pdf lista clienti
        data = DataRetrieve()
        customers = data.all_customers()
        '''pdf = Prints()
        pdf.customers_list(customers)'''
        excel = XLSaver()
        excel.customers_list(customers)
        self.mainwindow.focus_set()

    def on_company_config_press(self):
        # Apre finestra di configurazione anagrafica azienda
        CompanyConfig(self.mainwindow).mainwindow.grab_set()

    def on_suppliers_print_press(self):
        # Esporta file *.xlsx lista fornitori
        data = DataRetrieve()
        suppliers = data.all_suppliers()
        '''pdf = Prints()
        pdf.suppliers_list(suppliers)'''
        excel = XLSaver()
        excel.suppliers_list(suppliers)
        self.mainwindow.focus_set()

    def on_orders_view_press(self):
        # Apre finestra ricerca e aggiunta ordini
        order_view = OrderView
        order_view(master=self.mainwindow).mainwindow.grab_set()

    def on_warehouse_view_press(self):
        # Apre finestra ricerca magazzino
        WarehouseManagementWindow(master=self.mainwindow).mainwindow.grab_set()

    def on_suppliers_view_press(self):
        # Apre finestra ricerca e aggiunta fornitori
        SupplierView(master=self.mainwindow).mainwindow.grab_set()

    def on_customers_list_press(self):
        # Apre finestra lista clienti
        CustomerView(win=self.mainwindow).mainwindow.grab_set()

    def on_in_progress_press(self):
        # Mette in lavorazione un nuovo ordine
        item = self.waiting_tv.selection()
        # Verifica che sia selezionata una voce all'interno della treeview
        if item != ():
            for i in item:
                order_idx = self.waiting_tv.item(i, "values")[0]
                askinprogress = tkinter.messagebox.askyesno(
                    title="Mettere in lavorazione?", message=f"Sei sicuro di voler mettere in lavorazione l'ordine N°"
                                                             f"{order_idx}?")
                if askinprogress:
                    DataWrite().order_update(order_idx, 1)
                    toast = ToastNotification(
                        title="Ordine in lavorazione",
                        message="L'ordine è stato contrassegnato come in lavorazione!",
                        duration=3000,
                        icon="☺",
                        bootstyle="success"
                    )
                    toast.show_toast()

            self.mainwindow.focus_set()
        else:
            tkinter.messagebox.showerror(parent=self.mainwindow, title="Seleziona voce", message="Seleziona una voce da"
                                                                                                 " trasferire.")

    def on_delete_button_press(self):
        # Elimina l'ordine richiesto ricavando la selezione dalla treeview degli ordini in attesa
        item = self.waiting_tv.selection()
        if item != ():
            for i in item:
                order_idx = self.waiting_tv.item(i, "values")[0]
                askdelete = tkinter.messagebox.askyesno(
                    title="Eliminare ordine?", message=f"Sei sicuro di voler eliminare l'ordine N°{order_idx}?")
                if askdelete:
                    DataDelete().delete_order(order_idx)
                    self.on_load()

                self.mainwindow.focus_set()
        else:
            tkinter.messagebox.showerror(parent=self.mainwindow, title="Seleziona voce", message="Seleziona una voce da"
                                                                                                 " eliminare.")

    def on_done_btn_press(self):
        # Sposta l'ordine nella sezione "Completati"
        item = self.progress_tv.selection()
        if item != ():
            for i in item:
                order_idx = self.progress_tv.item(i, "values")[0]
                askinprogress = tkinter.messagebox.askyesno(
                    title="Completare l'ordine?", message=f"Sei sicuro di voler contrassegnare come completato l'ordine"
                                                          f" N°{order_idx}?")
                if askinprogress:
                    DataWrite().order_update(order_idx, 2)
                    toast = ToastNotification(
                        title="Ordine completato",
                        message="L'ordine è stato contrassegnato come completato!",
                        duration=3000,
                        icon="☺",
                        bootstyle="success"
                    )
                    toast.show_toast()

            self.mainwindow.focus_set()
        else:
            tkinter.messagebox.showerror(parent=self.mainwindow, title="Seleziona voce", message="Seleziona una voce da"
                                                                                                 " trasferire.")

    def on_delivered_press(self):
        # Sposta l'ordine nella sezione "Restituiti"
        item = self.done_tv.selection()
        if item != ():
            for i in item:
                order_idx = self.done_tv.item(i, "values")[0]
                askinprogress = tkinter.messagebox.askyesno(
                    title="Consegnare l'ordine?", message=f"Sei sicuro di voler contrassegnare come restituito l'ordine"
                                                          f" N°{order_idx}?")
                if askinprogress:
                    DataWrite().order_update(order_idx, 3)

            toast = ToastNotification(
                title="Ordine consegnato",
                message="L'ordine è stato consegnato!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()
            self.mainwindow.focus_set()
        else:
            tkinter.messagebox.showerror(parent=self.mainwindow, title="Seleziona voce", message="Seleziona una voce da"
                                                                                                 " consegnare.")

    def on_insert_order_press(self):
        # Apre la finestra di inserimento ordini
        order_insert = OrderInsertWindow
        order_insert(master=self.mainwindow)

    def on_search_btn_press(self, event=None):
        # Ricerca il prodotto indicato nella entry della sezione magazzino
        query = self.wh_search_entry.get()
        products = DataRetrieve().single_product_code(query)
        if not products:
            products = DataRetrieve().single_product_name(query)
        self.in_stock_tv.delete(*self.in_stock_tv.get_children())
        for product in products:
            self.in_stock_tv.insert("", END, values=product)

    def on_settings_press(self):
        PreferencesWindow(master=self.mainwindow).mainwindow.grab_set()

    def on_close_command_press(self):
        # Chiude l'applicativo senza chiedere conferma
        self.mainwindow.destroy()

    def on_product_tv_press(self, event=None):
        # Callback sulla selezione di un prodotto dalle tabelle di magazzino
        product_idx = "0"
        tab = self.warehouse_notebook.index("current")
        try:
            if tab == 0:
                item = self.in_stock_tv.selection()
                for i in item:
                    product_idx = self.in_stock_tv.item(i, "values")[0]

            elif tab == 1:
                item = self.ending_tv.selection()
                for i in item:
                    product_idx = self.ending_tv.item(i, "values")[0]
            if product_idx != "0":
                # Verifica che sia stato selezionato almeno un prodotto
                SingleProductView(master=self.mainwindow, code=product_idx, function=self.on_load).mainwindow.grab_set()
        except IndexError:
            pass

    def on_new_prev_press(self):
        # Apre la finestra "Nuovo documento" già sulla sezione "Nuovo preventivo"
        NewDocument(preventive=True, master=self.mainwindow).mainwindow.grab_set()

    def on_report_press(self):
        # Apre la finestra di generazione rapportini di lavoro
        WorkReport(master=self.mainwindow).mainwindow.grab_set()

    def backup(self):
        # Crea una copia esatta del database e la archivia nella cartella di backup indicata nel file di configurazione comprimendola
        # in un file zip e dando al file come nome la data odierna
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        database = f"{preferences['database_path']}sir.db"
        backup = f"{preferences['backup_path']}sir.db"
        shutil.copyfile(database, backup)
        compressed = f"{preferences['backup_path']}Backup {datetime.date.today()}.zip"
        with ZipFile(compressed, 'w') as myzip:
            myzip.write(backup)
        os.remove(backup)

    def on_documents_press(self):
        DocumentView(master=self.mainwindow).mainwindow.grab_set()

    def credits_win(self):
        Credits(master=self.mainwindow).mainwindow.grab_set()

    def agenda_win(self):
        Agenda(master=self.mainwindow).mainwindow.grab_set()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
