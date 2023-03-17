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
from tkinter import END

import pygubu

from db_functions import DataRetrieve, DataWrite

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "customer_pick.ui"


class CustomerPick:
    def __init__(self, query, codew, companyw, lastnamew, firstnamew, phonew, cityw,
                 master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("customer_view", master)
        builder.connect_callbacks(self)

        self.codew = codew
        self.companyw = companyw
        self.lastnamew = lastnamew
        self.firstnamew = firstnamew
        self.phonew = phonew
        self.cityw = cityw

        self.customers_tv = builder.get_object("customers_tv")
        self.customers_tv.focus_set()

        self.code_entry = builder.get_object("code_entry")
        self.company_name_entry = builder.get_object("company_name_entry")
        self.first_name_entry = builder.get_object("first_name_entry")
        self.last_name_entry = builder.get_object("last_name_entry")
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
        self.cell_entry = builder.get_object("cell_entry")
        self.fax_entry = builder.get_object("fax_entry")
        self.email_entry = builder.get_object("email_entry")
        self.bank_entry = builder.get_object("bank_entry")
        self.iban_entry = builder.get_object("iban_entry")
        self.list_combo = builder.get_object("list_combo")
        self.notes_txt = builder.get_object("notes_txt")

        self.code_entry.configure(state="readonly")

        self.separator2 = builder.get_object("separator2")
        self.separator2.configure(orient='vertical', style='info.Vertical.TSeparator')

        self.customers_tv.bind("<Double-1>", self.on_customers_click)

        self.on_load_search(query)

    def run(self):
        self.mainwindow.mainloop()

    def on_customers_click(self, event):
        item = self.customers_tv.selection()
        for i in item:
            customer_idx = self.customers_tv.item(i, "values")[0]
            customer_data = DataRetrieve().single_customer_code(customer_idx)
            self.code_entry.configure(state="normal")
            self.code_entry.insert(0, customer_data[0])
            self.code_entry.configure(state="readonly")
            self.company_name_entry.insert(0, customer_data[1])
            self.first_name_entry.insert(0, customer_data[2])
            self.last_name_entry.insert(0, customer_data[3])
            self.address_entry.insert(0, customer_data[4])
            self.address_num_entry.insert(0, customer_data[5])
            self.prov_entry.insert(0, customer_data[6])
            self.city_entry.insert(0, customer_data[7])
            self.cap_entry.insert(0, customer_data[8])
            self.nation_entry.insert(0, customer_data[9])
            self.fiscal_code_entry.insert(0, customer_data[10])
            self.iva_entry.insert(0, customer_data[11])
            self.sdicode_entry.insert(0, customer_data[12])
            self.phone_entry.insert(0, customer_data[13])
            self.cell_entry.insert(0, customer_data[14])
            self.fax_entry.insert(0, customer_data[15])
            self.email_entry.insert(0, customer_data[16])
            self.bank_entry.insert(0, customer_data[17])
            self.iban_entry.insert(0, customer_data[18])
            self.list_combo.insert(0, customer_data[19])
            self.notes_txt.insert(1.0, str(customer_data[20]))

    def on_load_search(self, query):
        companycustomers = DataRetrieve().company_customer(company=query)

        self.customers_tv.delete(*self.customers_tv.get_children())
        cust_collector = ()

        for customer in companycustomers:
            cust_collector = cust_collector + (customer[0],)
            self.customers_tv.insert("", END, values=customer)

        customers = DataRetrieve().customer(last_name=query)

        for customer in customers:
            if customer[0] not in cust_collector:
                self.customers_tv.insert("", END, values=customer)

    def on_save_press(self):
        code = self.code_entry.get()
        company = self.company_name_entry.get().upper()
        first_name = self.first_name_entry.get().upper()
        last_name = self.last_name_entry.get().upper()
        check = company + first_name + last_name
        if code == "" and check != "":
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
            cell = self.cell_entry.get()
            fax = self.fax_entry.get()
            email = self.email_entry.get()
            bank = self.bank_entry.get().upper()
            iban = self.iban_entry.get().upper()
            list_combo = self.list_combo.get().upper()
            notes = self.notes_txt.get(1.0, END)

            data_write = DataWrite()
            data_write.new_customer(company, first_name, last_name, address, address_num, prov, city, cap, nation,
                                    fiscal_code, iva, sdicode, phone, cell, fax, email, bank, iban, list_combo, notes)

            self.on_clear_press()
            self.on_load_search("")

        elif code != "":
            tkinter.messagebox.showwarning(title="Cliente già censito", message="Non è possibile salvare nuovamente "
                                                                                "un cliente già censito!")
            self.mainwindow.focus_set()
        elif check == "":
            tkinter.messagebox.showinfo(title="Dati incompleti", message="Compilare i campi di base e procedere al "
                                                                         "salvataggio dell'anagrafica")
            self.mainwindow.focus_set()

    def on_clear_press(self):
        self.code_entry.configure(state="normal")
        self.code_entry.delete(0, END)
        self.code_entry.configure(state="readonly")
        self.company_name_entry.delete(0, END)
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
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
        self.cell_entry.delete(0, END)
        self.fax_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.bank_entry.delete(0, END)
        self.iban_entry.delete(0, END)
        self.list_combo.delete(0, END)
        self.notes_txt.delete(1.0, END)

    def on_select_press(self):
        if self.code_entry.get() == "":
            tkinter.messagebox.showerror(title="Cliente non salvato", message="Salvare prima il cliente in anagrafica")
            self.mainwindow.focus_set()
        else:
            self.codew.configure(state="normal")
            self.codew.insert(0, self.code_entry.get())
            self.codew.configure(state="readonly")
            self.companyw.configure(state="normal")
            self.companyw.insert(0, self.company_name_entry.get())
            self.companyw.configure(state="readonly")
            self.lastnamew.configure(state="normal")
            self.lastnamew.insert(0, self.last_name_entry.get())
            self.lastnamew.configure(state="readonly")
            self.firstnamew.configure(state="normal")
            self.firstnamew.insert(0, self.first_name_entry.get())
            self.firstnamew.configure(state="readonly")
            self.phonew.configure(state="normal")
            self.phonew.insert(0, self.cell_entry.get())
            self.phonew.configure(state="readonly")
            self.cityw.configure(state="normal")
            self.cityw.insert(0, self.city_entry.get())
            self.cityw.configure(state="readonly")

            self.mainwindow.destroy()


if __name__ == "__main__":
    app = CustomerPick()
    app.run()
