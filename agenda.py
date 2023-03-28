#!/usr/bin/python3
import datetime
import pathlib
from tkinter import END
import sqlite3

import pygubu
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs.dialogs import DatePickerDialog, Messagebox
from ttkbootstrap.toast import ToastNotification

from xl_functions import XLSaver

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "agenda.ui"


class DoneWin(ttk.Toplevel):
    def __init__(self, master=None, events=None, **kw):
        super(DoneWin, self).__init__(master, **kw)
        events_tv = ttk.Treeview(self)
        events_tv.configure(selectmode="extended", show="headings")
        events_tv_cols = [
            'column1',
            'column2',
            'column3',
            'column4',
            'column5']
        events_tv_dcols = ['column2', 'column3', 'column4', 'column5']
        events_tv.configure(
            columns=events_tv_cols,
            displaycolumns=events_tv_dcols)
        events_tv.column(
            "column1",
            anchor="w",
            stretch=True,
            width=0,
            minwidth=0)
        events_tv.column(
            "column2",
            anchor="w",
            stretch=False,
            width=80,
            minwidth=20)
        events_tv.column(
            "column3",
            anchor="w",
            stretch=False,
            width=200,
            minwidth=20)
        events_tv.column(
            "column4",
            anchor="w",
            stretch=True,
            width=200,
            minwidth=20)
        events_tv.column(
            "column5",
            anchor="w",
            stretch=False,
            width=120,
            minwidth=20)
        events_tv.heading("column1", anchor="w", text='Id')
        events_tv.heading("column2", anchor="w", text='Data')
        events_tv.heading("column3", anchor="w", text='Evento')
        events_tv.heading("column4", anchor="w", text='Descrizione')
        events_tv.heading("column5", anchor="w", text='Contatto')
        events_tv.pack(expand=True, fill="both", side="top")
        for event in events:
            events_tv.insert("", END, values=event)
        self.configure(height=200, width=200)
        self.geometry("1024x480")
        self.iconbitmap("agenda.ico")
        self.focus_set()
        self.title("Attività completate")


