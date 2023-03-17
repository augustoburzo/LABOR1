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

import sqlite3
import datetime
from configparser import ConfigParser


class DBInit:
    def __init__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}labor.db"
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

        # Verifica l'esistenza delle tabelle nel db e le genera se non presenti
        # Generazione tabella prodotti
        self.cur.execute('''CREATE TABLE IF NOT EXISTS reports (
                            "cod"   INTEGER NOT NULL,
                            "wk_code"   TEXT,
                            "rep_date"  TEXT,
                            "worker"    TEXT,
                            "descr"     TEXT,
                            "trip_time" TEXT,
                            "trip_km"   TEXT,
                            "trip_price"    TEXT,
                            "accom_exp" TEXT,
                            "products"  TEXT,
                            "notes"     TEXT,
                            PRIMARY KEY ("cod" AUTOINCREMENT)
                        );''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS products (
                            "cod"	TEXT NOT NULL,
                            "category"  TEXT,
                            "product"   TEXT,
                            "ean"   TEXT UNIQUE,
                            "unit"  TEXT,
                            "quantity"  INT,
                            "price" TEXT,
                            "discount1" TEXT,
                            "discount2" TEXT,
                            "selling" TEXT,
                            "iva" TEXT,
                            PRIMARY KEY("cod")
                        );''')

        # Generazione tabella documenti
        self.cur.execute('''CREATE TABLE IF NOT EXISTS documents (
                            "cod"   TEXT NOT NULL,
                            "type"  TEXT,
                            "date"  TEXT,
                            "ref"   TEXT,
                            "supplier"  TEXT,
                            "destination"   TEXT,
                            "products"  TEXT,
                            "shipping_exp"  TEXT,
                            "package_exp"   TEXT,
                            "various_exp"   TEXT,
                            "withdrawal_exp"    TEXT,
                            "stamp_exp" TEXT,
                            "iva_exp"   TEXT,
                            "transporter" TEXT,
                            "ext_look"  TEXT,
                            "pack_numb" INT,
                            "weight"    TEXT,
                            "motivation"    TEXT,
                            "date_out"  TEXT,
                            "time_out"  TEXT,
                            "payment"   TEXT,
                            "account"   TEXT,
                            "notes" TEXT,
                            PRIMARY KEY("cod")
                        );''')

        # Generazione tabella ordini
        self.cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                            "code"	INTEGER NOT NULL,
                            "customer_code"	INTEGER,
                            "status"	INTEGER,
                            "product"	TEXT,
                            "date_in"	TEXT,
                            "date_out"	TEXT,
                            "malfunction"	TEXT,
                            "diagnosis"	TEXT,
                            "notes"	TEXT,
                            "intervention"	TEXT,
                            PRIMARY KEY("code" AUTOINCREMENT)
                        );''')

        # Generazione tabella clienti
        self.cur.execute('''CREATE TABLE IF NOT EXISTS customers (
                            "code"	INTEGER NOT NULL,
                            "company"	TEXT,
                            "first_name"	TEXT,
                            "last_name"	TEXT,
                            "address"	TEXT,
                            "addr_number"	TEXT,
                            "prov"	TEXT,
                            "city"	TEXT,
                            "cap"	TEXT,
                            "nation"	TEXT,
                            "fiscal_code"	TEXT,
                            "iva"	TEXT,
                            "sdi"	TEXT,
                            "phone"	TEXT,
                            "cell"	TEXT,
                            "fax"	TEXT,
                            "email"	TEXT,
                            "bank"	TEXT,
                            "iban"	TEXT,
                            "list"	TEXT,
                            "note"  TEXT,
                            PRIMARY KEY("code" AUTOINCREMENT)
                        );''')

        # Generazione tabella fornitori
        self.cur.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                                    "code"	INTEGER NOT NULL,
                                    "company"	TEXT,
                                    "address"	TEXT,
                                    "addr_number"	TEXT,
                                    "prov"	TEXT,
                                    "city"	TEXT,
                                    "cap"	TEXT,
                                    "nation"	TEXT,
                                    "fiscal_code"	TEXT,
                                    "iva"	TEXT,
                                    "sdi"	TEXT,
                                    "phone"	TEXT,
                                    "email"	TEXT,
                                    "bank"	TEXT,
                                    "iban"	TEXT,
                                    "note"  TEXT,
                                    PRIMARY KEY("code" AUTOINCREMENT)
                                );''')

        # Generazione tabella documenti
        self.cur.execute('''CREATE TABLE IF NOT EXISTS documents (
                                    "code"  INTEGER NOT NULL,
                                    "doc_type"  TEXT,
                                    "date"  TEXT,
                                    "ref"   TEXT,
                                    "supplier" TEXT,
                                    "destination"   TEXT,
                                    "products"  TEXT,
                                    "transp_exp"    TEXT,
                                    "package_exp"   TEXT,
                                    "various_exp"   TEXT,
                                    "withdrawal_exp"    TEXT,
                                    "stamp_exp" TEXT,
                                    "iva"   TEXT,
                                    "exp_total" TEXT,
                                    "transporter" TEXT,
                                    "ext_look"  TEXT,
                                    "boxes_num" TEXT,
                                    "weight"    TEXT,
                                    "date_out"  TEXT,
                                    "time_out"  TEXT,
                                    "payment"   TEXT,
                                    "account"   TEXT,
                                    "notes" TEXT,
                                    PRIMARY KEY("code")
                                );''')

        self.cur.close()
        self.cur = self.con.cursor()

        # Inizializza il codice cliente di partenza e lo elimina
        self.cur.execute("INSERT OR IGNORE INTO customers (code) VALUES ('9000000');")
        self.cur.execute("DELETE FROM customers WHERE code = 9000000")

        # Inizializza il codice report di partenza e lo elimina
        self.cur.execute("INSERT OR IGNORE INTO reports (cod) VALUES (15000000)")
        self.cur.execute("DELETE FROM reports WHERE cod = 15000000")

        config_object = ConfigParser()
        config_object.read("company.ini")
        companyinfo = config_object["COMPANYINFO"]

        # Inizializza il codice fornitore di partenza e lo elimina
        self.cur.execute("INSERT OR IGNORE INTO suppliers (code, company, address, prov, city, cap, nation,"
                         " fiscal_code, iva, phone, email) VALUES ('8000000', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                         (companyinfo["company"], companyinfo["address"], companyinfo["prov"], companyinfo["city"],
                          companyinfo["cap"], companyinfo["nation"], companyinfo["fiscal_code"], companyinfo["iva"],
                          companyinfo["phone"], companyinfo["email"]))

        # Inizializza il codice lavorazione di partenza e lo elimina
        self.cur.execute("INSERT OR IGNORE INTO orders (code) VALUES ('1000000');")
        self.cur.execute("DELETE FROM orders WHERE code = 1000000")
        self.con.commit()
        self.cur.close()


