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
from tkinter import messagebox
from tkinter import END

import pygubu
from ttkbootstrap.toast import ToastNotification

from db_functions import DataDelete, DataRetrieve, DataWrite
from pdf_functions import Prints
from product_insert import ProductInsert
from work_pick import WorkPick
from worker_pick import WorkerPick

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "work_report.ui"


class WorkReport:
    def __init__(self, master=None):
        self.date = datetime.datetime.now()
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("report_window", master)
        builder.connect_callbacks(self)
        self.mainwindow.focus_set()

        self.report_tv = builder.get_object("report_tv")
        self.report_tv.bind("<Double-1>", self.on_report_tv_click)
        self.code_entry = builder.get_object("code_entry")
        self.wk_code_entry = builder.get_object("wk_code_entry")
        self.rep_date_entry = builder.get_object("rep_date_entry")
        self.worker_entry = builder.get_object("worker_entry")
        self.descr_entry = builder.get_object("descr_entry")
        self.trip_time_entry = builder.get_object("trip_time_entry")
        self.trip_km_entry = builder.get_object("trip_km_entry")
        self.trip_price_entry = builder.get_object("trip_price_entry")
        self.accom_exp_entry = builder.get_object("accom_exp_entry")
        self.products_tv = builder.get_object("products_tv")
        self.notes_text = builder.get_object("notes_text")

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def on_load(self):
        reports = DataRetrieve().all_reports()
        self.report_tv.delete(*self.report_tv.get_children())
        for report in reports:
            report = (report[0], report[1], report[4], report[3])
            self.report_tv.insert("", END, values=report)
        self.code_entry.configure(state="normal")
        self.code_entry.delete(0, END)
        self.code_entry.configure(state="readonly")
        self.wk_code_entry.delete(0, END)
        self.rep_date_entry.delete(0, END)
        self.rep_date_entry.insert(0, self.date.strftime('%d/%m/%Y'))
        self.worker_entry.configure(state="normal")
        self.worker_entry.delete(0, END)
        self.worker_entry.configure(state="readonly")
        self.descr_entry.delete(0, END)
        self.trip_time_entry.delete(0, END)
        self.trip_km_entry.delete(0, END)
        self.trip_price_entry.delete(0, END)
        self.accom_exp_entry.delete(0, END)
        self.products_tv.delete(*self.products_tv.get_children())
        self.notes_text.delete(1.0, END)

    def on_report_tv_click(self, event=None):
        item = self.report_tv.selection()
        report_idx = None
        for i in item:
            report_idx = self.report_tv.item(i, "values")[0]
        if report_idx:
            report = DataRetrieve().single_report_code(report_idx)
            self.code_entry.configure(state="normal")
            self.code_entry.delete(0, END)
            self.wk_code_entry.delete(0, END)
            self.rep_date_entry.delete(0, END)
            self.worker_entry.delete(0, END)
            self.descr_entry.delete(0, END)
            self.trip_time_entry.delete(0, END)
            self.trip_km_entry.delete(0, END)
            self.trip_price_entry.delete(0, END)
            self.accom_exp_entry.delete(0, END)
            self.products_tv.delete(*self.products_tv.get_children())
            self.notes_text.delete(1.0, END)

            # Inserisce i dati presenti in database
            self.code_entry.insert(0, report[0])
            self.code_entry.configure(state="readonly")
            self.wk_code_entry.insert(0, str(report[1]))
            self.rep_date_entry.insert(0, str(report[2]))
            self.worker_entry.configure(state="normal")
            self.worker_entry.insert(0, str(report[3]))
            self.worker_entry.configure(state="readonly")
            self.descr_entry.insert(0, str(report[4]))
            self.trip_time_entry.insert(0, str(report[5]))
            self.trip_km_entry.insert(0, str(report[6]))
            self.trip_price_entry.insert(0, str(report[7]))
            self.accom_exp_entry.insert(0, str(report[8]))
            try:
                interventions = report[9].split("], [")
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
                        intervention_price = intervention_price.replace("]]", "")
                    intervention = (intervention_code, intervention_name, intervention_price)
                    self.products_tv.insert("", END, values=intervention)
            except TypeError:
                pass
            except IndexError:
                pass
            except AttributeError:
                pass
            self.notes_text.insert(1.0, report[10][:-1])

    def on_choose_press(self):
        WorkerPick(entry=self.worker_entry).mainwindow.grab_set()

    def on_product_insert_press(self):
        ProductInsert("out", self.products_tv, None, report=True).mainwindow.grab_set()

    def on_wk_insert_press(self):
        WorkPick(treeview=self.products_tv, validate=None, master=self.mainwindow). \
            mainwindow.grab_set()

    def on_freerow_insert_press(self):
        ProductInsert("out", self.products_tv, None, freerow=True, report=True).mainwindow.grab_set()

    def on_delete_row_press(self):
        item = self.products_tv.selection()
        self.products_tv.delete(item)

    def on_save_press(self):
        code = self.code_entry.get()
        if code != "":
            self.on_update_press()
        else:
            wk_code = self.wk_code_entry.get()
            rep_date = self.rep_date_entry.get()
            worker = self.worker_entry.get()
            if worker != "":
                descr = self.descr_entry.get()
                trip_time = self.trip_time_entry.get()
                trip_km = self.trip_km_entry.get()
                trip_price = self.trip_price_entry.get()
                accom_exp = self.accom_exp_entry.get()
                products = []
                for child in self.products_tv.get_children():
                    products.append(self.products_tv.item(child)["values"])
                notes = self.notes_text.get(1.0, END)
                written = DataWrite().new_report(code, wk_code, rep_date, worker, descr, trip_time, trip_km, trip_price,
                                                 accom_exp, str(products), notes)
                if written:
                    toast = ToastNotification(
                        title="Report salvato",
                        message="Il report è stato salvato con successo!",
                        duration=3000,
                        icon="☺",
                        bootstyle="success"
                    )
                    toast.show_toast()
                    self.on_load()
            else:
                tkinter.messagebox.showerror(parent=self.mainwindow,
                                             title="Inserire dipendente",
                                             message="Compilare il campo dipendente.")

    def on_update_press(self):
        code = self.code_entry.get()
        wk_code = self.wk_code_entry.get()
        rep_date = self.rep_date_entry.get()
        worker = self.worker_entry.get()
        descr = self.descr_entry.get()
        trip_time = self.trip_time_entry.get()
        trip_km = self.trip_km_entry.get()
        trip_price = self.trip_price_entry.get()
        accom_exp = self.accom_exp_entry.get()
        products = []
        for child in self.products_tv.get_children():
            products.append(self.products_tv.item(child)["values"])
        notes = self.notes_text.get(1.0, END)
        updated = DataWrite().report_update(code, wk_code, rep_date, worker, descr, trip_time, trip_km, trip_price,
                                            accom_exp, str(products), notes)
        if updated:
            toast = ToastNotification(
                title="Report aggiornato",
                message="Il report è stato aggiornato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()
            self.on_load()

    def on_delete_press(self):
        code = self.code_entry.get()
        if code == "":
            tkinter.messagebox.showwarning(parent=self.mainwindow,
                                           title="Nessun report selezionato",
                                           message="Selezionare un report da eliminare!")
        else:
            DataDelete().delete_report(code)
            toast = ToastNotification(
                title="Report eliminato",
                message="Il report è stato eliminato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="warning"
            )
            toast.show_toast()
            self. on_load()

    def on_export_press(self):
        code = self.code_entry.get()
        if code != "":
            wk_code = self.wk_code_entry.get()
            date = self.rep_date_entry.get()
            worker = self.worker_entry.get()
            description = self.descr_entry.get()
            trip_time = self.trip_time_entry.get()
            trip_km = self.trip_km_entry.get()
            trip_cost = self.trip_price_entry.get()
            if trip_cost == "":
                trip_cost = 0
            accommodation = self.accom_exp_entry.get()
            if accommodation == "":
                accommodation = 0
            products = []
            for child in self.products_tv.get_children():
                products.append(self.products_tv.item(child)["values"])
            notes = self.notes_text.get(1.0, END)
            Prints().work_report(code, wk_code, date, worker, description, trip_time, trip_km, trip_cost, accommodation,
                                 products, notes)
        else:
            tkinter.messagebox.showwarning(parent=self.mainwindow,
                                           title="Report non salvato",
                                           message="Salvare il report e procedere all'esportazione.")


if __name__ == "__main__":
    app = WorkReport()
    app.run()
