#!/usr/bin/python3
from calendar import Calendar
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import calendar
import tkcalendar


class Agenda:
    def __init__(self, master=None):
        # build ui
        self.main_window = tk.Tk() if master is None else tk.Toplevel(master)
        self.main_window.configure(height=200, width=200)
        self.main_window.geometry("800x600")
        self.left_frm = ttk.Frame(self.main_window)
        self.left_frm.configure(height=200, width=200)
        self.event_lbl = ttk.Label(self.left_frm)
        self.event_lbl.configure(text='Evento:')
        self.event_lbl.grid(column=0, row=0, sticky="e")
        self.event_entry = ttk.Entry(self.left_frm)
        self.event_entry.grid(column=1, row=0, sticky="ew")
        self.descr_lbl = ttk.Label(self.left_frm)
        self.descr_lbl.configure(text='Descrizione:')
        self.descr_lbl.grid(column=0, row=1, sticky="e")
        self.descr_text = tk.Text(self.left_frm)
        self.descr_text.configure(height=6, width=20)
        self.descr_text.grid(column=1, pady="0 10", row=1, sticky="nsew")
        self.date_calendar = ttk.dialogs.dialogs.calendar(self.left_frm)
        self.date_calendar.grid(column=1, row=2, sticky="ew")
        self.date_lbl = ttk.Label(self.left_frm)
        self.date_lbl.configure(text='Data:')
        self.date_lbl.grid(column=0, row=2, sticky="e")
        self.contact_lbl = ttk.Label(self.left_frm)
        self.contact_lbl.configure(text='Contatto:')
        self.contact_lbl.grid(column=0, row=3, sticky="e")
        self.contact_entry = ttk.Entry(self.left_frm)
        self.contact_entry.grid(column=1, row=3, sticky="ew")
        self.left_frm.grid(
            column=0,
            padx="10 5",
            pady="10 0",
            row=0,
            sticky="nsew")
        self.left_frm.rowconfigure("all", pad=10, weight=1)
        self.left_frm.columnconfigure(1, weight=1)
        self.left_frm.columnconfigure("all", pad=10)
        self.right_frm = ttk.Frame(self.main_window)
        self.right_frm.configure(height=200, width=200)
        self.events_tv = ttk.Treeview(self.right_frm)
        self.events_tv.configure(selectmode="extended", show="headings")
        self.events_tv_cols = ['date_col', 'event_col']
        self.events_tv_dcols = ['date_col', 'event_col']
        self.events_tv.configure(
            columns=self.events_tv_cols,
            displaycolumns=self.events_tv_dcols)
        self.events_tv.column(
            "date_col",
            anchor="w",
            stretch="false",
            width=80,
            minwidth=80)
        self.events_tv.column(
            "event_col",
            anchor="w",
            stretch="true",
            width=200,
            minwidth=20)
        self.events_tv.heading("date_col", anchor="w", text='Data')
        self.events_tv.heading("event_col", anchor="w", text='Evento')
        self.events_tv.grid(column=0, row=0, sticky="nsew")
        self.right_frm.grid(
            column=1,
            padx="5 10",
            pady="10 0",
            row=0,
            sticky="nsew")
        self.right_frm.rowconfigure(0, weight=1)
        self.right_frm.columnconfigure(0, weight=1)
        self.toolbar_frm = ttk.Frame(self.main_window)
        self.toolbar_frm.configure(height=32, width=200)
        self.toolbar_frm.grid(
            column=0,
            columnspan=2,
            padx=10,
            pady="0 10",
            row=1,
            sticky="ew")
        self.main_window.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(1, weight=5)

        # Main widget
        self.mainwindow = self.main_window

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = Agenda()
    app.run()
