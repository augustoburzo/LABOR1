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
from tkinter import END

import pygubu

from db_functions import DataRetrieve
from new_document import NewDocument

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "document_view.ui"


class DocumentView:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("document_view", master)
        builder.connect_callbacks(self)

        self.mainwindow.focus_set()

        self.main_notebook = builder.get_object("main_notebook")

        self.query_entry = builder.get_object("query_entry")
        self.query_entry.bind("<Return>", self.on_search)

        # Treeviews singole tab e binding alla funzione di doppio click
        self.pf_tv = builder.get_object("pf_tv")
        self.pf_tv.bind("<Double-1>", self.on_tv_click)
        self.of_tv = builder.get_object("of_tv")
        self.of_tv.bind("<Double-1>", self.on_tv_click)
        self.bf_tv = builder.get_object("bf_tv")
        self.bf_tv.bind("<Double-1>", self.on_tv_click)
        self.ff_tv = builder.get_object("ff_tv")
        self.ff_tv.bind("<Double-1>", self.on_tv_click)
        self.rf_tv = builder.get_object("rf_tv")
        self.rf_tv.bind("<Double-1>", self.on_tv_click)
        self.pr_tv = builder.get_object("pr_tv")
        self.pr_tv.bind("<Double-1>", self.on_tv_click)
        self.oc_tv = builder.get_object("oc_tv")
        self.oc_tv.bind("<Double-1>", self.on_tv_click)
        self.bc_tv = builder.get_object("bc_tv")
        self.bc_tv.bind("<Double-1>", self.on_tv_click)
        self.bd_tv = builder.get_object("bd_tv")
        self.bd_tv.bind("<Double-1>", self.on_tv_click)
        self.in_tv = builder.get_object("in_tv")
        self.in_tv.bind("<Double-1>", self.on_tv_click)

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def on_load(self):
        # Recupero documenti per categoria
        pf = DataRetrieve().PF_retrieve()
        of = DataRetrieve().OF_retrieve()
        bf = DataRetrieve().BF_retrieve()
        ff = DataRetrieve().FF_retrieve()
        rf = DataRetrieve().RF_retrieve()
        pr = DataRetrieve().PR_retrieve()
        oc = DataRetrieve().OC_retrieve()
        bc = DataRetrieve().BC_retrieve()
        bd = DataRetrieve().BD_retrieve()
        inv = DataRetrieve().IN_retrieve()

        # Svuota le tabelle e le popola con i dati recuperati dal db
        self.pf_tv.delete(*self.pf_tv.get_children())
        for document in pf:
            values = (document[0], document[4], document[2])
            self.pf_tv.insert("", 0, values=values)
        self.of_tv.delete(*self.of_tv.get_children())
        for document in of:
            values = (document[0], document[4], document[2])
            self.of_tv.insert("", 0, values=values)
        self.bf_tv.delete(*self.bf_tv.get_children())
        for document in bf:
            values = (document[0], document[4], document[2])
            self.bf_tv.insert("", 0, values=values)
        self.ff_tv.delete(*self.ff_tv.get_children())
        for document in ff:
            values = (document[0], document[4], document[2])
            self.ff_tv.insert("", 0, values=values)
        self.rf_tv.delete(*self.rf_tv.get_children())
        for document in rf:
            values = (document[0], document[4], document[2])
            self.rf_tv.insert("", 0, values=values)
        self.pr_tv.delete(*self.pr_tv.get_children())
        for document in pr:
            values = (document[0], document[4], document[2])
            self.pr_tv.insert("", 0, values=values)
        self.oc_tv.delete(*self.oc_tv.get_children())
        for document in oc:
            values = (document[0], document[4], document[2])
            self.oc_tv.insert("", 0, values=values)
        self.bc_tv.delete(*self.bc_tv.get_children())
        for document in bc:
            values = (document[0], document[4], document[2])
            self.bc_tv.insert("", 0, values=values)
        self.bd_tv.delete(*self.bd_tv.get_children())
        for document in bd:
            values = (document[0], document[4], document[2])
            self.bd_tv.insert("", 0, values=values)

        self.in_tv.delete(*self.in_tv.get_children())
        for document in inv:
            values = (document[0], document[4], document[2])
            self.in_tv.insert("", 0, values=values)

    def on_search(self, event=None):
        self.on_load()
        # Rileva la tab evidenziata
        tab = self.main_notebook.index("current")
        query = self.query_entry.get().upper()
        if query != "":
            if tab == 0:
                for child in self.pf_tv.get_children():
                    if query not in str(self.pf_tv.item(child)['values']).upper():
                        self.pf_tv.delete(child)

            elif tab == 1:
                for child in self.of_tv.get_children():
                    if query not in str(self.of_tv.item(child)['values']).upper():
                        self.of_tv.delete(child)

            elif tab == 2:
                for child in self.bf_tv.get_children():
                    if query not in str(self.bf_tv.item(child)['values']).upper():
                        self.bf_tv.delete(child)

            elif tab == 3:
                for child in self.ff_tv.get_children():
                    if query not in str(self.ff_tv.item(child)['values']).upper():
                        self.ff_tv.delete(child)

            elif tab == 4:
                for child in self.rf_tv.get_children():
                    if query not in str(self.rf_tv.item(child)['values']).upper():
                        self.rf_tv.delete(child)

            elif tab == 5:
                for child in self.pr_tv.get_children():
                    if query not in str(self.pr_tv.item(child)['values']).upper():
                        self.pr_tv.delete(child)

            elif tab == 6:
                for child in self.oc_tv.get_children():
                    if query not in str(self.oc_tv.item(child)['values']).upper():
                        self.oc_tv.delete(child)

            elif tab == 7:
                for child in self.bc_tv.get_children():
                    if query not in str(self.bc_tv.item(child)['values']).upper():
                        self.bc_tv.delete(child)

            elif tab == 8:
                for child in self.bd_tv.get_children():
                    if query not in str(self.bd_tv.item(child)['values']).upper():
                        self.bd_tv.delete(child)

            elif tab == 9:
                for child in self.in_tv.get_children():
                    if query not in str(self.in_tv.item(child)['values']).upper():
                        self.in_tv.delete(child)

    def on_tv_click(self, event=None):
        # Scelta documento in una delle tab
        doc_idx = 0
        tab = self.main_notebook.index("current")
        if tab == 0:
            item = self.pf_tv.selection()
            for i in item:
                doc_idx = self.pf_tv.item(i, 'values')[0]

        elif tab == 1:
            item = self.of_tv.selection()
            for i in item:
                doc_idx = self.of_tv.item(i, 'values')[0]

        elif tab == 2:
            item = self.bf_tv.selection()
            for i in item:
                doc_idx = self.bf_tv.item(i, 'values')[0]

        elif tab == 3:
            item = self.ff_tv.selection()
            for i in item:
                doc_idx = self.ff_tv.item(i, 'values')[0]

        elif tab == 4:
            item = self.rf_tv.selection()
            for i in item:
                doc_idx = self.rf_tv.item(i, 'values')[0]

        elif tab == 5:
            item = self.pr_tv.selection()
            for i in item:
                doc_idx = self.pr_tv.item(i, 'values')[0]

        elif tab == 6:
            item = self.oc_tv.selection()
            for i in item:
                doc_idx = self.oc_tv.item(i, 'values')[0]

        elif tab == 7:
            item = self.bc_tv.selection()
            for i in item:
                doc_idx = self.bc_tv.item(i, 'values')[0]

        elif tab == 8:
            item = self.bd_tv.selection()
            for i in item:
                doc_idx = self.bd_tv.item(i, 'values')[0]

        elif tab == 9:
            item = self.in_tv.selection()
            for i in item:
                doc_idx = self.in_tv.item(i, 'values')[0]

        else:
            pass

        if doc_idx != 0:
            # Verifica che sia stato scelto un documento ed apre la finestra
            NewDocument(edit=True, doc_num=doc_idx, master=self.mainwindow).mainwindow.grab_set()


if __name__ == "__main__":
    app = DocumentView()
    app.run()
