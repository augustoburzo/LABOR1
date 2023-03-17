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

from distutils.command.build import build
import pathlib
import tkinter.filedialog
from configparser import ConfigParser
from tkinter import END
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "preferences_window.ui"


class PreferencesWindow:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("preferences_window", master)
        builder.connect_callbacks(self)

        # Sezione lavorazioni
        self.working_cod_entry = builder.get_object("working_cod_entry")
        self.working_name_entry = builder.get_object("working_name_entry")
        self.working_price_entry = builder.get_object("working_price_entry")

        self.works_tv = builder.get_object("works_tv")
        self.works_tv.bind("<Double-1>", self.wk_click)

        # Sezione IVA
        self.iva_cod_entry = builder.get_object("iva_cod_entry")
        self.iva_desc_entry = builder.get_object("iva_desc_entry")
        self.iva_perc_entry = builder.get_object("iva_perc_entry")

        self.iva_tv = builder.get_object("iva_tv")
        self.iva_tv.bind("<Double-1>", self.iva_click)

        # Sezione categorie
        self.cat_cod_entry = builder.get_object("cat_cod_entry")
        self.cat_name_entry = builder.get_object("cat_name_entry")

        self.cat_tv = builder.get_object("cat_tv")
        self.cat_tv.bind("<Double-1>", self.cat_click)

        # Sezione dipendenti
        self.worker_code_entry = builder.get_object("worker_code_entry")
        self.worker_name_entry = builder.get_object("worker_name_entry")

        self.workers_tv = builder.get_object("workers_tv")
        self.workers_tv.bind("<Double-1>", self.worker_click)

        # Sezione listini
        self.lists_tv = builder.get_object("lists_tv")
        self.list_code_entry = builder.get_object("list_code_entry")
        self.list_descr_entry = builder.get_object("list_descr_entry")
        self.list_discount_combo = builder.get_object("list_discount_combo")

        self.lists_tv.bind("<Double-1>", self.list_click)

        # Ricerca file configurazione
        self.db_entry = builder.get_object("db_entry")
        self.backup_entry = builder.get_object("backup_entry")

        self.mainwindow.focus_set()

        # Ricerca i dati i popola le tabelle
        self.wk_retrieve()
        self.iva_retrieve()
        self.cat_retrieve()
        self.workers_retrieve()
        self.preferences_retrieve()
        self.list_retrieve()

    def run(self):
        self.mainwindow.mainloop()

    def preferences_retrieve(self):
        # Ricava gli indirizzi di configurazione dal file "config.ini"
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        self.db_entry.insert(0, preferences["database_path"])
        self.backup_entry.insert(0, preferences["backup_path"])

    def cat_click(self, event=None):
        # Callback sul click della tabella categorie
        self.cat_cod_entry.delete(0, END)
        self.cat_name_entry.delete(0, END)
        selections = self.cat_tv.selection()
        for selection in selections:
            code = self.cat_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}cat.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(code):
                        i = i.split(",")
                        self.cat_cod_entry.insert(0, i[0])
                        self.cat_name_entry.insert(0, i[1])

    def worker_click(self, event=None):
        # Callback sul click della tabella dipendenti
        self.worker_code_entry.delete(0, END)
        self.worker_name_entry.delete(0, END)
        selections = self.workers_tv.selection()
        for selection in selections:
            code = self.workers_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}workers.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(code):
                        i = i.split(",")
                        self.worker_code_entry.insert(0, i[0])
                        self.worker_name_entry.insert(0, i[1])

    def cat_retrieve(self):
        # Ricava le categorie dal file "cat.dat"
        cat_code = None
        self.cat_cod_entry.delete(0, END)
        self.cat_name_entry.delete(0, END)
        self.cat_tv.delete(*self.cat_tv.get_children())
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}cat.dat"
        with open(filename, "r") as infile:
            lines = infile.readlines()

        for line in lines:
            line = line.split(",")
            try:
                cat_code = int(line[0]) + 1
            except ValueError:
                pass
            self.cat_cod_entry.delete(0, END)
            self.cat_cod_entry.insert(0, cat_code)
            self.cat_tv.insert("", END, values=line)
        if self.cat_cod_entry.get() == "":
            self.cat_cod_entry.insert(0, "1000")

    def workers_retrieve(self):
        # Ricava i lavoratori dal file "workers.dat"
        worker_code = None
        self.worker_code_entry.delete(0, END)
        self.worker_name_entry.delete(0, END)
        self.workers_tv.delete(*self.workers_tv.get_children())
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}workers.dat"
        with open(filename, "r") as infile:
            lines = infile.readlines()

        for line in lines:
            line = line.split(",")
            try:
                worker_code = int(line[0]) + 1
            except ValueError:
                pass
            self.worker_code_entry.delete(0, END)
            self.worker_code_entry.insert(0, worker_code)
            self.workers_tv.insert("", END, values=line)
        if self.worker_code_entry.get() == "":
            self.worker_code_entry.insert(0, "1000")

    def on_catsave_press(self):
        # Salva la nuova categoria nel file "cat.dat"
        cat_code = self.cat_cod_entry.get()
        cat_name = self.cat_name_entry.get()
        cat_string = f"{cat_code},{cat_name}\n"
        cat_string_a = f"{cat_code},{cat_name}"
        lines = []
        update = False
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}cat.dat"
        with open(filename, "r") as f:
            d = f.readlines()
            f.seek(0)

            for i in d:
                lines.append(i)

        for line in lines:
            if line.startswith(cat_code):
                update = True

        if update:
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(cat_code):
                        f.write(cat_string_a)
                    else:
                        f.write(i)
                f.truncate()
        elif not update:
            with open(filename, "a") as f:
                f.write(cat_string)

        self.cat_retrieve()

    def on_workersave_press(self):
        cat_code = self.worker_code_entry.get()
        cat_name = self.worker_name_entry.get()
        cat_string = f"{cat_code},{cat_name}\n"
        cat_string_a = f"{cat_code},{cat_name}"
        lines = []
        update = False
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}workers.dat"
        with open(filename, "r+") as f:
            d = f.readlines()
            f.seek(0)

            for i in d:
                lines.append(i)

        for line in lines:
            if line.startswith(cat_code):
                update = True

        if update:
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(cat_code):
                        if int(cat_code) == 1000:
                            f.write(cat_string)
                        else:
                            f.write(cat_string_a)
                    else:
                        f.write(i)
                f.truncate()
        elif not update:
            with open(filename, "a") as f:
                f.write(cat_string)

        self.workers_retrieve()

    def on_catdelete_press(self):
        selections = self.cat_tv.selection()
        for selection in selections:
            code = self.cat_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}cat.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if not i.startswith(code):
                        f.write(i)
                f.truncate()

        self.cat_retrieve()

    def on_workerdelete_press(self):
        selections = self.workers_tv.selection()
        for selection in selections:
            code = self.workers_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}workers.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if not i.startswith(code):
                        f.write(i)
                f.truncate()

        self.workers_retrieve()

    def iva_click(self, event=None):
        self.iva_cod_entry.delete(0, END)
        self.iva_desc_entry.delete(0, END)
        self.iva_perc_entry.delete(0, END)
        selections = self.iva_tv.selection()
        for selection in selections:
            code = self.iva_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}iva.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(code):
                        i = i.split(",")
                        self.iva_cod_entry.insert(0, i[0])
                        self.iva_desc_entry.insert(0, i[1])
                        self.iva_perc_entry.insert(0, i[2])

    def wk_click(self, event):
        self.working_cod_entry.delete(0, END)
        self.working_name_entry.delete(0, END)
        self.working_price_entry.delete(0, END)
        selections = self.works_tv.selection()
        for selection in selections:
            code = self.works_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}wk.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(code):
                        i = i.split(",")
                        self.working_cod_entry.insert(0, i[0])
                        self.working_name_entry.insert(0, i[1])
                        self.working_price_entry.insert(0, i[2])

    def wk_retrieve(self):
        wk_code = None
        self.working_cod_entry.delete(0, END)
        self.working_price_entry.delete(0, END)
        self.working_name_entry.delete(0, END)
        self.working_price_entry.insert(0, "0")
        self.works_tv.delete(*self.works_tv.get_children())
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}wk.dat"
        with open(filename, "r") as infile:
            lines = infile.readlines()

        for line in lines:
            line = line.split(",")
            try:
                wk_code = int(line[0]) + 1
            except ValueError:
                pass
            self.working_cod_entry.delete(0, END)
            self.working_cod_entry.insert(0, wk_code)
            self.works_tv.insert("", END, values=line)
        if self.working_cod_entry.get() == "":
            self.working_cod_entry.insert(0, "1000")

    def iva_retrieve(self):
        tax_code = None
        self.iva_cod_entry.delete(0, END)
        self.iva_desc_entry.delete(0, END)
        self.iva_perc_entry.delete(0, END)
        self.iva_perc_entry.insert(0, "22")
        self.iva_tv.delete(*self.iva_tv.get_children())
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}tax.dat"
        with open(filename, "r") as infile:
            lines = infile.readlines()

        for line in lines:
            line = line.split(",")
            try:
                tax_code = int(line[0]) + 1
            except ValueError:
                pass
            self.iva_cod_entry.delete(0, END)
            self.iva_cod_entry.insert(0, tax_code)
            self.iva_tv.insert("", END, values=line)
        if self.iva_cod_entry.get() == "":
            self.iva_cod_entry.insert(0, "1000")

    def on_db_search_press(self):
        db_dir = tkinter.filedialog.askdirectory(parent=self.mainwindow)
        self.db_entry.insert(0, db_dir)

    def on_backup_search(self):
        backup_dir = tkinter.filedialog.askdirectory(parent=self.mainwindow)
        self.backup_entry.insert(0, backup_dir)

    def on_wksave_press(self):
        wk_code = self.working_cod_entry.get()
        wk_name = self.working_name_entry.get()
        wk_price = "%.2f" % float(self.working_price_entry.get())
        wk_string = f"{wk_code},{wk_name},{wk_price}\n"
        wk_string_a = f"{wk_code},{wk_name},{wk_price}"
        lines = []
        update = False
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}wk.dat"
        with open(filename, "r") as f:
            d = f.readlines()
            f.seek(0)

            for i in d:
                lines.append(i)

        for line in lines:
            if line.startswith(wk_code):
                update = True

        if update:
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(wk_code):
                        f.write(wk_string_a)
                    else:
                        f.write(i)
                f.truncate()
        elif not update:
            with open(filename, "a") as f:
                f.write(wk_string)

        self.wk_retrieve()

    def on_wkdelete_press(self):
        selections = self.works_tv.selection()
        for selection in selections:
            code = self.works_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}wk.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if not i.startswith(code):
                        f.write(i)
                f.truncate()

        self.wk_retrieve()

    def on_ivasave_press(self):
        tax_code = self.iva_cod_entry.get()
        tax_name = self.iva_desc_entry.get()
        tax_perc = self.iva_perc_entry.get()
        tax_string = f"{tax_code},{tax_name},{tax_perc}\n"
        tax_string_a = f"{tax_code},{tax_name},{tax_perc}"
        lines = []
        update = False
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}tax.dat"
        with open(filename, "r") as f:
            d = f.readlines()
            f.seek(0)

            for i in d:
                lines.append(i)

        for line in lines:
            if line.startswith(tax_code):
                update = True

        if update:
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(tax_code):
                        f.write(tax_string_a)
                    else:
                        f.write(i)
                f.truncate()
        elif not update:
            with open(filename, "a") as f:
                f.write(tax_string)

        self.iva_retrieve()

    def on_ivadelete_press(self):
        selections = self.iva_tv.selection()
        for selection in selections:
            code = self.iva_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}tax.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if not i.startswith(code):
                        f.write(i)
                f.truncate()

        self.iva_retrieve()

    def on_path_save_press(self):
        db_path = self.db_entry.get()
        if db_path != "":
            if not db_path.endswith("/"):
                db_path = f"{db_path}/"
        backup = self.backup_entry.get()
        if backup != "":
            if not backup.endswith("/"):
                backup = f"{backup}/"
        config_object = ConfigParser()
        # Aggiorna i dati contenuti nel file di configurazione "company.ini"
        config_object["PREFERENCES"] = {
            "database_path  ": db_path,
            "backup_path    ": backup
        }
        with open('config.ini', 'w') as conf:
            config_object.write(conf)

    def on_listsave_press(self):
        list_code = self.list_code_entry.get()
        list_name = self.list_descr_entry.get()
        list_discount = self.list_discount_combo.get()
        list_string = f"{list_code},{list_name},{list_discount}\n"
        list_string_a = f"{list_code},{list_name},{list_discount}"
        lines = []
        update = False
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}lists.dat"
        with open(filename, "r") as f:
            d = f.readlines()
            f.seek(0)

            for i in d:
                lines.append(i)

        for line in lines:
            if line.startswith(list_code):
                update = True

        if update:
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(list_code):
                        f.write(list_string_a)
                    else:
                        f.write(i)
                f.truncate()
        elif not update:
            with open(filename, "a") as f:
                f.write(list_string)

        self.list_retrieve()

    def on_listdelete_press(self):
        selections = self.lists_tv.selection()
        for selection in selections:
            code = self.lists_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}lists.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if not i.startswith(code):
                        f.write(i)
                f.truncate()

        self.list_retrieve()

    def list_retrieve(self):
        list_code = None
        self.list_code_entry.delete(0, END)
        self.list_descr_entry.delete(0, END)
        self.lists_tv.delete(*self.lists_tv.get_children())
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}lists.dat"
        with open(filename, "r") as infile:
            lines = infile.readlines()

        for line in lines:
            line = line.split(",")
            try:
                list_code = int(line[0]) + 1
            except ValueError:
                pass
            self.list_code_entry.delete(0, END)
            self.list_code_entry.insert(0, list_code)
            self.lists_tv.insert("", END, values=line)
        if self.list_code_entry.get() == "":
            self.list_code_entry.insert(0, "1000")

    def list_click(self, event):
        self.list_code_entry.delete(0, END)
        self.working_name_entry.delete(0, END)
        selections = self.lists_tv.selection()
        for selection in selections:
            code = self.lists_tv.item(selection, "values")[0]
            config_object = ConfigParser()
            config_object.read("config.ini")
            preferences = config_object["PREFERENCES"]
            filename = f"{preferences['database_path']}lists.dat"
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.startswith(code):
                        i = i.split(",")
                        self.list_code_entry.insert(0, i[0])
                        self.list_descr_entry.insert(0, i[1])
                        self.list_discount_combo.configure(state="normal")
                        self.list_discount_combo.insert(0, i[2])
                        self.list_discount_combo.configure(state="readonly")


if __name__ == "__main__":
    app = PreferencesWindow()
    app.run()
