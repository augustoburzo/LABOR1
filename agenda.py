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

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "agenda.ui"


class Agenda:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Database
        self.db = sqlite3.connect("agenda.db")
        self.cur = self.db.cursor()

        # Main widget
        self.mainwindow = builder.get_object("main_window", master)
        builder.connect_callbacks(self)

        Style('labor')

        # Entries
        self.event_entry = builder.get_object("event_entry")
        self.descr_text = builder.get_object("descr_text")
        self.date_entry = builder.get_object("date_entry")
        self.contact_entry = builder.get_object("contact_entry")
        # Calendar picker
        self.cal_btn = builder.get_object("cal_btn")
        self.cal_btn.configure(text="📆")
        # Treeview eventi
        self.events_tv = builder.get_object("events_tv")
        self.events_tv.bind("<Double-1>", self.on_event_selected)
        self.events_tv.tag_configure('FUTURO', background='#2c2ca0', foreground="#dbe2e3")
        self.events_tv.tag_configure('SCADUTO', background='#161650', foreground="#dbe2e3")
        self.events_tv.tag_configure('SCADENZA', background='#212178', foreground="#dbe2e3")

        # Evento selezionato
        self.event = None

        # Carica gli eventi
        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

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
        pass

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


if __name__ == "__main__":
    app = Agenda()
    app.run()

