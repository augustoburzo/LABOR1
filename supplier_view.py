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

from db_functions import DataRetrieve, DataWrite, DataDelete
from pdf_functions import Prints

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "supplier_view.ui"


class SupplierView:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("supplier_view", master)
        builder.connect_callbacks(self)

        self.mainwindow.state('zoomed')

        self.suppliers_tv = builder.get_object("suppliers_tv")
        self.suppliers_tv.focus_set()
        self.suppliers_tv.bind("<Double-1>", self.on_suppliers_click)

        self.code_entry = builder.get_object("code_entry")
        self.company_name_entry = builder.get_object("company_name_entry")
        self.company_name_entry.focus_set()
        self.address_entry = builder.get_object("address_entry")
        self.address_num_entry = builder.get_object("address_num_entry")
        self.prov_entry = builder.get_object("prov_entry")
        self.city_entry = builder.get_object("city_entry")
        self.cap_entry = builder.get_object("cap_entry")
        self.nation_entry = builder.get_object("nation_entry")
        self.fiscal_code_entry = builder.get_object("fiscal_code_entry")
        self.iva_entry = builder.get_object("iva_entry")
        self.sdicode_entry = builder.get_object("sdicode_entry")
        self.phone_entry = builder.get_object("phone_entry")
        self.email_entry = builder.get_object("email_entry")
        self.bank_entry = builder.get_object("bank_entry")
        self.iban_entry = builder.get_object("iban_entry")
        self.notes_txt = builder.get_object("notes_txt")

        self.update_btn = builder.get_object("update_btn")
        self.save_btn = builder.get_object("save_btn")
        self.export_btn = builder.get_object("export_btn")

        if self.code_entry.get() == "":
            self.update_btn.configure(state="disabled")

        self.code_entry.configure(state="readonly")

        self.separator1 = builder.get_object("separator3")
        self.separator1.configure(orient='vertical', style='info.Vertical.TSeparator')

        self.separator2 = builder.get_object("separator2")
        self.separator2.configure(orient='vertical', style='info.Vertical.TSeparator')

        self.delete_btn = builder.get_object("delete_btn")
        self.delete_btn.configure(style="danger.TButton")

        self.on_load_search()

    def run(self):
        self.mainwindow.mainloop()

    def on_load_search(self):
        suppliers = DataRetrieve().all_suppliers()

        if self.code_entry.get() == "":
            self.update_btn.configure(state="disabled")

        self.suppliers_tv.delete(*self.suppliers_tv.get_children())

        for supplier in suppliers:
            self.suppliers_tv.insert("", END, values=supplier)

    def on_suppliers_click(self, event):
        item = self.suppliers_tv.selection()
        for i in item:
            supplier_idx = self.suppliers_tv.item(i, "values")[0]
            supplier_data = DataRetrieve().single_supplier_code(supplier_idx)
            self.code_entry.configure(state="normal")
            self.code_entry.delete(0, END)
            self.code_entry.insert(0, str(supplier_data[0]))
            self.code_entry.configure(state="readonly")
            self.company_name_entry.delete(0, END)
            self.company_name_entry.insert(0, str(supplier_data[1]))
            self.address_entry.delete(0, END)
            self.address_entry.insert(0, str(supplier_data[2]))
            self.address_num_entry.delete(0, END)
            self.address_num_entry.insert(0, str(supplier_data[3]))
            self.prov_entry.delete(0, END)
            self.prov_entry.insert(0, str(supplier_data[4]))
            self.city_entry.delete(0, END)
            self.city_entry.insert(0, str(supplier_data[5]))
            self.cap_entry.delete(0, END)
            self.cap_entry.insert(0, str(supplier_data[6]))
            self.nation_entry.delete(0, END)
            self.nation_entry.insert(0, str(supplier_data[7]))
            self.fiscal_code_entry.delete(0, END)
            self.fiscal_code_entry.insert(0, str(supplier_data[8]))
            self.iva_entry.delete(0, END)
            self.iva_entry.insert(0, str(supplier_data[9]))
            self.sdicode_entry.delete(0, END)
            self.sdicode_entry.insert(0, str(supplier_data[10]))
            self.phone_entry.delete(0, END)
            self.phone_entry.insert(0, str(supplier_data[11]))
            self.email_entry.delete(0, END)
            self.email_entry.insert(0, str(supplier_data[12]))
            self.bank_entry.delete(0, END)
            self.bank_entry.insert(0, str(supplier_data[13]))
            self.iban_entry.delete(0, END)
            self.iban_entry.insert(0, str(supplier_data[14]))
            self.notes_txt.delete(1.0, END)
            try:
                self.notes_txt.insert(1.0, str(supplier_data[15][:-1]))
            except TypeError:
                pass

            self.update_btn.configure(state="normal")
            self.save_btn.configure(state="disabled")
            self.export_btn.configure(state="normal")

    def on_update_press(self):
        code = self.code_entry.get()
        company = self.company_name_entry.get().upper()
        address = self.address_entry.get().upper()
        address_num = self.address_num_entry.get().upper()
        prov = self.prov_entry.get().upper()
        city = self.city_entry.get().upper()
        cap = self.cap_entry.get().upper()
        nation = self.nation_entry.get().upper()
        fiscal_code = self.fiscal_code_entry.get().upper()
        iva = self.iva_entry.get().upper()
        sdicode = self.sdicode_entry.get().upper()
        phone = self.phone_entry.get().upper()
        email = self.email_entry.get()
        bank = self.bank_entry.get().upper()
        iban = self.iban_entry.get().upper()
        notes = self.notes_txt.get(1.0, END)

        data_write = DataWrite()
        data_write.supplier_update(code, company, address, address_num, prov, city, cap, nation,
                                   fiscal_code, iva, sdicode, phone, email, bank, iban, notes)

        self.on_clear_press()
        self.on_load_search()

    def on_export_press(self):
        code = self.code_entry.get()
        company = self.company_name_entry.get().upper()
        address = self.address_entry.get().upper()
        address_num = self.address_num_entry.get().upper()
        prov = self.prov_entry.get().upper()
        city = self.city_entry.get().upper()
        cap = self.cap_entry.get().upper()
        nation = self.nation_entry.get().upper()
        fiscal_code = self.fiscal_code_entry.get().upper()
        iva = self.iva_entry.get().upper()
        sdicode = self.sdicode_entry.get().upper()
        phone = self.phone_entry.get().upper()
        email = self.email_entry.get()
        bank = self.bank_entry.get().upper()
        iban = self.iban_entry.get().upper()
        notes = self.notes_txt.get(1.0, END)
        customers_print = Prints()
        customers_print.single_supplier(code, company, address, address_num, prov, city, cap, nation, fiscal_code, iva,
                                        sdicode, phone, email, bank, iban, notes)

        self.mainwindow.focus_set()

    def on_delete_press(self):
        code = self.code_entry.get()
        if code != "":
            answer = tkinter.messagebox.askyesno(parent=self.mainwindow,
                                                 title="Eliminare fornitore?", message="Si intende eliminare la voce"
                                                                                       " definitivamente?")
            if answer:

                data_delete = DataDelete()
                data_delete.delete_supplier(code)
                self.mainwindow.focus_set()
                self.on_clear_press()
                self.on_load_search()

            else:
                self.mainwindow.focus_set()

    def on_save_press(self):
        code = self.code_entry.get()
        company = self.company_name_entry.get().upper()
        if code == "" and company != "":
            address = self.address_entry.get().upper()
            address_num = self.address_num_entry.get().upper()
            prov = self.prov_entry.get().upper()
            city = self.city_entry.get().upper()
            cap = self.cap_entry.get().upper()
            nation = self.nation_entry.get().upper()
            fiscal_code = self.fiscal_code_entry.get().upper()
            iva = self.iva_entry.get().upper()
            sdicode = self.sdicode_entry.get().upper()
            phone = self.phone_entry.get().upper()
            email = self.email_entry.get()
            bank = self.bank_entry.get().upper()
            iban = self.iban_entry.get().upper()
            notes = self.notes_txt.get("1.0", END)

            data_write = DataWrite()
            data_write.new_supplier(company, address, address_num, prov, city, cap, nation, fiscal_code, iva, sdicode,
                                    phone, email, bank, iban, notes)
            self.on_clear_press()
            self.on_load_search()

        elif code != "":
            tkinter.messagebox.showwarning(parent=self.mainwindow,
                                           title="Cliente già censito", message="Non è possibile salvare nuovamente "
                                                                                "un cliente già censito!")
            self.mainwindow.focus_set()
        elif company == "":
            tkinter.messagebox.showinfo(parent=self.mainwindow,
                                        title="Dati incompleti", message="Compilare i campi di base e procedere al "
                                                                         "salvataggio dell'anagrafica")
            self.mainwindow.focus_set()

    def on_clear_press(self):
        self.code_entry.configure(state="normal")
        self.code_entry.delete(0, END)
        self.code_entry.configure(state="readonly")
        self.company_name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.address_num_entry.delete(0, END)
        self.prov_entry.delete(0, END)
        self.city_entry.delete(0, END)
        self.cap_entry.delete(0, END)
        self.nation_entry.delete(0, END)
        self.fiscal_code_entry.delete(0, END)
        self.iva_entry.delete(0, END)
        self.sdicode_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.bank_entry.delete(0, END)
        self.iban_entry.delete(0, END)
        self.notes_txt.delete(1.0, END)

        self.update_btn.configure(state="disabled")
        self.save_btn.configure(state="normal")
        self.export_btn.configure(state="disabled")


if __name__ == "__main__":
    app = SupplierView()
    app.run()
