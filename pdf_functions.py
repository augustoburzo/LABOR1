#!/usr/bin/python3
# Labor1 - Augusto Burzo

from configparser import ConfigParser

from fpdf import FPDF
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import datetime

import os

from ttkbootstrap.toast import ToastNotification
from PyQt5 import QtPrintSupport


class PDF(FPDF):
    def header(self):
        config_object = ConfigParser()
        config_object.read("company.ini")
        companyinfo = config_object["COMPANYINFO"]

        self.set_font('Arial', '', 10)
        self.set_fill_color(44, 44, 160)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(255, 255, 255)
        try:
            self.image(companyinfo["logo"], w=80, h=20)
        except FileNotFoundError:
            tkinter.messagebox.showerror(title="File logo non trovato",
                                         message="Verificare configurazione azienda nel menù Modifica.")
        self.set_xy(-70, 10)
        self.multi_cell(60, 4, f'{companyinfo["company"]}\n{companyinfo["address"]} - {companyinfo["cap"]}\n'
                               f'{companyinfo["city"]} ({companyinfo["prov"]})\n{companyinfo["iva"]}\n'
                               f'Tel.: {companyinfo["phone"]} - Cell.: {companyinfo["cell"]}', 0, "R", True)
        self.set_xy(-75, 10)
        self.set_fill_color(33, 33, 120)
        self.multi_cell(5, 4, f'\n\n\n\n\n', 0, "R", True)
        self.set_xy(-80, 10)
        self.set_fill_color(22, 22, 80)
        self.multi_cell(5, 4, f'\n\n\n\n\n', 0, "R", True)

        self.ln()

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(95, 10, 'Labor1 - Software Gestionale')
        self.set_x(-105)
        self.cell(95, 10, 'Pagina ' + str(self.page_no()), 0, 0, 'R')


