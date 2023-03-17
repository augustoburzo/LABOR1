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
import tkinter.filedialog
from tkinter import END

import pygubu
from configparser import ConfigParser

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "company_config.ui"


class CompanyConfig:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("company_config", master)
        builder.connect_callbacks(self)

        # Connessione del builder a tutte le widget
        self.company_entry = builder.get_object("company_entry")
        self.company_entry.focus_set()

        self.address_entry = builder.get_object("address_entry")
        self.cap_entry = builder.get_object("cap_entry")
        self.city_entry = builder.get_object("city_entry")
        self.prov_entry = builder.get_object("prov_entry")
        self.nation_entry = builder.get_object("nation_entry")
        self.phone_entry = builder.get_object("phone_entry")
        self.fax_entry = builder.get_object("fax_entry")
        self.cell_entry = builder.get_object("cell_entry")
        self.email_entry = builder.get_object("email_entry")
        self.web_entry = builder.get_object("web_entry")
        self.fiscal_code_entry = builder.get_object("fiscal_code_entry")
        self.iva_entry = builder.get_object("iva_entry")
        self.cciaa_entry = builder.get_object("cciaa_entry")
        self.capital_entry = builder.get_object("capital_entry")
        self.registration_entry = builder.get_object("registration_entry")
        self.reg_num_entry = builder.get_object("reg_num_entry")
        self.logo_entry = builder.get_object("logo_entry")

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def on_load(self):
        # Legge il file di config "company.ini" e popola tutte le entry
        config_object = ConfigParser()
        config_object.read("company.ini")
        userinfo = config_object["COMPANYINFO"]

        self.company_entry.insert(0, userinfo["company"])
        self.address_entry.insert(0, userinfo["address"])
        self.cap_entry.insert(0, userinfo["cap"])
        self.city_entry.insert(0, userinfo["city"])
        self.prov_entry.insert(0, userinfo["prov"])
        self.nation_entry.insert(0, userinfo["nation"])
        self.phone_entry.insert(0, userinfo["phone"])
        self.fax_entry.insert(0, userinfo["fax"])
        self.cell_entry.insert(0, userinfo["cell"])
        self.email_entry.insert(0, userinfo["email"])
        self.web_entry.insert(0, userinfo["web"])
        self.fiscal_code_entry.insert(0, userinfo["fiscal_code"])
        self.iva_entry.insert(0, userinfo["iva"])
        self.cciaa_entry.insert(0, userinfo["cciaa"])
        self.capital_entry.insert(0, userinfo["capital"])
        self.registration_entry.insert(0, userinfo["reg"])
        self.reg_num_entry.insert(0, userinfo["reg_num"])
        self.logo_entry.insert(0, userinfo["logo"])

    def on_logo_search_press(self):
        # Apre la finestra di ricerca del logo
        logo = tkinter.filedialog.askopenfilename()
        self.logo_entry.delete(0, END)
        self.logo_entry.insert(0, logo)
        self.logo_entry.focus_set()

    def on_save_press(self):
        # Inizializza le variabili
        company = self.company_entry.get()
        address = self.address_entry.get()
        cap = self.cap_entry.get()
        city = self.city_entry.get()
        prov = self.prov_entry.get()
        nation = self.nation_entry.get()
        phone = self.phone_entry.get()
        fax = self.fax_entry.get()
        cell = self.cell_entry.get()
        email = self.email_entry.get()
        web = self.web_entry.get()
        fiscal_code = self.fiscal_code_entry.get()
        iva = self.iva_entry.get()
        cciaa = self.cciaa_entry.get()
        capital = self.capital_entry.get()
        registration = self.registration_entry.get()
        reg_num = self.reg_num_entry.get()
        logo = self.logo_entry.get()

        config_object = ConfigParser()
        # Aggiorna i dati contenuti nel file di configurazione "company.ini"
        config_object["COMPANYINFO"] = {
            "company    ": company,
            "address    ": address,
            "cap        ": cap,
            "city       ": city,
            "prov       ": prov,
            "nation     ": nation,
            "phone      ": phone,
            "fax        ": fax,
            "cell       ": cell,
            "email      ": email,
            "web        ": web,
            "fiscal_code": fiscal_code,
            "iva        ": iva,
            "cciaa      ": cciaa,
            "capital    ": capital,
            "reg        ": registration,
            "reg_num    ": reg_num,
            "logo       ": logo
        }

        with open('company.ini', 'w') as conf:
            config_object.write(conf)

        self.mainwindow.destroy()

    def on_undo_press(self):
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = CompanyConfig()
    app.run()
