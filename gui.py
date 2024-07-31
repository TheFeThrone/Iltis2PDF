import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from utils.helpers import _on_mouse_wheel, update_label, truncate, update_config
from utils.tool_tip import create_tooltip
from handlers.iltis_handler import fetch_hyperlinks, refresh_hyperlinks
from handlers.printer_handler import save_hyperlinks_as_pdf

config_file = "config.json"

def select_all(checkbuttons, var_all):
    is_checked = var_all.get()
    for cb, var in checkbuttons:
        var.set(is_checked)

def on_sort_toggle(checkbuttons, refresh_hyperlinks, links_inner_frame, var_all, sort_var, create_tooltip, truncate):
    hyperlinks = [var.link for cb, var in checkbuttons]
    refresh_hyperlinks(hyperlinks, links_inner_frame, checkbuttons, var_all, sort_var, create_tooltip, truncate)

def save_selected_hyperlinks(driver, iltis_url_entry, checkbuttons, stop_flag, update_label, print_status_label, print_error_status_label, root):
    stop_flag = False  
    update_config(config_file, 'stop_flag', stop_flag)
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if output_dir:
        save_hyperlinks_as_pdf(output_dir, driver, iltis_url_entry, checkbuttons, 
                               stop_flag, stop_button, update_label, print_status_label, 
                               print_error_status_label, root)
        if not stop_flag:
            update_label(print_status_label, "Finished printing", "green")
            messagebox.showinfo("Success", "Selected hyperlinks have been saved as PDFs.")

def stop_printing(stop_flag, update_label, print_status_label):
    stop_flag = True
    update_config(config_file, 'stop_flag', stop_flag)
    update_label(print_status_label, "Stopping after this print", "blue")

def setup_gui(root, driver, config):
    global login_url_entry, username_entry, password_entry, iltis_url_entry, filter_string_entry
    global login_status_label, access_status_label, hyperlinks_status_label
    global select_all_cb, sort_cb, print_button, stop_button, print_status_label, print_error_status_label
    global var_all, sort_var, links_canvas, links_inner_frame, checkbuttons
    global stop_flag, logged_flag, default_filter_string, original_iltis_url

    stop_flag = config['stop_flag']
    logged_flag =  config['logged_flag']
    original_iltis_url =  config['original_iltis_url']
    default_moodle_url = config['default_moodle_url']
    default_username = config['default_username']
    default_iltis_url = config['default_iltis_url']
    default_filter_string = config['default_filter_string']

    tk.Label(root, text="Moodle Login URL:", anchor='w').grid(row=0, column=0, padx=10, pady=5, sticky='w')
    login_url_entry = tk.Entry(root, width=60)
    login_url_entry.insert(0, default_moodle_url)
    login_url_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=3, sticky='w')

    tk.Label(root, text="Username:", anchor='e').grid(row=1, column=0, padx=10, pady=5, sticky='e')
    username_entry = tk.Entry(root, width=20)
    username_entry.insert(0, default_username)
    username_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    tk.Label(root, text="Password:", anchor='e').grid(row=1, column=2, padx=10, pady=5, sticky='e')
    password_entry = tk.Entry(root, show='*', width=20)
    password_entry.grid(row=1, column=3, padx=10, pady=5, sticky='w')

    tk.Label(root, text="Iltis redirect URL:", anchor='w').grid(row=2, column=0, padx=10, pady=5, sticky='w')
    iltis_url_entry = tk.Entry(root, width=60)
    iltis_url_entry.insert(0, default_iltis_url)
    iltis_url_entry.grid(row=2, column=1, padx=10, pady=5, columnspan=3, sticky='w')

    tk.Label(root, text="Filter String:", anchor='e').grid(row=3, column=0, padx=10, pady=5, sticky='e')
    filter_string_entry = tk.Entry(root, width=60)
    filter_string_entry.insert(0, default_filter_string)
    filter_string_entry.grid(row=3, column=1, padx=10, pady=5, columnspan=3, sticky='w')

    fetch_button = tk.Button(root, text="Fetch Hyperlinks", 
        command=lambda: threading.Thread(target=fetch_hyperlinks, 
                args=(driver, config['logged_flag'], config['original_iltis_url'], login_url_entry, username_entry, password_entry, 
                    iltis_url_entry, filter_string_entry, login_status_label, 
                    access_status_label, hyperlinks_status_label, select_all_cb, 
                    sort_cb, print_button, print_status_label, stop_button, 
                    update_label, refresh_hyperlinks, 
                    links_inner_frame, checkbuttons, var_all, sort_var, 
                    create_tooltip, truncate
                )
            ).start()
        )
    fetch_button.grid(row=4, column=0, padx=10, pady=5, sticky='w')

    status_frame = tk.Frame(root)
    status_frame.grid(row=4, column=1, columnspan=3, sticky='w')
    login_status_label = tk.Label(status_frame, text="", wraplength=400, anchor='w')
    login_status_label.pack(side='left', padx=10)
    access_status_label = tk.Label(status_frame, text="", wraplength=400, anchor='w')
    access_status_label.pack(side='left', padx=10)
    hyperlinks_status_label = tk.Label(status_frame, text="", wraplength=400, anchor='w')
    hyperlinks_status_label.pack(side='left', padx=10)

    select_all_frame = tk.Frame(root)
    select_all_frame.grid(row=5, column=0, padx=10, pady=5, sticky='w')
    var_all = tk.BooleanVar()
    select_all_cb = tk.Checkbutton(select_all_frame, text="Select All", variable=var_all, 
        command=lambda: select_all(checkbuttons, var_all))

    sort_frame = tk.Frame(root)
    sort_frame.grid(row=5, column=1, padx=10, pady=5, sticky='w')
    sort_var = tk.BooleanVar(value=True)  
    sort_cb = tk.Checkbutton(sort_frame, text="Sort Ascending", variable=sort_var, 
        command=lambda: on_sort_toggle(checkbuttons, refresh_hyperlinks, 
                                       links_inner_frame, var_all, sort_var, 
                                       create_tooltip, truncate
                        )
        )

    links_frame = tk.Frame(root)
    links_frame.grid(row=6, column=0, columnspan=5, padx=10, pady=5, sticky='nsew')

    links_canvas = tk.Canvas(links_frame, borderwidth=0, highlightthickness=0)
    scrollbar = tk.Scrollbar(links_frame, orient="vertical", command=links_canvas.yview)
    links_inner_frame = tk.Frame(links_canvas)

    links_inner_frame.bind(
        "<Configure>",
        lambda e: links_canvas.configure(
            scrollregion=links_canvas.bbox("all")
        )
    )

    links_canvas.create_window((0, 0), window=links_inner_frame, anchor="nw")
    links_canvas.configure(yscrollcommand=scrollbar.set)

    links_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    links_canvas.bind_all("<MouseWheel>", lambda event: _on_mouse_wheel(event, links_canvas))

    root.grid_rowconfigure(6, weight=1) 
    root.grid_columnconfigure(1, weight=1) 

    print_button = tk.Button(root, text="Print to PDF", 
        command=lambda: threading.Thread(target=save_selected_hyperlinks, 
                args=(driver, iltis_url_entry, checkbuttons, config['stop_flag'], 
                      update_label, print_status_label, print_error_status_label, root
            )).start()
        )
    print_status_label = tk.Label(root, text="", wraplength=200, anchor='w')
    stop_button = tk.Button(root, text="Stop Print", 
        command=lambda: stop_printing(config['stop_flag'], update_label, print_status_label))
    print_error_status_label = tk.Label(root, text="", wraplength=200, anchor='w')

    checkbuttons = []