class Prints:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.pdf = PDF()

    def single_customer(self, code, company, first_name, last_name, address, address_num, prov, city, cap, nation,
                        fiscal_code, iva, sdicode, phone, cell, fax, email, bank, iban, note):

        self.pdf.add_page(orientation='P')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(190, 10, 'ANAGRAFICA CLIENTE', align='C', ln=2)
        filename = f'Anagrafica cliente {first_name} {last_name}'
        self.pdf.set_font('', '', 10)
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.cell(30, 6, "Codice cliente:", 1, align="L")
        self.pdf.cell(160, 6, str(code), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Ragione sociale:", 1, align="L")
        self.pdf.cell(160, 6, str(company), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Nome cliente:", 1, align="L")
        self.pdf.cell(65, 6, str(first_name), 1, align="L")
        self.pdf.cell(30, 6, "Cognome cliente:", 1, align="L")
        self.pdf.cell(65, 6, str(last_name), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Indirizzo cliente:", 1, align="L")
        self.pdf.cell(130, 6, str(address), 1, align="L")
        self.pdf.cell(15, 6, "N.:", 1, align="L")
        self.pdf.cell(15, 6, str(address_num), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Provincia:", 1, align="L")
        self.pdf.cell(30, 6, str(prov), 1, align="L")
        self.pdf.cell(30, 6, "Città:", 1, align="L")
        self.pdf.cell(40, 6, str(city), 1, align="L")
        self.pdf.cell(30, 6, "CAP:", 1, align="L")
        self.pdf.cell(30, 6, str(cap), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Nazione:", 1, align="L")
        self.pdf.cell(160, 6, str(nation), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Codice fiscale:", 1, align="L")
        self.pdf.cell(40, 6, str(fiscal_code), 1, align="L")
        self.pdf.cell(15, 6, "P. IVA:", 1, align="L")
        self.pdf.cell(30, 6, str(iva), 1, align="L")
        self.pdf.cell(27, 6, "Cod.Dest./PEC:", 1, align="L")
        self.pdf.cell(48, 6, str(sdicode), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Telefono:", 1, align="L")
        self.pdf.cell(65, 6, str(phone), 1, align="L")
        self.pdf.cell(30, 6, "Cellulare:", 1, align="L")
        self.pdf.cell(65, 6, str(cell), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Fax:", 1, align="L")
        self.pdf.cell(65, 6, str(fax), 1, align="L")
        self.pdf.cell(30, 6, "Email:", 1, align="L")
        self.pdf.cell(65, 6, str(email), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Banca:", 1, align="L")
        self.pdf.cell(160, 6, str(bank), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "IBAN", 1, align="L")
        self.pdf.cell(160, 6, iban, 1, align="L")
        self.pdf.ln(12)
        self.pdf.cell(30, 6, "Note:", 1, align="L")
        self.pdf.ln()
        self.pdf.multi_cell(190, 6, note, 1, align="J")
        self.pdf.ln()
        self.pdf.set_xy(75, -50)
        self.pdf.cell(60, 6, "Autorizzo il trattamento dei miei dati:")
        self.pdf.cell(65, 12, "                  ", 1)

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Ordine',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def customers_list(self, customers):
        self.pdf.add_page(orientation='L')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(277, 10, 'ELENCO CLIENTI', align='C', ln=2)
        filename = "Elenco clienti"
        self.pdf.set_font('', '', 10)
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.cell(17, 6, "Codice", 1, align="L")
        self.pdf.cell(49, 6, "Ragione sociale", 1, align="L")
        self.pdf.cell(37, 6, "Nome", 1, align="L")
        self.pdf.cell(37, 6, "Cognome", 1, align="L")
        self.pdf.cell(47, 6, "Indirizzo", 1, align="L")
        self.pdf.cell(13, 6, "Civ.", 1, align="L")
        self.pdf.cell(10, 6, "Prov.", 1, align="L")
        self.pdf.cell(27, 6, "Città", 1, align="L")
        self.pdf.cell(12, 6, "CAP", 1, align="L")
        self.pdf.cell(27, 6, "Cellulare", 1, align="L")
        self.pdf.ln()
        for customer in customers:
            self.pdf.cell(17, 6, str(customer[0]), 1, align="L")
            self.pdf.cell(49, 6, str(customer[1][:22]), 1, align="L")
            self.pdf.cell(37, 6, str(customer[2][:18]), 1, align="L")
            self.pdf.cell(37, 6, str(customer[3][:18]), 1, align="L")
            self.pdf.cell(47, 6, str(customer[4][:21]), 1, align="L")
            self.pdf.cell(13, 6, str(customer[5]), 1, align="L")
            self.pdf.cell(10, 6, str(customer[6]), 1, align="L")
            self.pdf.cell(27, 6, str(customer[7][:13]), 1, align="L")
            self.pdf.cell(12, 6, str(customer[8]), 1, align="L")
            self.pdf.cell(27, 6, str(customer[14]), 1, align="L")
            self.pdf.ln()

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Ordine',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def single_supplier(self, code, company, address, address_num, prov, city, cap, nation, fiscal_code, iva, sdicode,
                        phone, email, bank, iban, note):

        self.pdf.add_page(orientation='P')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(190, 10, 'ANAGRAFICA FORNITORE', align='C', ln=2)
        filename = f"Anagrafica fornitore {company}"
        self.pdf.set_font('', '', 10)
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.cell(30, 6, "Codice fornitore:", 1, align="L")
        self.pdf.cell(160, 6, str(code), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Ragione sociale:", 1, align="L")
        self.pdf.cell(160, 6, str(company), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Indirizzo:", 1, align="L")
        self.pdf.cell(130, 6, str(address), 1, align="L")
        self.pdf.cell(15, 6, "N.:", 1, align="L")
        self.pdf.cell(15, 6, str(address_num), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Provincia:", 1, align="L")
        self.pdf.cell(30, 6, str(prov), 1, align="L")
        self.pdf.cell(30, 6, "Città:", 1, align="L")
        self.pdf.cell(40, 6, str(city), 1, align="L")
        self.pdf.cell(30, 6, "CAP:", 1, align="L")
        self.pdf.cell(30, 6, str(cap), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Nazione:", 1, align="L")
        self.pdf.cell(160, 6, str(nation), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Codice fiscale:", 1, align="L")
        self.pdf.cell(40, 6, str(fiscal_code), 1, align="L")
        self.pdf.cell(15, 6, "P. IVA:", 1, align="L")
        self.pdf.cell(30, 6, str(iva), 1, align="L")
        self.pdf.cell(27, 6, "Cod.Dest./PEC:", 1, align="L")
        self.pdf.cell(48, 6, str(sdicode), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Telefono:", 1, align="L")
        self.pdf.cell(65, 6, str(phone), 1, align="L")
        self.pdf.cell(30, 6, "Email:", 1, align="L")
        self.pdf.cell(65, 6, str(email), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Banca:", 1, align="L")
        self.pdf.cell(160, 6, str(bank), 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "IBAN", 1, align="L")
        self.pdf.cell(160, 6, iban, 1, align="L")
        self.pdf.ln(12)
        self.pdf.cell(30, 6, "Note:", 1, align="L")
        self.pdf.ln()
        self.pdf.multi_cell(190, 6, note, 1, align="J")
        self.pdf.ln()

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Ordine',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def suppliers_list(self, suppliers):
        self.pdf.add_page(orientation='L')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(277, 10, 'ELENCO FORNITORI', align='C', ln=2)
        filename = "Elenco fornitori"
        self.pdf.set_font('', '', 10)
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.cell(17, 6, "Codice", 1, align="L")
        self.pdf.cell(49, 6, "Ragione sociale", 1, align="L")
        self.pdf.cell(47, 6, "Indirizzo", 1, align="L")
        self.pdf.cell(13, 6, "Civ.", 1, align="L")
        self.pdf.cell(10, 6, "Prov.", 1, align="L")
        self.pdf.cell(27, 6, "Città", 1, align="L")
        self.pdf.cell(12, 6, "CAP", 1, align="L")
        self.pdf.cell(37, 6, "P.IVA", 1, align="L")
        self.pdf.cell(37, 6, "Cod. Univoco/PEC", 1, align="L")
        self.pdf.cell(27, 6, "Telefono", 1, align="L")
        self.pdf.ln()
        for supplier in suppliers:
            self.pdf.cell(17, 6, str(supplier[0]), 1, align="L")
            self.pdf.cell(49, 6, str(supplier[1][:22]), 1, align="L")
            self.pdf.cell(47, 6, str(supplier[2][:21]), 1, align="L")
            self.pdf.cell(13, 6, str(supplier[3]), 1, align="L")
            self.pdf.cell(10, 6, str(supplier[4]), 1, align="L")
            self.pdf.cell(27, 6, str(supplier[5][:13]), 1, align="L")
            self.pdf.cell(12, 6, str(supplier[6]), 1, align="L")
            self.pdf.cell(37, 6, str(supplier[8][:18]), 1, align="L")
            self.pdf.cell(37, 6, str(supplier[10][:18]), 1, align="L")
            self.pdf.cell(27, 6, str(supplier[11]), 1, align="L")
            self.pdf.ln()

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Ordine',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def single_order(self, order_cod, customer_code, company, first_name, last_name, city, cell, product, date_in, work,
                     malfunction, notes):
        self.pdf.add_page(orientation='P')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(190, 10, 'DOCUMENTO RITIRO PRODOTTO', align='C', ln=2)
        filename = f"Documento ritiro prodotto n. {order_cod} {last_name} {first_name}"
        self.pdf.set_font('', '', 10)
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.cell(30, 6, "Numero ordine:", 1, align="L")
        self.pdf.cell(65, 6, order_cod, 1, align="L")
        self.pdf.cell(30, 6, "Numero cliente:", 1, align="L")
        self.pdf.cell(65, 6, customer_code, 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Ragione sociale:", 1, align="L")
        self.pdf.cell(160, 6, company, 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Nome cliente:", 1, align="L")
        self.pdf.cell(65, 6, first_name, 1, align="L")
        self.pdf.cell(30, 6, "Cognome cliente:", 1, align="L")
        self.pdf.cell(65, 6, last_name, 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Città:", 1, align="L")
        self.pdf.cell(65, 6, city, 1, align="L")
        self.pdf.cell(30, 6, "Cellulare:", 1, align="L")
        self.pdf.cell(65, 6, cell, 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Prodotto:", 1, align="L")
        self.pdf.cell(100, 6, product, 1, align="L")
        self.pdf.cell(30, 6, "Data ingresso:", 1, align="L")
        self.pdf.cell(30, 6, date_in, 1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 6, "Intervento prev.:", 1, align="L")
        self.pdf.cell(160, 6, work, 1, align="L")

        self.pdf.ln(12)
        self.pdf.cell(30, 6, "Difetto riscontrato:", 1, align="L")
        self.pdf.ln()
        self.pdf.multi_cell(190, 6, malfunction, 1)
        self.pdf.ln(6)
        self.pdf.cell(30, 6, "Note:", 1, align="L")
        self.pdf.ln()
        self.pdf.multi_cell(190, 6, notes, 1)
        self.pdf.set_xy(100, -50)
        self.pdf.cell(35, 6, "Firma per consegna:")
        self.pdf.cell(65, 12, "                  ", 1)

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Ordine',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def orders_list(self, orders):
        self.pdf.add_page(orientation='L')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(277, 10, 'ELENCO LAVORAZIONI', align='C', ln=2)
        filename = "Elenco lavorazioni"
        self.pdf.set_font('', '', 10)
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.cell(15, 6, "Codice", 1, align="L")
        self.pdf.cell(10, 6, "Stato", 1, align="L")
        self.pdf.cell(40, 6, "Prodotto", 1, align="L")
        self.pdf.cell(40, 6, "Ragione sociale", 1, align="L")
        self.pdf.cell(40, 6, "Nome cliente", 1, align="L")
        self.pdf.cell(40, 6, "Cognome cliente", 1, align="L")
        self.pdf.cell(20, 6, "Data arrivo", 1, align="L")
        self.pdf.cell(20, 6, "Data ricons.", 1, align="L")
        self.pdf.cell(52, 6, "Difetto riscontrato", 1, align="L")
        self.pdf.ln()
        for order in orders:
            if order[1] != 3:
                self.pdf.cell(15, 6, str(order[0]), 1, align="L")
                self.pdf.cell(10, 6, str(order[1]), 1, align="L")
                self.pdf.cell(40, 6, order[2][:22], 1, align="L")
                self.pdf.cell(40, 6, order[3][:22], 1, align="L")
                self.pdf.cell(40, 6, order[4][:22], 1, align="L")
                self.pdf.cell(40, 6, order[5][:22], 1, align="L")
                self.pdf.cell(20, 6, str(order[6]), 1, align="L")
                self.pdf.cell(20, 6, str(order[7]), 1, align="L")
                self.pdf.cell(52, 6, order[8][:25], 1, align="L")
                self.pdf.ln()

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Ordine',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()
            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def single_document(self, cod, doc_type, date, ref, supplier, destination, products, shipping_exp, package_exp,
                        various_exp, withdrawal_exp, stamp_exp, iva_exp, transporter, ext_look, pack_numb, weight,
                        motivation, date_out, time_out, payment, account, notes, net_value, total_taxed_exp,
                        total_taxable, doc_total, delta_iva):
        self.pdf.add_page(orientation='P')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(190, 10, doc_type, align='C', ln=2)
        self.pdf.ln()
        filename = f"Documento {cod} del {self.date.strftime('%d/%m/%Y')}"
        ##########
        self.pdf.set_font('', '', 10)
        self.pdf.cell(30, 6, "Numero doc.:", 1)
        self.pdf.cell(50, 6, str(cod), 1)
        self.pdf.cell(30, 6, "Riferimento:", 1)
        self.pdf.cell(50, 6, str(ref), 1)
        self.pdf.cell(10, 6, "Data:", 1)
        self.pdf.cell(20, 6, str(date), 1)
        self.pdf.ln()
        self.pdf.cell(30, 6, "Fornitore:", 1)
        self.pdf.cell(160, 6, supplier, 1)
        self.pdf.ln()
        self.pdf.cell(30, 6, "Destinazione:", 1)
        self.pdf.cell(160, 6, destination, 1)
        self.pdf.ln(12)
        self.pdf.set_font('', 'B', 10)
        self.pdf.cell(190, 6, "LISTA PRODOTTI", align="C")
        self.pdf.set_font('', '', 10)
        self.pdf.ln()
        self.pdf.cell(15, 6, "Codice", 1)
        self.pdf.cell(15, 6, "Categoria", 1)
        self.pdf.cell(70, 6, "Articolo", 1)
        self.pdf.cell(10, 6, "Un.", 1)
        self.pdf.cell(10, 6, "Q.tà", 1)
        self.pdf.cell(20, 6, "Prezzo U.", 1)
        self.pdf.cell(20, 6, "Importo", 1)
        self.pdf.cell(10, 6, "IVA", 1)
        self.pdf.cell(20, 6, "Totale", 1)
        self.pdf.ln()
        # Popola la tabella con i dati contenuti nel singolo prodotto
        for product in products:
            self.pdf.cell(15, 6, str(product[0]), 1)
            self.pdf.cell(15, 6, str(product[1]), 1)
            self.pdf.cell(70, 6, str(product[2][:17]), 1)
            self.pdf.cell(10, 6, str(product[3]), 1)
            self.pdf.cell(10, 6, str(product[4]), 1)
            self.pdf.cell(20, 6, str(product[5]), 1)
            self.pdf.cell(20, 6, str(product[8]), 1)
            self.pdf.cell(10, 6, str(product[9]), 1)
            self.pdf.cell(20, 6, str(product[10]), 1)
            self.pdf.ln()
        self.pdf.ln()
        self.pdf.cell(30, 6, "Spese spedizione", 1)
        self.pdf.cell(30, 6, "Spese imball.", 1)
        self.pdf.cell(30, 6, "Spese varie", 1)
        self.pdf.cell(30, 6, "Spese incasso", 1)
        self.pdf.cell(30, 6, "Spese di bollo", 1)
        self.pdf.cell(40, 6, "Spese IVA", 1)
        self.pdf.ln()
        self.pdf.cell(30, 6, str(shipping_exp), 1)
        self.pdf.cell(30, 6, str(package_exp), 1)
        self.pdf.cell(30, 6, str(various_exp), 1)
        self.pdf.cell(30, 6, str(withdrawal_exp), 1)
        self.pdf.cell(30, 6, str(stamp_exp), 1)
        self.pdf.cell(40, 6, str(iva_exp), 1)
        self.pdf.ln()
        self.pdf.cell(30, 6, "Trasporto:", 1)
        self.pdf.cell(30, 6, str(transporter), 1)
        self.pdf.cell(30, 6, "Totale spese:", 1)
        self.pdf.cell(30, 6, str(total_taxed_exp), 1)
        self.pdf.cell(30, 6, "Totale doc.:", 1)
        self.pdf.cell(40, 6, str(doc_total), 1)
        ##########

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Ordine',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def invoice(self, doc_type=None, doc_num=None, doc_date=None, payment=None, fiscal_code=None, iva_code=None,
                receiver=None, destination=None, products=None, withdrawal_exp=None, shipping_exp=None,
                total_exp=None, total_taxable=None, exp_iva=None, exp_tax=None, total_tax=None, doc_total=None,
                ext_look=None, motivation=None, transporter=None, weight=None, date_out=None, time_out=None,
                boxes=None, ref=None, notes=None):
        self.pdf.add_page(orientation='P')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(190, 10, doc_type, align='C', ln=2)
        self.pdf.ln()
        filename = f"Documento {str(doc_num)} del {datetime.date.today()}"
        ##########
        # Intestazione
        self.pdf.set_font('', '', 10)
        self.pdf.cell(190, 12, f"Destinatario: {receiver}", 1)
        self.pdf.ln()
        self.pdf.cell(190, 12, f"Destinazione: {destination}", 1)
        self.pdf.ln()
        self.pdf.cell(190, 6, f"Riferimento: {ref}", 1)
        self.pdf.ln()
        self.pdf.cell(70, 6, f"Tipo documento: {doc_type}", 1)
        self.pdf.cell(70, 6, f"Numero documento: {doc_num}", 1)
        self.pdf.cell(50, 6, f"Data documento: {doc_date}", 1)
        self.pdf.ln()
        self.pdf.cell(70, 6, f"Cond. di pagamento: {payment}", 1)
        self.pdf.cell(70, 6, f"Codice fiscale: {fiscal_code}", 1)
        self.pdf.cell(50, 6, f"Partita iva: {iva_code}", 1)
        self.pdf.ln(12)

        # Lista prodotti
        self.pdf.cell(88, 6, "Lista prodotti:")
        self.pdf.ln()
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.cell(18, 6, "Codice", 1)
        self.pdf.cell(77, 6, "Descrizione", 1)
        self.pdf.cell(14, 6, "U.M.", 1)
        self.pdf.cell(8, 6, "Q.tà", 1)
        self.pdf.cell(20, 6, "Pr. unit.", 1)
        self.pdf.cell(25, 6, "Importo", 1)
        self.pdf.cell(14, 6, "Sconto", 1)
        self.pdf.cell(14, 6, "IVA", 1)
        self.pdf.set_fill_color(255, 255, 255)

        self.pdf.ln()
        # Ciclo singolo prodotto
        for product in products:
            self.pdf.cell(18, 6, str(product[0]), 1, align="C")
            self.pdf.cell(77, 6, str(product[2]), 1)
            self.pdf.cell(14, 6, str(product[3]), 1)
            self.pdf.cell(8, 6, str(product[4]), 1)
            self.pdf.cell(20, 6, f"{chr(128)}{str(product[5])}", 1, align="R")
            self.pdf.cell(25, 6, f"{str(product[8])}", 1, align="R")
            self.pdf.cell(14, 6, f"{chr(128)}{str(product[6])}", 1)
            self.pdf.cell(14, 6, str(product[9]), 1, align="R")
            self.pdf.ln()
        # Sezione spese
        self.pdf.ln()
        self.pdf.cell(47.5, 6, f"Spese di trasporto: {chr(128)}{'%.2f'%float(shipping_exp)}", 1, align="R")
        self.pdf.cell(47.5, 6, f"Spese d'incasso: {chr(128)}{'%.2f'%float(withdrawal_exp)}", 1, align="R")
        self.pdf.cell(47.5, 6, f"Totale spese: {chr(128)}{'%.2f'%float(total_exp)}", 1, align="R")
        self.pdf.cell(47.5, 6, f"Imponibile: {chr(128)}{'%.2f'%float(total_taxable)}", 1, align="R")
        self.pdf.ln()
        exp_iva = exp_iva.split(" - ")
        exp_iva = exp_iva[2]
        self.pdf.cell(47.5, 6, f"IVA: {exp_iva}%", 1, align="R")
        self.pdf.cell(47.5, 6, f"Imposta: {chr(128)}{'%.2f'%float(exp_tax)}", 1, align="R")
        self.pdf.cell(47.5, 6, f"Totale imposta: {chr(128)}{'%.2f'%float(total_tax)}", 1, align="R")
        self.pdf.cell(47.5, 6, f"Totale: {chr(128)}{'%.2f'%float(doc_total)}", 1, align="R")
        self.pdf.ln(12)
        self.pdf.cell(190, 6, f"Causale: {motivation}", 1)
        self.pdf.ln()
        self.pdf.multi_cell(190, 6, f"Note {notes}", 1)
        self.pdf.cell(63.3, 6, f"Colli: {boxes}", 1)
        self.pdf.cell(63.3, 6, f"Aspetto est. beni: {ext_look}", 1)
        self.pdf.cell(63.4, 6, f"Trasporto a cura: {transporter}", 1)
        self.pdf.ln()
        self.pdf.cell(63.3, 6, f"Peso lordo: {weight}", 1)
        self.pdf.cell(63.3, 6, f"Data trasporto: {date_out}", 1)
        self.pdf.cell(63.4, 6, f"Ora trasporto: {time_out}", 1)
        self.pdf.ln(12)
        self.pdf.cell(95, 18, "Firma conducente:", 1)
        self.pdf.cell(95, 18, "Firma destinatario:", 1)
        self.pdf.ln()
        ##########

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Documento',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def order_invoice(self, order_cod=None, customer_code=None, company=None, customer_name=None, customer_lname=None,
                      customer_city=None, customer_phone=None, product=None, status=None, date_in=None, date_out=None,
                      malfunction=None, works=None, notes=None):
        self.pdf.add_page(orientation='P')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(190, 10, f"Scheda ordine n° {order_cod}", align='C', ln=2)
        self.pdf.ln()
        filename = f"Scheda ordine {str(order_cod)} - {customer_lname}"
        self.pdf.set_font('', '', 10)
        self.pdf.cell(95, 6, "Dati cliente:")
        self.pdf.ln()
        self.pdf.cell(95, 6, f"Codice ordine: {order_cod}", 1)
        self.pdf.ln()
        self.pdf.cell(95, 6, f"Codice cliente: {customer_code}", 1)
        self.pdf.ln(12)
        self.pdf.cell(190, 6, f"Ragione sociale: {company}", 1)
        self.pdf.ln()
        self.pdf.cell(95, 6, f"Nome: {customer_name}", 1)
        self.pdf.cell(95, 6, f"Cognome: {customer_lname}", 1)
        self.pdf.ln()
        self.pdf.cell(95, 6, f"Città: {customer_city}", 1)
        self.pdf.cell(95, 6, f"Cellulare: {customer_phone}", 1)
        self.pdf.ln(12)
        self.pdf.cell(95, 6, "Dati prodotto:")
        self.pdf.ln()
        self.pdf.cell(190, 6, f"Prodotto e S/N: {product}", 1)
        self.pdf.ln()
        self.pdf.cell(95, 6, f"Data di arrivo: {date_in}", 1)
        self.pdf.cell(95, 6, f"Data di uscita: {date_out}", 1)
        self.pdf.ln()
        self.pdf.multi_cell(190, 6, f"Difetto riscontrato: \n{malfunction}", 1)
        self.pdf.ln()
        self.pdf.cell(30, 6, "Codice", 1)
        self.pdf.cell(100, 6, "Lavorazione", 1)
        self.pdf.cell(30, 6, "Prezzo", 1)
        self.pdf.cell(30, 6, "Data", 1)
        self.pdf.ln()
        price = 0.0
        for work in works:
            self.pdf.cell(30, 6, str(work[0]), 1)
            self.pdf.cell(100, 6, str(work[1]), 1)
            self.pdf.cell(30, 6, f"{chr(128)}{str(work[2])}", 1)
            self.pdf.cell(30, 6, str(work[3]), 1)
            self.pdf.ln()
            price = price + float(work[2])
        self.pdf.cell(130, 6, "", 0)
        price = "%.2f" % price
        self.pdf.set_font('', 'B', 10)
        self.pdf.cell(60, 6, f"Totale documento: {chr(128)}{price}", 1, align="R")
        self.pdf.set_font('', '', 10)
        self.pdf.ln(12)
        self.pdf.multi_cell(190, 6, f"Note:\n{notes}", 1)
        self.pdf.ln(24)

        self.pdf.cell(130, 20, "Firma per ritiro:", 0, align="R")
        self.pdf.cell(60, 20, " ", 1)

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Documento',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass

    def work_report(self, code, wk_code, date, worker, description, trip_time, trip_km, trip_cost, accommodation,
                    products, notes):
        self.pdf.add_page(orientation='P')
        self.pdf.set_font('', 'B', 14)
        self.pdf.cell(190, 10, f"Rapportino n° {code} - Dipendente: {worker}", align='C', ln=2)
        self.pdf.ln()
        filename = f"Rapportino {str(code)}"
        self.pdf.set_font('', '', 10)
        self.pdf.cell(95, 6, "Dati generali:")
        self.pdf.ln()
        self.pdf.cell(63.3, 6, f"Codice report: {code}", 1)
        self.pdf.cell(63.3, 6, f"Codice lavorazione: {wk_code}", 1)
        self.pdf.cell(63.4, 6, f"Data: {date}", 1)
        self.pdf.ln()
        self.pdf.cell(190, 6, f"Dipendente: {worker}", 1)
        self.pdf.ln()
        self.pdf.cell(190, 6, f"Descrizione: {description}", 1)
        self.pdf.ln(12)
        self.pdf.cell(47.5, 6, f"Ore viaggio: {trip_time}", 1)
        self.pdf.cell(47.5, 6, f"Km viaggio: {trip_km}", 1)
        self.pdf.cell(47.5, 6, f"Costo viaggio: {chr(128)}{'%.2f' % float(trip_cost)}", 1)
        self.pdf.cell(47.5, 6, f"Vitto e alloggio: {chr(128)}{'%.2f' % float(accommodation)}", 1)
        self.pdf.ln(12)
        self.pdf.cell(95, 6, "Lavorazioni e prodotti:")
        self.pdf.ln()
        self.pdf.cell(40, 6, "Codice", 1)
        self.pdf.cell(110, 6, "Lavorazione/Prodotto", 1)
        self.pdf.cell(40, 6, "Prezzo", 1)
        self.pdf.ln()
        total_price = 0
        for product in products:
            self.pdf.cell(40, 6, str(product[0]), 1)
            self.pdf.cell(110, 6, str(product[1]), 1)
            self.pdf.cell(40, 6, f"{chr(128)}{product[2]}", 1, align="R")
            total_price = total_price + float(product[2])
            self.pdf.ln()
        self.pdf.cell(150, 6, "")
        self.pdf.set_font('', 'B', 10)
        total_price = total_price + float(trip_cost) + float(accommodation)
        total_price = "%.2f" % total_price
        self.pdf.cell(40, 6, f"Tot.: {chr(128)}{total_price}", 1, align="R")
        self.pdf.ln(12)
        self.pdf.set_font('', '', 10)
        self.pdf.cell(95, 6, "Note:")
        self.pdf.ln()
        self.pdf.multi_cell(190, 6, notes, 1)
        # # # #
        self.pdf.ln(30)
        self.pdf.cell(130, 20, "Firma del lavoratore:", 0, align="R")
        self.pdf.cell(60, 20, " ", 1)

        try:
            files = [("PDF", "*.pdf")]
            outfile = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files, title='Documento',
                                                      initialfile=filename)
            self.pdf.output(outfile, 'F')
            toast = ToastNotification(
                title="Documento salvato",
                message="Il documento è stato salvato con successo!",
                duration=3000,
                icon="☺",
                bootstyle="success"
            )
            toast.show_toast()

            os.startfile(outfile)

        except PermissionError:
            tk.messagebox.showerror(title="Impossibile salvare", message="Il file potrebbe essere aperto in un altro"
                                                                         " programma o protetto da scrittura.")

        except FileNotFoundError:
            pass
