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

import _tkinter
import pathlib
import tkinter.ttk
import tkinter.messagebox
import tkinter.ttk as ttk
import datetime
from configparser import ConfigParser
from tkinter import END, NORMAL

import pygubu
from ttkbootstrap import READONLY

from customer_view import CustomerView
from db_functions import DataWrite, DataRetrieve
from pdf_functions import Prints
from product_insert import ProductInsert
from supplier_view import SupplierView
from warehouse_management_window import WarehouseManagementWindow

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "new_document.ui"


class NewDocument:
    def __init__(self, preventive=False, edit=False, doc_num="", master=None):
        self.edit = edit
        self.doc_num = doc_num
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("new_document", master)
        builder.connect_callbacks(self)
        self.mainwindow.focus_set()

        self.mainwindow.state('zoomed')

        self.date = datetime.datetime.now()
        self.discount = 0
        self.doc_in = True

        self.document_type_combo = builder.get_object("document_type_combo")
        # Inizializza le tipologie documento e imposta la combobox sul valore "BC Bolla di Consegna"
        self.document_type_combo['values'] = ("PF Preventivo Fornitore", "OF Ordine Fornitore", "BF Bolla Fornitore",
                                              "FF Fattura Fornitore", "RF Reso Fornitore", "PR Preventivo",
                                              "OC Ordine Cliente", "BC Bolla di Consegna", "BD Bolla Deposito",
                                              "IN Inventario")
        self.document_type_combo.configure(state="readonly")
        if preventive:
            self.document_type_combo.current(5)
        else:
            self.document_type_combo.current(7)

        # Inizializza la variabile doc_type
        self.doc_type = self.document_type_combo.get()[:2]
        self.document_number_entry = builder.get_object("document_number_entry")
        self.document_date_entry = builder.get_object("document_date_entry")
        self.document_reference_entry = builder.get_object("document_reference_entry")
        self.document_supplier_entry = builder.get_object("document_supplier_entry")
        self.document_destination_text = builder.get_object("document_destination_text")

        self.articles_tv = builder.get_object("articles_tv")

        # Inizializza le entry dell'interfaccia e aggiunge il bind per calcolare i totali nelle etichette
        self.shipping_entry = builder.get_object("shipping_entry")
        self.shipping_entry.bind("<FocusOut>", self.on_update_press)
        self.package_entry = builder.get_object("package_entry")
        self.package_entry.bind("<FocusOut>", self.on_update_press)
        self.various_entry = builder.get_object("various_entry")
        self.various_entry.bind("<FocusOut>", self.on_update_press)
        self.withdrawal_entry = builder.get_object("withdrawal_entry")
        self.withdrawal_entry.bind("<FocusOut>", self.on_update_press)
        self.stamp_entry = builder.get_object("stamp_entry")
        self.stamp_entry.bind("<FocusOut>", self.on_update_press)
        self.iva_combo = builder.get_object("iva_combo")
        self.iva_combo.bind("<<ComboboxSelected>>", self.on_update_press)
        self.total_entry = builder.get_object("total_entry")
        self.shipping_box = builder.get_object("shipping_box")
        self.ext_look_entry = builder.get_object("ext_look_entry")
        self.boxes_entry = builder.get_object("boxes_entry")
        self.weight_entry = builder.get_object("weight_entry")
        self.motivation_entry = builder.get_object("motivation_entry")
        self.date_entry = builder.get_object("date_entry")
        self.time_entry = builder.get_object("time_entry")
        self.payment_entry = builder.get_object("payment_entry")
        self.account_entry = builder.get_object("account_entry")
        self.notes_text = builder.get_object("notes_text")

        self.document_supplier_lbl = builder.get_object("document_supplier_lbl")
        self.net_lbl = builder.get_object("net_lbl")
        self.taxable_lbl = builder.get_object("taxable_lbl")
        self.iva_lbl = builder.get_object("iva_lbl")
        self.total_lbl = builder.get_object("total_lbl")

        self.cf_entry = builder.get_object("cf_entry")
        self.piva_entry = builder.get_object("piva_entry")

        self.save_btn = builder.get_object("save_btn")

        if edit:
            self.save_btn.configure(text="Aggiorna documento", command=self.doc_update)

        taxes = []
        with open("tax.dat", "r") as taxfile:
            for line in taxfile:
                line = line.strip()
                taxes.append(line)

        taxlines = []
        for tax in taxes:
            tax = tax.split(",")
            tax = " - ".join(tax)
            taxlines.append(tax)

        self.iva_combo.configure(values=taxlines, state="readonly")
        self.iva_combo.current(0)

        # Verifica la modifica della entry fornitore
        self.suppliervar = None
        builder.import_variables(self, ['suppliervar'])

        self.suppliervar.trace("w", lambda name, index, mode, sv=self.suppliervar: self.update_suppliers())

        # Binding variazione combobox document_type
        self.document_type_combo.bind("<<ComboboxSelected>>", self.on_load)
        self.document_supplier_entry.bind("<<ComboboxSelected>>", self.on_customer_selected)

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def doc_update(self):
        pass

    def on_customer_selected(self, event):
        customer = self.document_supplier_entry.get().split(" ")[0]
        config_object = ConfigParser()
        config_object.read("company.ini")
        companyinfo = config_object["COMPANYINFO"]
        docs = ("BC", "BD", "IN", "OC", "PR")
        if self.doc_type in docs:
            customer_data = DataRetrieve().single_customer_code(customer)
            self.discount = customer_data[19]
            self.discount = self.discount.split(" - ")[1]
            fiscal_code = customer_data[10]
            piva_code = customer_data[11]
            destination = f"{customer_data[4]}, {customer_data[5]} ({customer_data[6]}) - {customer_data[8]} - " \
                          f"{customer_data[7]}"

        else:
            supplier_data = DataRetrieve().single_supplier_code(customer)
            fiscal_code = supplier_data[8]
            piva_code = supplier_data[9]
            destination = f'{companyinfo["address"]} - {companyinfo["cap"]} {companyinfo["city"]} ' \
                          f'({companyinfo["prov"]})'

        self.cf_entry.delete(0, END)
        self.cf_entry.insert(0, fiscal_code)
        self.piva_entry.delete(0, END)
        self.piva_entry.insert(0, piva_code)
        self.document_destination_text.insert(1.0, destination)

    def update_suppliers(self):
        if not self.edit:
            docs = ("BC", "BD", "IN", "OC", "PR")
            if self.doc_type not in docs:
                self.document_supplier_entry.configure(style="light.TButton")
                query = self.document_supplier_entry.get()
                query = query.upper()
                try:
                    if int(query[:6]) >= 800000 < 899999:
                        query = query[10:]
                except ValueError:
                    pass

                customers = DataRetrieve().suppliers_by_query(query)
                customer_list = []
                for customer in customers:
                    customer_list.append(f"{customer[0]} - {customer[1]}")

                if len(query) >= 2 and customer_list == []:
                    self.document_supplier_entry.configure(style="warning.TButton")
                    ask_insert = tkinter.messagebox.askyesno(parent=self.mainwindow, title="Nessun fornitore trovato",
                                                             message="Non è stato possibile trovare fornitori, ne vuoi "
                                                                     "inserire uno nuovo?")
                    if ask_insert:
                        SupplierView(master=self.mainwindow)

                self.document_supplier_entry.configure(values=customer_list)

            if self.doc_type in docs:
                self.document_supplier_entry.configure(style="light.TButton")
                query = self.document_supplier_entry.get()
                query = query.upper()
                try:
                    if int(query[:6]) >= 900000 < 999999:
                        query = query[10:].split(", ")[0]
                except ValueError:
                    pass

                customers = DataRetrieve().customers_by_query(query)
                customer_list = []
                for customer in customers:
                    customer_list.append(f"{customer[0]} | {customer[3]}, {customer[2]}")

                if len(query) >= 2 and customer_list == []:
                    self.document_supplier_entry.configure(style="warning.TButton")
                    ask_insert = tkinter.messagebox.askyesno(parent=self.mainwindow, title="Nessun cliente trovato",
                                                             message="Non è stato possibile trovare clienti, "
                                                                     "ne vuoi inserire uno nuovo?")
                    if ask_insert:
                        CustomerView(master=self.mainwindow)

                self.document_supplier_entry.configure(values=customer_list)

    def on_load(self, event=None):
        if not self.edit:
            self.document_number_entry.configure(state="normal")
            self.document_number_entry.delete(0, END)
            self.doc_type = self.document_type_combo.get()[:2]
            self.document_supplier_entry.delete(0, END)
            docs = ("BC", "BD", "IN", "OC", "PR")
            if self.doc_type in docs:
                self.document_supplier_lbl.configure(text="Cliente")
                self.document_date_entry.delete(0, END)
                self.document_date_entry.insert(0, self.date.strftime('%d/%m/%Y'))
                self.document_number_entry.insert(0, datetime.date.today().year)
                self.document_number_entry.insert(END, self.doc_type)
                query = self.document_number_entry.get()
                self.doc_in = False
                try:
                    # Formatta la stringa con (ANNO)(TIPO DOCUMENTO)(PROGRESSIVO)
                    last_doc = DataRetrieve().last_document_get(query)
                    last_doc = int(last_doc[0].replace(query, "")) + 1
                except TypeError:
                    # Raccoglie l'errore in caso di assenza di documenti precedenti e inizializza il valore
                    last_doc = 900000
                self.document_number_entry.insert(END, last_doc)
                self.document_number_entry.configure(state="readonly")
                customer = self.document_supplier_entry.get()
                customer = customer.split(" |")[0]

            else:
                self.document_supplier_lbl.configure(text="Fornitore")
        else:
            document = DataRetrieve().single_document_code(self.doc_num)
            self.document_number_entry.insert(0, document[0])
            self.document_number_entry.configure(state=READONLY)
            self.document_type_combo.configure(state="normal")
            self.document_type_combo.delete(0, END)
            self.document_type_combo.insert(0, document[1])
            self.document_type_combo.configure(state=READONLY)
            self.document_date_entry.insert(0, document[2])
            self.document_date_entry.configure(state=READONLY)
            self.document_reference_entry.insert(0, document[3])
            self.document_reference_entry.configure(state=READONLY)
            self.document_supplier_entry.configure(state=NORMAL)
            self.document_supplier_entry.delete(0, END)
            self.document_supplier_entry.insert(0, document[4])
            self.document_supplier_entry.configure(state=READONLY)
            self.document_destination_text.delete(1.0, END)
            self.document_destination_text.insert(1.0, document[5][:-1])
            self.document_supplier_entry.configure(state="normal")
            self.articles_tv.delete(*self.articles_tv.get_children())
            products = document[6].split("], [")
            for product in products:
                product = product.replace("'", "")
                product = product.replace("[[", "")
                product = product.replace("]]", "")
                values = product.split(",")
                self.articles_tv.insert("", END, values=values)
            self.shipping_entry.delete(0, END)
            self.shipping_entry.insert(0, "%.2f" % float(document[7]))
            self.package_entry.delete(0, END)
            self.package_entry.insert(0, "%.2f" % float(document[8]))
            self.various_entry.delete(0, END)
            self.various_entry.insert(0, "%.2f" % float(document[9]))
            self.withdrawal_entry.delete(0, END)
            self.withdrawal_entry.insert(0, "%.2f" % float(document[10]))
            self.stamp_entry.delete(0, END)
            self.stamp_entry.insert(0, "%.2f" % float(document[11]))
            self.iva_combo.configure(state=NORMAL)
            self.iva_combo.delete(0, END)
            self.iva_combo.insert(0, document[12])
            self.iva_combo.configure(state=READONLY)
            self.shipping_box.configure(state=NORMAL)
            self.shipping_box.delete(0, END)
            self.shipping_box.insert(0, document[13])
            self.shipping_box.configure(state=READONLY)
            self.ext_look_entry.delete(0, END)
            self.ext_look_entry.insert(0, document[14])
            self.boxes_entry.delete(0, END)
            self.boxes_entry.insert(0, document[15])
            self.weight_entry.delete(0, END)
            self.weight_entry.insert(0, document[16])
            self.motivation_entry.delete(0, END)
            self.motivation_entry.insert(0, document[17])
            self.date_entry. delete(0, END)
            self.date_entry.insert(0, document[18])
            self.time_entry.delete(0, END)
            self.time_entry.insert(0, document[19])
            self.payment_entry.delete(0, END)
            self.payment_entry.insert(0, document[20])
            self.account_entry.delete(0, END)
            self.account_entry.insert(0, document[21])
            self.notes_text.delete(1.0, END)
            self.notes_text.insert(1.0, document[22])
            # Inserimento dati cliente/fornitore
            self.doc_type = self.document_type_combo.get()[:2]
            docs = ("BC", "BD", "IN", "OC", "PR")
            customer = self.document_supplier_entry.get().split(" ")[0]
            fiscal_code = ""
            piva_code = ""
            if self.doc_type in docs:
                self.document_supplier_lbl.configure(text="Cliente:")
                customer_data = DataRetrieve().single_customer_code(customer)
                self.discount = customer_data[19]
                try:
                    fiscal_code = customer_data[10]
                except TypeError:
                    pass
                try:
                    piva_code = customer_data[11]
                except TypeError:
                    pass
            
            else:
                self.document_supplier_lbl.configure(text="Fornitore:")
                supplier_data = DataRetrieve().single_supplier_code(customer)
                fiscal_code = supplier_data[8]
                piva_code = supplier_data[9]
            
            self.cf_entry.insert(0, fiscal_code)
            self.piva_entry.insert(0, piva_code)

            self.on_update_press()

    def on_freerow_press(self):
        ProductInsert("out", self.articles_tv, self.on_update_press, freerow=True).mainwindow.grab_set()

    def on_delete_press(self):
        try:
            item = self.articles_tv.selection()
            self.articles_tv.delete(item)
        except _tkinter.TclError:
            tkinter.messagebox.showerror(parent=self.mainwindow,
                                         title="Seleziona riga",
                                         message="Selezionare la riga da eliminare!")

    def document_calc(self):
        # Calcolo spese
        shipment = float(self.shipping_entry.get())
        package = float(self.package_entry.get())
        various = float(self.various_entry.get())
        withdrawal = float(self.withdrawal_entry.get())
        stamp = float(self.stamp_entry.get())
        try:
            iva = int(self.iva_combo.get().split(" - ")[2])
        except IndexError:
            iva = int(self.iva_combo.get())
        taxable = package + various + stamp + withdrawal
        iva = iva / 100 + 1
        taxed = taxable * iva + shipment
        tax = (taxable * iva) - taxable
        tax = "%.2f" % tax
        expenses = taxed
        exp_tax = float(tax)
        # Calcolo prodotti
        prod_taxed = 0.0
        prod_taxable = 0.0
        discount = 0
        for child in self.articles_tv.get_children():
            prod_taxed = prod_taxed + float(self.articles_tv.item(child)["values"][10])
            prod_taxable = prod_taxable + float(self.articles_tv.item(child)["values"][8])
            if not self.doc_in:
                if int(self.discount) == 1:
                    discount = float(self.articles_tv.item(child)["values"][6])/100 + 1
                    prod_taxed = prod_taxed/discount

                elif int(self.discount) == 2:
                    discount = float(self.articles_tv.item(child)["values"][7])/100 + 1
                    prod_taxed = prod_taxed/discount

        prod_tax = prod_taxed - prod_taxable
        taxable = taxable + prod_taxable
        tax = float(tax) + float(prod_tax)
        taxed = taxed + prod_taxed
        taxable = round(taxable, 2)
        tax = round(tax, 2)
        taxed = round(taxed, 2)
        prod_taxable = round(prod_taxable, 2)
        prod_taxed = round(prod_taxed, 2)

        costs = {"taxable": taxable, "tax": tax, "taxed": taxed, "prod_taxable": prod_taxable, "prod_taxed": prod_taxed,
                 "expenses": expenses, "exp_tax": exp_tax}

        return costs

    def on_new_art_press(self):
        # Apre la finestra d'inserimento prodotto
        supplier = self.document_supplier_entry.get()
        docs = ("BC", "BD", "IN", "OC", "PR")
        if self.doc_type in docs:
            ProductInsert("out", self.articles_tv, self.on_update_press).mainwindow.grab_set()
        else:
            ProductInsert("in", self.articles_tv, self.on_update_press, supplier=supplier).mainwindow.grab_set()

    def on_update_press(self, event=None):
        # Calcola il valore totale dei prodotti in elenco
        costs = self.document_calc()

        self.net_lbl.configure(text=f'€{"%.2f" %float(costs["prod_taxable"])}')
        self.taxable_lbl.configure(text=f'€{"%.2f" %float(costs["taxable"])}')
        self.iva_lbl.configure(text=f'€{"%.2f" %float(costs["tax"])}')
        self.total_lbl.configure(text=f'€{"%.2f" %float(costs["taxed"])}')
        self.total_entry.delete(0, END)
        self.total_entry.insert(0, "%.2f" % float(costs["expenses"]))

    def on_save_press(self):
        self.doc_type = self.document_type_combo.get()[:2]
        if self.document_number_entry.get() == "" or self.document_supplier_entry.get() == "":
            tkinter.messagebox.showwarning(parent=self.mainwindow, title="Campi incompleti",
                                           message="Inserisci i campi mancanti")
            self.mainwindow.focus_set()
        else:
            doc_type = self.document_type_combo.get()
            doc_number = self.document_number_entry.get()
            doc_date = self.document_date_entry.get()
            doc_ref = self.document_reference_entry.get()
            doc_supplier = self.document_supplier_entry.get()
            doc_destination = self.document_destination_text.get(1.0, END)

            products = []
            for child in self.articles_tv.get_children():
                products.append(self.articles_tv.item(child)["values"])
                docs = ("BC", "BD", "IN", "OC", "PR")
                if self.doc_type in docs:
                    try:
                        DataWrite().product_stock_update_subtract(cod=self.articles_tv.item(child)["values"][0],
                                                                  qty=self.articles_tv.item(child)["values"][4])
                    except TypeError:
                        pass
                else:
                    try:
                        DataWrite().product_stock_update_add(cod=self.articles_tv.item(child)["values"][0],
                                                             qty=self.articles_tv.item(child)["values"][4])
                    except TypeError:
                        pass

            shipping_exp = self.shipping_entry.get()
            package_exp = self.package_entry.get()
            various_exp = self.various_entry.get()
            withdrawal_exp = self.withdrawal_entry.get()
            stamp_exp = self.stamp_entry.get()
            iva_exp = self.iva_combo.get()
            total = self.total_entry.get()
            transporter = self.shipping_box.get()
            ext_look = self.ext_look_entry.get()
            pack_numb = self.boxes_entry.get()
            weight = self.weight_entry.get()
            motivation = self.motivation_entry.get()
            date_out = self.date_entry.get()
            time_out = self.time_entry.get()
            payment = self.payment_entry.get()
            account = self.account_entry.get()
            notes = self.notes_text.get(1.0, END)

            check = DataWrite().insert_document(doc_number, doc_type, doc_date, doc_ref, doc_supplier, doc_destination,
                                                products, shipping_exp, package_exp, various_exp, withdrawal_exp,
                                                stamp_exp, iva_exp, transporter, ext_look, pack_numb, weight,
                                                motivation, date_out, time_out, payment, account, notes)
            if not check:
                tkinter.messagebox.showerror(parent=self.mainwindow, title="Documento già presente",
                                             message="Impossibile registrare un documento già in database.")

            self.doc_type = self.document_type_combo.get()[:2]
            document_type = self.document_type_combo.get()
            docs = ("BC", "BD", "IN", "OC", "PR")
            if self.doc_type in docs:
                self.on_print_press()
        self.on_clear_press()

    def on_print_press(self):
        doc_type = self.document_type_combo.get()
        doc_number = self.document_number_entry.get()
        doc_date = self.document_date_entry.get()
        doc_ref = self.document_reference_entry.get()
        doc_supplier = self.document_supplier_entry.get()
        doc_destination = self.document_destination_text.get(1.0, END)
        fiscal_code = self.cf_entry.get()
        iva_code = self.piva_entry.get()

        products = ()
        for child in self.articles_tv.get_children():
            product = self.articles_tv.item(child)["values"]
            if self.discount == "0":
                product = (product[0], product[1], product[2], product[3], product[4], product[5],
                           "0", "0", product[8], product[9], product[10])
            elif self.discount == "1":
                product = (product[0], product[1], product[2], product[3], product[4], product[5],
                           product[6], product[6], product[8], product[9], product[10])
            elif self.discount == "2":
                product = (product[0], product[1], product[2], product[3], product[4], product[5],
                           product[7], product[7], product[8], product[9], product[10])
            products.append(product)

        shipping_exp = self.shipping_entry.get()
        package_exp = self.package_entry.get()
        various_exp = self.various_entry.get()
        withdrawal_exp = self.withdrawal_entry.get()
        stamp_exp = self.stamp_entry.get()
        iva_exp = self.iva_combo.get()
        total = self.total_entry.get()
        transporter = self.shipping_box.get()
        ext_look = self.ext_look_entry.get()
        pack_numb = self.boxes_entry.get()
        weight = self.weight_entry.get()
        motivation = self.motivation_entry.get()
        date_out = self.date_entry.get()
        time_out = self.time_entry.get()
        payment = self.payment_entry.get()
        account = self.account_entry.get()
        notes = self.notes_text.get(1.0, END)

        document_type = self.document_type_combo.get()

        data = self.document_calc()

        Prints().invoice(products=products, doc_type=document_type, doc_num=doc_number, receiver=doc_supplier,
                         destination=doc_destination, doc_date=doc_date, payment=payment, fiscal_code=fiscal_code,
                         iva_code=iva_code, shipping_exp=shipping_exp, withdrawal_exp=withdrawal_exp,
                         total_exp=round(float(data['expenses']), 2), total_taxable=round(float(data['taxable']), 2),
                         exp_iva=iva_exp, exp_tax=round(float(data['exp_tax']), 2), total_tax=data['tax'],
                         doc_total=data['taxed'], ext_look=ext_look, motivation=motivation, transporter=transporter,
                         weight=weight, date_out=date_out, time_out=time_out, boxes=pack_numb, ref=doc_ref, notes=notes)

    def on_clear_press(self):
        self.document_number_entry.delete(0, END)
        self.document_date_entry.delete(0, END)
        self.document_reference_entry.delete(0, END)
        self.document_supplier_entry.delete(0, END)
        self.document_destination_text.delete(1.0, END)
        self.cf_entry.delete(0, END)
        self.piva_entry.delete(0, END)
        self.shipping_entry.delete(0, END)
        self.package_entry.delete(0, END)
        self.various_entry.delete(0, END)
        self.withdrawal_entry.delete(0, END)
        self.stamp_entry.delete(0, END)
        self.iva_combo.delete(0, END)
        self.total_entry.delete(0, END)
        self.shipping_box.delete(0, END)
        self.ext_look_entry.delete(0, END)
        self.boxes_entry.delete(0, END)
        self.weight_entry.delete(0, END)
        self.motivation_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.time_entry.delete(0, END)
        self.payment_entry.delete(0, END)
        self.account_entry.delete(0, END)
        self.notes_text.delete(1.0, END)
        self.articles_tv.delete(*self.articles_tv.get_children())
        self.on_load()

    def ignore(self):
        pass


if __name__ == "__main__":
    app = NewDocument()
    app.run()