class Agenda:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Database
        self.db = sqlite3.connect("agenda.db")
        self.cur = self.db.cursor()
        # Ricava la data di oggi
        self.now = datetime.datetime.now()

        # Main widget
        self.mainwindow = builder.get_object("main_window", master)
        builder.connect_callbacks(self)

        Style('labor')

        # Entries
        self.event_entry = builder.get_object("event_entry")
        self.event_entry.focus_set()
        self.descr_text = builder.get_object("descr_text")
        self.descr_text.bind("<Tab>", self.focus_next_widget)
        self.date_entry = builder.get_object("date_entry")
        self.contact_entry = builder.get_object("contact_entry")
        # Calendar picker
        self.cal_btn = builder.get_object("cal_btn")
        self.cal_btn.configure(text="📆")
        # Treeview eventi
        self.events_tv = builder.get_object("events_tv")
        self.scrollbar = builder.get_object("scrollbar")
        self.scrollbar.configure(command=self.events_tv.yview)
        self.events_tv.bind("<Double-1>", self.on_event_selected)
        self.events_tv.configure(yscrollcommand=self.scrollbar.set)
        self.events_tv.tag_configure('FUTURO', background='#2c2ca0', foreground="#dbe2e3")
        self.events_tv.tag_configure('SCADUTO', background='#161650', foreground="#dbe2e3")
        self.events_tv.tag_configure('SCADENZA', background='#212178', foreground="#dbe2e3")

        # Evento selezionato
        self.event = None

        # Carica gli eventi
        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def show_done(self):
        self.cur.execute("SELECT * FROM agenda WHERE status = 1 ORDER BY date ASC")
        events = self.cur.fetchall()
        DoneWin(master=self.mainwindow, events=events)

    def on_load(self):
        self.events_tv.delete(*self.events_tv.get_children())

        self.cur.execute('''CREATE TABLE IF NOT EXISTS agenda (
                        "id"	INTEGER NOT NULL,
                        "date"	TEXT NOT NULL,
                        "event"	TEXT NOT NULL,
                        "descr"	TEXT,
                        "contact"	TEXT,
                        "status"    INTEGER,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    );''')
        self.db.commit()
        self.cur.execute("SELECT * FROM agenda WHERE status = 0 ORDER BY date ASC")
        events = self.cur.fetchall()
        for event in events:
            event = (event[0], event[1], event[2])
            tag = "FUTURO"
            event_date = datetime.datetime.strptime(event[1], "%d/%m/%Y")
            if event_date.date() < datetime.date.today():
                tag = "SCADUTO"
            elif event_date.date() == datetime.date.today():
                tag = "SCADENZA"
            self.events_tv.insert("", END, values=event, tags=tag)
        self.event_entry.delete(0, END)
        self.descr_text.delete(1.0, END)
        self.date_entry.delete(0, END)
        self.date_entry.insert(0, self.now.strftime("%d/%m/%Y"))
        self.contact_entry.delete(0, END)

    def show_calendar(self):
        date = DatePickerDialog(title="Scegli una data", parent=self.date_entry)
        self.date_entry.delete(0, END)
        date = date.date_selected.strftime("%d/%m/%Y")
        self.date_entry.insert(0, date)

    def on_insert_press(self):
        if self.date_entry.get() and self.event_entry.get() != "":
            self.cur.execute('''INSERT INTO "agenda" ("date", "event", "descr", "contact", "status") 
                                 VALUES (?, ?, ?, ?, ?);''',
                             (self.date_entry.get(), self.event_entry.get(), self.descr_text.get(1.0, END),
                              self.contact_entry.get(), 0))
            self.db.commit()
            self.on_load()

        elif self.date_entry.get() == "" and self.event_entry.get() == "":
            pass

        else:
            toast = ToastNotification(
                title="Completare i dati!",
                message="Inserire la data o il nome dell'evento",
                duration=5000,
                bootstyle='danger',
                icon="😒"
            )
            toast.show_toast()

    def on_update_press(self):
        self.cur.execute('''UPDATE agenda SET
                            date = ?,
                            event = ?,
                            descr = ?,
                            contact = ?
                            WHERE id = ?''', (
                         self.date_entry.get(), self.event_entry.get(), self.descr_text.get(1.0, END),
                         self.contact_entry.get(), self.event))
        self.db.commit()
        self.on_load()

    def on_delete_press(self):
        ask = False
        if self.event is not None:
            ask = Messagebox.yesno(parent=self.mainwindow, title="Eliminare evento?",
                                   message="Sei sicuro di voler eliminare l'evento?",
                                   alert=True)
        if ask:
            self.cur.execute("DELETE FROM agenda WHERE id = ?", (self.event,))

    def on_done_press(self):
        self.cur.execute('''UPDATE agenda SET
                                    status = 1
                                    WHERE id = ?''', (self.event,))
        self.db.commit()
        self.on_load()

    def on_event_selected(self, event=None):
        self.event_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.descr_text.delete(1.0, END)
        self.contact_entry.delete(0, END)
        item = self.events_tv.selection()
        for i in item:
            event_idx = self.events_tv.item(i, "values")[0]
            self.event = event_idx
            self.cur.execute("SELECT * FROM agenda WHERE id = ?", (event_idx,))
            event = self.cur.fetchone()
            self.event_entry.insert(0, event[2])
            self.date_entry.insert(0, event[1])
            self.descr_text.insert(1.0, event[3][:-1])
            self.contact_entry.insert(0, event[4])

    def on_export_press(self):
        self.cur.execute("SELECT * FROM agenda WHERE status = 0 ORDER BY date ASC")
        events = self.cur.fetchall()
        excel = XLSaver()
        excel.agenda(events)
        self.mainwindow.focus_set()


if __name__ == "__main__":
    app = Agenda()
    app.run()

