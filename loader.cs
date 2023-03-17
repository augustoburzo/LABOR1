namespace Namespace {
    
    using System.Collections.Generic;
    
    using datetime;
    
    using os;
    
    using pathlib;
    
    using sys;
    
    using threading;
    
    using time;
    
    using tkinter.messagebox;
    
    using ConfigParser = configparser.ConfigParser;
    
    using shutil;
    
    using ZipFile = zipfile.ZipFile;
    
    using ToastNotification = ttkbootstrap.toast.ToastNotification;
    
    using CompanyConfig = company_config.CompanyConfig;
    
    using Credits = credits.Credits;
    
    using CustomerView = customer_view.CustomerView;
    
    using DataRetrieve = db_functions.DataRetrieve;
    
    using DBInit = db_functions.DBInit;
    
    using DataDelete = db_functions.DataDelete;
    
    using DataWrite = db_functions.DataWrite;
    
    using DocumentView = document_view.DocumentView;
    
    using OrderInsertWindow = order_insert_window.OrderInsertWindow;
    
    using pygubu;
    
    using ttk = ttkbootstrap;
    
    using Style = ttkbootstrap.Style;
    
    using ToolTip = ttkbootstrap.tooltip.ToolTip;
    
    using OrderView = order_view.OrderView;
    
    using Prints = pdf_functions.Prints;
    
    using PreferencesWindow = preferences_window.PreferencesWindow;
    
    using ProductInsert = product_insert.ProductInsert;
    
    using SingleOrderView = single_order_view.SingleOrderView;
    
    using SingleProductView = single_product_view.SingleProductView;
    
    using SupplierView = supplier_view.SupplierView;
    
    using WarehouseManagementWindow = warehouse_management_window.WarehouseManagementWindow;
    
    using NewDocument = new_document.NewDocument;
    
    using WorkReport = work_report.WorkReport;
    
    using pyi_splash;
    
    public static class Module {
        
        public static object @__author__ = "Augusto Burzo";
        
        public static object @__copyright__ = "Copyright 2023 - Augusto Burzo";
        
        public static object @__credits__ = new List<object> {
            "Augusto Burzo"
        };
        
        public static object @__license__ = "Proprietary";
        
        public static object @__version__ = "1.2.0";
        
        public static object @__maintainer__ = "Augusto Burzo";
        
        public static object @__email__ = "info@augustoburzo.com";
        
        public static object @__status__ = "Beta";
        
        public static object PROJECT_PATH = pathlib.Path(@__file__).parent;
        
        public static object PROJECT_UI = PROJECT_PATH / "main_window.ui";
        
        public class MainWindow {
            
            public MainWindow(object master = null, object translator = null) {
                this.builder = pygubu.Builder(translator);
                builder.add_resource_path(PROJECT_PATH);
                builder.add_from_file(PROJECT_UI);
                var config_object = ConfigParser();
                config_object.read("company.ini");
                var companyinfo = config_object["COMPANYINFO"];
                // Main widget
                this.mainwindow = builder.get_object("main_window", master);
                builder.connect_callbacks(this);
                this.mainwindow.title("Labor1 | {companyinfo['company']} - {companyinfo['city']} ({companyinfo['prov']})");
                Style("labor");
                this.mainwindow.state("zoomed");
                this.mainwindow.protocol("WM_DELETE_WINDOW", this.on_close);
                DBInit();
                // Inizializza le treeview della sezione ordini
                this.waiting_tv = builder.get_object("waiting_tv");
                this.waiting_tv.bind("<Double-1>", this.on_order_click);
                this.progress_tv = builder.get_object("progress_tv");
                this.progress_tv.bind("<Double-1>", this.on_order_click);
                this.done_tv = builder.get_object("done_tv");
                this.done_tv.bind("<Double-1>", this.on_order_click);
                // Inizializza le funzioni della sezione magazzino
                this.in_stock_tv = builder.get_object("in_stock_tv");
                this.in_stock_tv.bind("<Double-1>", this.on_product_tv_press);
                this.ending_tv = builder.get_object("ending_tv");
                this.ending_tv.bind("<Double-1>", this.on_product_tv_press);
                this.wh_search_entry = builder.get_object("wh_search_entry");
                this.wh_search_entry.bind("<Return>", this.on_search_btn_press);
                this.separator1 = builder.get_object("separator1");
                this.separator1.configure(orient: "vertical", style: "info.Vertical.TSeparator");
                // Binding dei ToolTip sui tasti d'interfaccia
                this.customers_list_btn = builder.get_object("customers_list_btn");
                ToolTip(this.customers_list_btn, text: "Consulta anagrafiche clienti", bootstyle: PRIMARY);
                this.suppliers_list_btn = builder.get_object("suppliers_list_btn");
                ToolTip(this.suppliers_list_btn, text: "Consulta anagrafiche fornitori", bootstyle: PRIMARY);
                this.btn_orders = builder.get_object("btn_orders");
                ToolTip(this.btn_orders, text: "Consulta lista ordini", bootstyle: PRIMARY);
                this.new_document_btn = builder.get_object("new_document_btn");
                ToolTip(this.new_document_btn, text: "Inserisci nuovo documento", bootstyle: PRIMARY);
                this.new_prev_btn = builder.get_object("new_prev_btn");
                ToolTip(this.new_prev_btn, text: "Genera nuovo preventivo", bootstyle: PRIMARY);
                this.add_prd_btn = builder.get_object("add_prd_btn");
                ToolTip(this.add_prd_btn, text: "Inserisci nuovo prodotto", bootstyle: PRIMARY);
                this.report_btn = builder.get_object("report_btn");
                ToolTip(this.report_btn, text: "Inserisci o gestisci i rapportini", bootstyle: PRIMARY);
                this.settings_btn = builder.get_object("settings_btn");
                ToolTip(this.settings_btn, text: "Gestisci le impostazioni", bootstyle: PRIMARY);
                this.delete_btn = builder.get_object("delete_btn");
                this.delete_btn.configure(style: "danger.TButton");
                ToolTip(this.delete_btn, text: "Elimina l'ordine", bootstyle: DANGER);
                this.in_progress_btn = builder.get_object("in_progress_btn");
                this.in_progress_btn.configure(bootstyle: "success");
                ToolTip(this.in_progress_btn, text: "Metti l'ordine in lavorazione", bootstyle: PRIMARY);
                this.done_btn = builder.get_object("done_btn");
                this.done_btn.configure(style: "warning.TButton");
                ToolTip(this.done_btn, text: "Contrassegna l'ordine come lavorato", bootstyle: PRIMARY);
                this.delivered_btn = builder.get_object("delivered_btn");
                this.delivered_btn.configure(bootstyle: "info");
                ToolTip(this.delivered_btn, text: "Contrassegna l'ordine come restituito", bootstyle: PRIMARY);
                // Carica i dati dal db per popolare le tabelle della schermata principale
                this.waiting_orders = DataRetrieve().waiting_orders();
                this.in_progress_orders = DataRetrieve().in_progress_orders();
                this.done_orders = DataRetrieve().done_orders();
                this.warehouse_lf = builder.get_object("warehouse_lf");
                this.overview_lf = builder.get_object("overview_lf");
                this.overview_notebook = builder.get_object("overview_notebook");
                this.warehouse_notebook = builder.get_object("warehouse_notebook");
                this.on_load();
                this.auto_update_daemon();
            }
            
            public virtual object run() {
                if (getattr(sys, "frozen", false)) {
                    pyi_splash.close();
                }
                this.mainwindow.mainloop();
            }
            
            public virtual object on_load() {
                object values;
                object last_name;
                object first_name;
                object company;
                object customer;
                object malfunction;
                object date_out;
                object date_in;
                object product;
                object status;
                object cust_code;
                object code;
                DBInit();
                this.waiting_tv.delete(this.waiting_tv.get_children());
                this.progress_tv.delete(this.progress_tv.get_children());
                this.done_tv.delete(this.done_tv.get_children());
                // Attiva la ricerca del database e la consultazione delle tabelle ordini
                // Ordini in attesa
                foreach (var order in this.waiting_orders) {
                    code = order[0];
                    cust_code = order[1];
                    status = order[2];
                    product = order[3];
                    date_in = order[4];
                    date_out = order[5];
                    malfunction = order[6];
                    customer = DataRetrieve().single_customer_code(cust_code);
                    company = customer[1];
                    first_name = customer[2];
                    last_name = customer[3];
                    values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction);
                    this.waiting_tv.insert("", END, values: values);
                }
                // Ordini in corso
                foreach (var order in this.in_progress_orders) {
                    code = order[0];
                    cust_code = order[1];
                    status = order[2];
                    product = order[3];
                    date_in = order[4];
                    date_out = order[5];
                    malfunction = order[6];
                    customer = DataRetrieve().single_customer_code(cust_code);
                    company = customer[1];
                    first_name = customer[2];
                    last_name = customer[3];
                    values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction);
                    this.progress_tv.insert("", END, values: values);
                }
                // Ordini completati
                foreach (var order in this.done_orders) {
                    code = order[0];
                    cust_code = order[1];
                    status = order[2];
                    product = order[3];
                    date_in = order[4];
                    date_out = order[5];
                    malfunction = order[6];
                    customer = DataRetrieve().single_customer_code(cust_code);
                    company = customer[1];
                    first_name = customer[2];
                    last_name = customer[3];
                    values = (code, status, product, company, first_name, last_name, date_in, date_out, malfunction);
                    this.done_tv.insert("", END, values: values);
                }
                // Attiva la ricerca del database e la consultazione della tabella magazzino
                this.in_stock_tv.delete(this.in_stock_tv.get_children());
                var wharehouse = DataRetrieve().warehouse_status();
                foreach (var product in wharehouse) {
                    this.in_stock_tv.insert("", END, values: product);
                }
                var products_low = DataRetrieve().warehouse_low_qty();
                this.ending_tv.delete(this.ending_tv.get_children());
                foreach (var productl in products_low) {
                    this.ending_tv.insert("", END, values: productl);
                }
            }
            
            public virtual object on_close() {
                // Chiede conferma per chiusura programma
                var answer = tkinter.messagebox.askyesno(title: "Chiusura programma", message: "Sei sicuro di voler chiudere Labor1?");
                if (answer) {
                    this.mainwindow.destroy();
                }
            }
            
            public virtual object update_lookup() {
                // Funzione di ricerca aggiornamenti lavorazioni in loop
                while (1) {
                    time.sleep(1);
                    var waiting_orders = DataRetrieve().waiting_orders();
                    var in_progress_orders = DataRetrieve().in_progress_orders();
                    var done_orders = DataRetrieve().done_orders();
                    if (waiting_orders != this.waiting_orders) {
                        this.waiting_orders = waiting_orders;
                        this.on_load();
                        time.sleep(1);
                    } else if (in_progress_orders != this.in_progress_orders) {
                        this.in_progress_orders = in_progress_orders;
                        this.on_load();
                        time.sleep(1);
                    } else if (done_orders != this.done_orders) {
                        this.done_orders = done_orders;
                        this.on_load();
                        time.sleep(1);
                    } else {
                        time.sleep(1);
                    }
                }
            }
            
            public virtual object auto_update_daemon() {
                // Attiva il daemon di ricerca
                var newthread = threading.Thread(target: this.update_lookup);
                newthread.daemon = true;
                newthread.start();
                Console.WriteLine("Daemon STARTED\n");
            }
            
            public virtual object on_order_click(object @event = null) {
                // Ricava l'ordine su cui si è cliccatto a seconda della tab in cui ci si trova
                var order_idx = "0";
                var tab = this.overview_notebook.index("current");
                if (tab == 0) {
                    var item = this.waiting_tv.selection();
                    foreach (var i in item) {
                        order_idx = this.waiting_tv.item(i, "values")[0];
                    }
                } else if (tab == 1) {
                    item = this.progress_tv.selection();
                    foreach (var i in item) {
                        order_idx = this.progress_tv.item(i, "values")[0];
                    }
                } else if (tab == 2) {
                    item = this.done_tv.selection();
                    foreach (var i in item) {
                        order_idx = this.done_tv.item(i, "values")[0];
                    }
                }
                if (order_idx != "0") {
                    // Controlla che sia stato selezionato almeno un ordine
                    SingleOrderView(code: order_idx, master: this.mainwindow).mainwindow.grab_set();
                }
            }
            
            public virtual object on_preferences_press() {
                // Apre la finestra impostazioni
                PreferencesWindow(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_new_product_press() {
                // Apre la finestra di inserimento singolo prodotto
                ProductInsert(single: true, status: "in", treeview: null, function: null, master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_new_document_press() {
                // Apre la finestra di inserimento documento
                NewDocument(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_customers_print_press() {
                // Esporta file *.pdf lista clienti
                var data = DataRetrieve();
                var customers = data.all_customers();
                var pdf = Prints();
                pdf.customers_list(customers);
                this.mainwindow.focus_set();
            }
            
            public virtual object on_company_config_press() {
                // Apre finestra di configurazione anagrafica azienda
                CompanyConfig(this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_suppliers_print_press() {
                // Esporta file *.pdf lista fornitori
                var data = DataRetrieve();
                var suppliers = data.all_suppliers();
                var pdf = Prints();
                pdf.suppliers_list(suppliers);
                this.mainwindow.focus_set();
            }
            
            public virtual object on_orders_view_press() {
                // Apre finestra ricerca e aggiunta ordini
                var order_view = OrderView;
                order_view(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_warehouse_view_press() {
                // Apre finestra ricerca magazzino
                WarehouseManagementWindow(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_suppliers_view_press() {
                // Apre finestra ricerca e aggiunta fornitori
                SupplierView(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_customers_list_press() {
                // Apre finestra lista clienti
                CustomerView(win: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_in_progress_press() {
                // Mette in lavorazione un nuovo ordine
                var item = this.waiting_tv.selection();
                // Verifica che sia selezionata una voce all'interno della treeview
                if (item != ValueTuple.Create("<Empty>")) {
                    foreach (var i in item) {
                        var order_idx = this.waiting_tv.item(i, "values")[0];
                        var askinprogress = tkinter.messagebox.askyesno(title: "Mettere in lavorazione?", message: "Sei sicuro di voler mettere in lavorazione l'ordine N°{order_idx}?");
                        if (askinprogress) {
                            DataWrite().order_update(order_idx, 1);
                            var toast = ToastNotification(title: "Ordine in lavorazione", message: "L'ordine è stato contrassegnato come in lavorazione!", duration: 3000, icon: "☺", bootstyle: "success");
                            toast.show_toast();
                        }
                    }
                    this.mainwindow.focus_set();
                } else {
                    tkinter.messagebox.showerror(parent: this.mainwindow, title: "Seleziona voce", message: "Seleziona una voce da trasferire.");
                }
            }
            
            public virtual object on_delete_button_press() {
                // Elimina l'ordine richiesto ricavando la selezione dalla treeview degli ordini in attesa
                var item = this.waiting_tv.selection();
                if (item != ValueTuple.Create("<Empty>")) {
                    foreach (var i in item) {
                        var order_idx = this.waiting_tv.item(i, "values")[0];
                        var askdelete = tkinter.messagebox.askyesno(title: "Eliminare ordine?", message: "Sei sicuro di voler eliminare l'ordine N°{order_idx}?");
                        if (askdelete) {
                            DataDelete().delete_order(order_idx);
                            this.on_load();
                        }
                        this.mainwindow.focus_set();
                    }
                } else {
                    tkinter.messagebox.showerror(parent: this.mainwindow, title: "Seleziona voce", message: "Seleziona una voce da eliminare.");
                }
            }
            
            public virtual object on_done_btn_press() {
                // Sposta l'ordine nella sezione "Completati"
                var item = this.progress_tv.selection();
                if (item != ValueTuple.Create("<Empty>")) {
                    foreach (var i in item) {
                        var order_idx = this.progress_tv.item(i, "values")[0];
                        var askinprogress = tkinter.messagebox.askyesno(title: "Completare l'ordine?", message: "Sei sicuro di voler contrassegnare come completato l'ordine N°{order_idx}?");
                        if (askinprogress) {
                            DataWrite().order_update(order_idx, 2);
                            var toast = ToastNotification(title: "Ordine completato", message: "L'ordine è stato contrassegnato come completato!", duration: 3000, icon: "☺", bootstyle: "success");
                            toast.show_toast();
                        }
                    }
                    this.mainwindow.focus_set();
                } else {
                    tkinter.messagebox.showerror(parent: this.mainwindow, title: "Seleziona voce", message: "Seleziona una voce da trasferire.");
                }
            }
            
            public virtual object on_delivered_press() {
                // Sposta l'ordine nella sezione "Restituiti"
                var item = this.done_tv.selection();
                if (item != ValueTuple.Create("<Empty>")) {
                    foreach (var i in item) {
                        var order_idx = this.done_tv.item(i, "values")[0];
                        var askinprogress = tkinter.messagebox.askyesno(title: "Consegnare l'ordine?", message: "Sei sicuro di voler contrassegnare come restituito l'ordine N°{order_idx}?");
                        if (askinprogress) {
                            DataWrite().order_update(order_idx, 3);
                        }
                    }
                    var toast = ToastNotification(title: "Ordine consegnato", message: "L'ordine è stato consegnato!", duration: 3000, icon: "☺", bootstyle: "success");
                    toast.show_toast();
                    this.mainwindow.focus_set();
                } else {
                    tkinter.messagebox.showerror(parent: this.mainwindow, title: "Seleziona voce", message: "Seleziona una voce da consegnare.");
                }
            }
            
            public virtual object on_insert_order_press() {
                // Apre la finestra di inserimento ordini
                var order_insert = OrderInsertWindow;
                order_insert(master: this.mainwindow);
            }
            
            public virtual object on_search_btn_press(object @event = null) {
                // Ricerca il prodotto indicato nella entry della sezione magazzino
                var query = this.wh_search_entry.get();
                var products = DataRetrieve().single_product_code(query);
                if (!products) {
                    products = DataRetrieve().single_product_name(query);
                }
                this.in_stock_tv.delete(this.in_stock_tv.get_children());
                foreach (var product in products) {
                    this.in_stock_tv.insert("", END, values: product);
                }
            }
            
            public virtual object on_settings_press() {
                PreferencesWindow(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_close_command_press() {
                // Chiude l'applicativo senza chiedere conferma
                this.mainwindow.destroy();
            }
            
            public virtual object on_product_tv_press(object @event = null) {
                object item;
                // Callback sulla selezione di un prodotto dalle tabelle di magazzino
                var product_idx = "0";
                var tab = this.warehouse_notebook.index("current");
                try {
                    if (tab == 0) {
                        item = this.in_stock_tv.selection();
                        foreach (var i in item) {
                            product_idx = this.in_stock_tv.item(i, "values")[0];
                        }
                    } else if (tab == 1) {
                        item = this.ending_tv.selection();
                        foreach (var i in item) {
                            product_idx = this.ending_tv.item(i, "values")[0];
                        }
                    }
                    if (product_idx != "0") {
                        // Verifica che sia stato selezionato almeno un prodotto
                        SingleProductView(master: this.mainwindow, code: product_idx, function: this.on_load).mainwindow.grab_set();
                    }
                } catch (IndexError) {
                }
            }
            
            public virtual object on_new_prev_press() {
                // Apre la finestra "Nuovo documento" già sulla sezione "Nuovo preventivo"
                NewDocument(preventive: true, master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object on_report_press() {
                // Apre la finestra di generazione rapportini di lavoro
                WorkReport(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object backup() {
                // Crea una copia esatta del database e la archivia nella cartella di backup indicata nel file di configurazione comprimendola
                // in un file zip e dando al file come nome la data odierna
                var config_object = ConfigParser();
                config_object.read("config.ini");
                var preferences = config_object["PREFERENCES"];
                var database = "{preferences['database_path']}sir.db";
                var backup = "{preferences['backup_path']}sir.db";
                shutil.copyfile(database, backup);
                var compressed = "{preferences['backup_path']}Backup {datetime.date.today()}.zip";
                using (var myzip = ZipFile(compressed, "w")) {
                    myzip.write(backup);
                }
                os.remove(backup);
            }
            
            public virtual object on_documents_press() {
                DocumentView(master: this.mainwindow).mainwindow.grab_set();
            }
            
            public virtual object credits_win() {
                Credits(master: this.mainwindow).mainwindow.grab_set();
            }
        }
        
        public static object app = MainWindow();
        
        static Module() {
            app.run();
        }
    }
}