class DataRetrieve:
    # Classe di recupero dati dal database
    def __init__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}labor.db"
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

    def single_order_code(self, code):
        # Restituisce singolo ordine per codice
        self.cur.execute("SELECT * FROM orders WHERE code = ?", (code,))
        order = self.cur.fetchone()
        self.cur.close()
        return order

    def all_orders(self):
        # Restituisce la lista completa degli ordini in ordine di stato
        self.cur.execute("SELECT * FROM orders ORDER BY status ASC")
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def all_working_orders(self):
        # Restituisce la lista completa degli ordini in ordine di stato
        self.cur.execute("SELECT * FROM orders WHERE status NOT LIKE '3' ORDER BY status ASC")
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def single_customer_orders(self, customer_code):
        self.cur.execute("SELECT * FROM orders WHERE customer_code = ?", (customer_code,))
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def waiting_orders(self):
        # Restituisce la lista degli ordini in attesa
        self.cur.execute("SELECT * FROM orders WHERE status = '0'")
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def in_progress_orders(self):
        # Restituisce la lista degli ordini in lavorazione
        self.cur.execute("SELECT * FROM orders WHERE status = '1'")
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def done_orders(self):
        # Restituisce la lista degli ordini completati
        self.cur.execute("SELECT * FROM orders WHERE status = '2'")
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def closed_orders(self):
        # Restituisce la lista degli ordini restituiti
        self.cur.execute("SELECT * FROM orders WHERE status = '3'")
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def customer(self, last_name):
        # Restituisce una lista di clienti il cui cognome contenga la query "last_name"
        last_name = f'%{last_name}%'
        self.cur.execute("SELECT * FROM customers WHERE last_name LIKE ?", (last_name,))
        customers = self.cur.fetchall()
        self.cur.close()
        return customers

    def company_customer(self, company):
        # Restituisce una lista di clienti la cui ragione sociale contenga la query "company"
        company = f'%{company}%'
        self.cur.execute("SELECT * FROM customers WHERE company LIKE ?", (company,))
        customers = self.cur.fetchall()
        self.cur.close()
        return customers

    def all_customers(self):
        # Restituisce la lista clienti
        self.cur.execute("SELECT * FROM customers")
        customers = self.cur.fetchall()
        self.cur.close()
        return customers

    def single_customer_code(self, code):
        # Resituisce singolo cliente per codice
        self.cur.execute("SELECT * FROM customers WHERE code = ?", (code,))
        customer = self.cur.fetchone()
        self.cur.close()
        return customer

    def warehouse_status(self):
        # Restituisce la giacenza di magazzino
        self.cur.execute("SELECT * FROM products")
        products = self.cur.fetchall()
        self.cur.close()
        return products

    def warehouse_low_qty(self):
        self.cur.execute("SELECT * FROM products WHERE quantity <= 3")
        products = self.cur.fetchall()
        return products

    def single_product_code(self, code):
        # Restituisce lista prodotti il cui codice contenga la query "code"
        code = f"%{code}%"
        self.cur.execute(f"SELECT * FROM products WHERE cod LIKE ?", (code,))
        products = self.cur.fetchall()
        self.cur.close()
        return products

    def multiple_orders_name(self, query):
        query = f"%{query}%"
        self.cur.execute("SELECT * FROM orders WHERE product LIKE ? ORDER BY status ASC", (query,))
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def multiple_orders_code(self, query):
        query = f"%{query}%"
        self.cur.execute("SELECT * FROM orders WHERE code LIKE ? ORDER BY status ASC", (query,))
        orders = self.cur.fetchall()
        self.cur.close()
        return orders

    def single_product_code_NOLIST(self, code):
        # Restituisce lista prodotti il cui codice contenga la query "code"

        self.cur.execute(f"SELECT * FROM products WHERE cod = ?", (code,))
        products = self.cur.fetchall()
        self.cur.close()
        return products

    def single_product_name(self, name):
        # Restituisce lista prodotti il cui codice contenga la query "name"
        name = f"%{name}%"
        self.cur.execute(f"SELECT * FROM products WHERE product LIKE ?", (name,))
        products = self.cur.fetchall()
        self.cur.close()
        return products

    def all_suppliers(self):
        # Restituisce la lista fornitori
        self.cur.execute("SELECT * FROM suppliers")
        customers = self.cur.fetchall()
        self.cur.close()
        return customers

    def single_supplier_code(self, code):
        # Restituisce singolo fornitore per codice
        self.cur.execute("SELECT * FROM suppliers WHERE code = ?", (code,))
        supplier = self.cur.fetchone()
        self.cur.close()
        return supplier

    def suppliers_by_query(self, query):
        query = f"%{query}%"
        self.cur.execute("SELECT * FROM suppliers WHERE company LIKE ?", (query,))
        suppliers = self.cur.fetchall()
        self.cur.close()
        return suppliers

    def customers_by_query(self, query):
        query = f"%{query}%"
        self.cur.execute("SELECT * FROM customers WHERE last_name LIKE ?", (query,))
        suppliers = self.cur.fetchall()
        self.cur.close()
        return suppliers

    def single_document_code(self, code):
        # Restituisce singolo documento per codice
        self.cur.execute("SELECT * FROM documents WHERE cod = ?", (code,))
        document = self.cur.fetchone()
        self.cur.close()
        return document

    def documents_by_query(self, query):
        query = f"%{query}%"
        self.cur.execute("SELECT * FROM documents WHERE cod LIKE ?", (query,))
        documents = self.cur.fetchall()
        if not documents:
            self.cur.execute("SELECT * FROM documents WHERE supplier LIKE ?", (query,))
            documents = self.cur.fetchall()

    def last_document_get(self, query):
        # Cerca l'ultimo documento inserito con all'inizio la query e lo restituisce
        query = f"{query}%"
        self.cur.execute("SELECT * FROM documents WHERE cod LIKE ? ORDER BY cod DESC;", (query,))
        document = self.cur.fetchone()
        self.cur.close()
        return document

    def documents_by_date(self, date):
        # Restituisce la lista di documenti per data contenuta nella query "date"
        self.cur.execute("SELECT * FROM documents WHERE date = ?", (date,))
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def all_documents(self):
        # Restituisce la lista documenti
        self.cur.execute("SELECT * FROM documents")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def all_reports(self):
        # Restituisce la lista rapportini
        self.cur.execute("SELECT * FROM reports")
        reports = self.cur.fetchall()
        self.cur.close()
        return reports

    def single_report_code(self, code):
        self.cur.execute("SELECT * FROM reports WHERE cod = ?", (code,))
        report = self.cur.fetchone()
        self.cur.close()
        return report

    def PF_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'PF Preventivo Fornitore'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def OF_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'OF Ordine Fornitore'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def BF_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'BF Bolla Fornitore'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def FF_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'FF Fattura Fornitore'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def RF_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'RF Reso Fornitore'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def PR_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'PR Preventivo'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def OC_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'OC Ordine Cliente'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def BC_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'BC Bolla di Consegna'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def BD_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'BD Bolla Deposito'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents

    def IN_retrieve(self):
        self.cur.execute("SELECT * FROM documents WHERE type = 'IN Inventario'")
        documents = self.cur.fetchall()
        self.cur.close()
        return documents


