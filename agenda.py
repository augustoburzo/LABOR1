import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import datetime

class Scadenziario:
    def __init__(self, root):
        self.root = root
        self.root.title("Scadenziario")
        self.root.geometry("500x400")
        
        # Creazione del calendario
        self.cal_frame = tk.Frame(self.root)
        self.cal_frame.pack(pady=10)
        
        self.cal_label = tk.Label(self.cal_frame, text="Seleziona una data:")
        self.cal_label.pack(pady=5)
        self.cal = Calendar(self.cal_frame, selectmode="day", date_pattern="dd/MM/yyyy")
        self.cal.pack(pady=5)
        
        # Creazione dei campi di input
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        
        self.desc_label = tk.Label(self.input_frame, text="Descrizione:")
        self.desc_label.grid(row=0, column=0, padx=10, pady=5)
        self.desc_entry = tk.Entry(self.input_frame)
        self.desc_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Creazione del pulsante Aggiungi
        self.add_button = tk.Button(self.input_frame, text="Aggiungi", command=self.add_entry)
        self.add_button.grid(row=1, column=1, padx=10, pady=5)
        
        # Creazione della tabella delle scadenze
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10)
        
        self.table_columns = ("Data", "Descrizione")
        self.table = tk.ttk.Treeview(self.table_frame, columns=self.table_columns, show="headings")
        
        for col in self.table_columns:
            self.table.heading(col, text=col.title())
        
        self.table.pack()
        
    def add_entry(self):
        # Validazione dei dati inseriti
        try:
            date = datetime.strptime(str(self.cal.selection_get()), "%d/%m/%Y")
        except ValueError:
            tk.messagebox.showerror("Errore", "Data non valida. Selezionare una data.")
            return
        
        desc = self.desc_entry.get()
        if not desc:
            tk.messagebox.showerror("Errore", "Inserire una descrizione.")
            return
        
        # Aggiunta dell'entry alla tabella
        self.table.insert("", tk.END, values=(date.strftime("%d/%m/%Y"), desc))
        
        # Pulizia dei campi di input
        self.desc_entry.delete(0, tk.END)
        

if __name__ == "__main__":
    root = tk.Tk()
    scadenziario = Scadenziario(root)
    root.mainloop()