class DataWrite:
    # Classe di scrittura dati a database
    def __init__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}labor.db"
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()
        self.date = datetime.datetime.now()

    def new_report(self, cod, wk_code, rep_date, worker, descr, trip_time, trip_km, trip_price, accom_exp, products,
                   notes):
        self.cur.execute('''INSERT INTO reports (wk_code, rep_date, worker, descr, trip_time, trip_km, trip_price,
         accom_exp, products, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (wk_code, rep_date, worker,
                                                                                descr, trip_time, trip_km,
                                                                                trip_price, accom_exp, products,
                                                                                notes))
        self.con.commit()
        self.cur.close()
        written = True
        return written

    def new_customer(self, company, first_name, last_name, address, addr_number, prov, city, cap, nation, fiscal_code,
                     iva, sdi, phone, cell, fax, email, bank, iban, list_cat, note):

        # Inserisce nel database un singolo cliente
        self.cur.execute('''INSERT INTO customers (company, first_name, last_name, address, addr_number, prov, city, 
        cap, nation, fiscal_code, iva, sdi, phone, cell, fax, email, bank, iban, list, note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (company, first_name, last_name, address, addr_number, prov, city, cap, nation, fiscal_code,
                          iva, sdi, phone, cell, fax, email, bank, iban, list_cat, note))
        self.con.commit()
        self.cur.close()

    def new_supplier(self, company, address, addr_number, prov, city, cap, nation, fiscal_code, iva, sdi, phone, email,
                     bank, iban, note):

        # Inserisce nel database un singolo fornitore
        self.cur.execute('''INSERT INTO suppliers (company, address, addr_number, prov, city, cap, nation, fiscal_code, 
        iva, sdi, phone, email, bank, iban, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?)''',
                         (company, address, addr_number, prov, city, cap, nation, fiscal_code, iva, sdi, phone, email,
                          bank, iban, note))
        self.con.commit()
        self.cur.close()

    def supplier_update(self, code, company, address, addr_number, prov, city, cap, nation, fiscal_code, iva, sdi,
                        phone, email, bank, iban, note):

        # Aggiorna i dati di un fornitore già esistente
        self.cur.execute('''UPDATE suppliers SET
                            company = ?,
                            address = ?, 
                            addr_number = ?, 
                            prov = ?, 
                            city = ?,
                            cap = ?,
                            nation = ?,
                            fiscal_code = ?,
                            iva = ?,
                            sdi = ?,
                            phone = ?,
                            email = ?,
                            bank = ?,
                            iban = ?,
                            note = ?
                            WHERE code = ?''',
                         (company, address, addr_number, prov, city, cap, nation, fiscal_code, iva, sdi, phone, email,
                          bank, iban, note, code))
        self.con.commit()
        self.cur.close()

    def order_full_update(self, malfunction, diagnosis, notes, intervention, code):
        self.cur.execute('''UPDATE orders SET
                                    malfunction = ?,
                                    diagnosis = ?,
                                    notes = ?,
                                    intervention = ?
                                    WHERE code = ?;''',
                         (malfunction, diagnosis, notes, intervention, code))
        self.con.commit()
        self.cur.close()

    def report_update(self, code, wk_code, rep_date, worker, descr, trip_time, trip_km, trip_price, accom_exp,
                      products, notes):
        self.cur.execute('''UPDATE reports SET
                                wk_code = ?,
                                rep_date = ?,
                                worker = ?,
                                descr = ?,
                                trip_time = ?,
                                trip_km = ?,
                                trip_price = ?,
                                accom_exp = ?,
                                products = ?,
                                notes = ?
                                WHERE cod = ?;''',
                         (wk_code, rep_date, worker, descr, trip_time, trip_km, trip_price, accom_exp, products, notes,
                          code))
        self.con.commit()
        self.cur.close()
        updated = True
        return updated

    def product_stock_update_add(self, cod, qty):
        self.cur.execute("SELECT * FROM products WHERE cod = ?", (cod,))
        old_qty = self.cur.fetchone()[5]
        qty = int(old_qty) + int(qty)
        # Aumenta la giacenza di un prodotto già esistente
        self.cur.execute('''UPDATE products SET
                                    quantity = ?
                                    WHERE cod = ?''',
                         (qty, cod))
        self.con.commit()
        self.cur.close()

    def product_stock_update_subtract(self, cod, qty):
        self.cur.execute("SELECT * FROM products WHERE cod = ?", (cod,))
        old_qty = self.cur.fetchone()[5]
        qty = int(old_qty) - int(qty)
        # Diminuisce la giacenza di un prodotto già esistente
        self.cur.execute('''UPDATE products SET
                                    quantity = ?
                                    WHERE cod = ?''',
                         (qty, cod))
        self.con.commit()
        self.cur.close()

    def customer_update(self, code, company, first_name, last_name, address, addr_number, prov, city, cap, nation,
                        fiscal_code, iva, sdi, phone, cell, fax, email, bank, iban, list_cat, notes):

        # Aggiorna i dati di un cliente già esistente
        self.cur.execute('''UPDATE customers SET
                            company = ?, 
                            first_name = ?, 
                            last_name = ?, 
                            address = ?, 
                            addr_number = ?, 
                            prov = ?, 
                            city = ?,
                            cap = ?,
                            nation = ?,
                            fiscal_code = ?,
                            iva = ?,
                            sdi = ?,
                            phone = ?,
                            cell = ?,
                            fax = ?,
                            email = ?,
                            bank = ?,
                            iban = ?,
                            list = ?,
                            note = ?
                            WHERE code = ?''',
                         (company, first_name, last_name, address,
                          addr_number, prov, city, cap, nation,
                          fiscal_code, iva, sdi, phone, cell, fax,
                          email, bank, iban, list_cat, notes, code))
        self.con.commit()
        self.cur.close()

    def order_update(self, code, status):

        # Aggiorna un ordine già esistente
        if status == 3:
            date = self.date.strftime('%d/%m/%Y')
            self.cur.execute(f"UPDATE orders SET status = {status}, date_out = '{str(date)}' WHERE code = "
                             f"{code}")
        else:
            self.cur.execute(f"UPDATE orders SET status = {status} WHERE code = {code}")
        self.con.commit()
        self.cur.close()

    def insert_order(self, customer_code, product, date_in, malfunction, diagnosis, notes):

        # Inserisce nel database un nuovo ordine
        self.cur.execute("INSERT INTO orders (customer_code, status, product, date_in, malfunction, "
                         "diagnosis, notes) VALUES (?, 0, ?, ?, ?, ?, ?)",
                         (customer_code, product, date_in, malfunction, diagnosis, notes))
        self.con.commit()
        self.cur.close()

    def insert_document(self, cod, doc_type, date, ref, supplier, destination, products, shipping_exp, package_exp,
                        various_exp, withdrawal_exp, stamp_exp, iva_exp, transporter, ext_look, pack_numb, weight,
                        motivation, date_out, time_out, payment, account, notes):

        # Inserisce nel database un nuovo documento
        try:
            self.cur.execute("INSERT INTO documents (cod, type, date, ref, supplier, destination, products, "
                             "shipping_exp, package_exp, various_exp, withdrawal_exp, stamp_exp, iva_exp, transporter, "
                             "ext_look, pack_numb, weight, motivation, date_out, time_out, payment, account, notes)"
                             " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                             (cod, doc_type, date, ref, supplier, destination, str(products), shipping_exp, package_exp,
                              various_exp, withdrawal_exp, stamp_exp, iva_exp, transporter, ext_look, pack_numb, weight,
                              motivation, date_out, time_out, payment, account, notes))
            self.con.commit()
            self.cur.close()
            return True

        # Restituisce "False" se nel database risulta già registrato un altro documento con lo stesso numero documento
        except sqlite3.IntegrityError:
            return False

    def insert_product(self, cod, category, product, ean, unit, quantity, price, discount1, discount2, selling, iva):

        # Inserisce nel database un nuovo prodotto
        try:
            self.cur.execute("INSERT INTO products (cod, category, product, ean, unit, quantity, price, discount1, "
                             "discount2, selling, iva)"
                             " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                             (cod, category, product, ean, unit, quantity, price, discount1, discount2, selling, iva))
            self.con.commit()
            self.cur.close()
            return True

        # Restituisce "False" se nel database risulta già registrato un altro documento con lo stesso numero documento
        except sqlite3.IntegrityError:
            return False

    def update_product(self, cod, category, product, ean, unit, quantity, price, discount1, discount2, selling, iva,
                       history):

        # Inserisce nel database un nuovo prodotto
        try:
            self.cur.execute("UPDATE products SET "
                             "category = ?,"
                             "product = ?,"
                             "ean = ?,"
                             "unit = ?,"
                             "quantity = ?,"
                             "price = ?,"
                             "discount1 = ?,"
                             "discount2 = ?,"
                             "selling = ?,"
                             "iva = ?,"
                             "history = ?"
                             "WHERE cod = ?",
                             (category, product, ean, unit, quantity, price, discount1, discount2, selling, iva,
                              history, cod))
            self.con.commit()
            self.cur.close()
            return True

        # Restituisce "False" se nel database risulta già registrato un altro documento con lo stesso numero documento
        except sqlite3.IntegrityError:
            return False


class DataDelete:
    def __init__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        preferences = config_object["PREFERENCES"]
        filename = f"{preferences['database_path']}labor.db"
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

    def delete_customer(self, code):
        # Elimina un singolo cliente per codice
        self.cur.execute("DELETE FROM customers WHERE code = ?", (code,))
        self.con.commit()
        self.cur.close()

    def delete_supplier(self, code):
        # Elimina un singolo fornitore per codice
        self.cur.execute("DELETE FROM suppliers WHERE code = ?", (code,))
        self.con.commit()
        self.cur.close()

    def delete_order(self, code):
        # Elimina un singolo ordine per codice
        self.cur.execute("DELETE FROM orders WHERE code = ?", (code,))
        self.con.commit()
        self.cur.close()

    def delete_product(self, code):
        # Elimina un singolo prodotto per codice
        self.cur.execute("DELETE FROM products WHERE cod = ?", (code,))
        self.con.commit()
        self.cur.close()

    def delete_report(self, code):
        # Elimina un singolo rapportino per codice
        self.cur.execute("DELETE FROM reports WHERE cod = ?", (code,))
        self.con.commit()
        self.cur.close()
