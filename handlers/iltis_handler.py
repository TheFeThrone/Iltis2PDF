from bs4 import BeautifulSoup
import tkinter as tk
import time
import logging
from .moodle_handler import login_to_moodle, access_iltis
from urllib.parse import urljoin
from utils.helpers import wait_for_page_load

def get_hyperlinks(driver, iltis_url, filter_string, update_label, hyperlinks_status_label):
    logging.info("Fetching hyperlinks...")
    update_label(hyperlinks_status_label, "Fetching hyperlinks...", "black")
    driver.get(iltis_url)
    
    time.sleep(5)  
    wait_for_page_load(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', href=True)
    hyperlinks = [urljoin(iltis_url, link['href']) for link in links if filter_string in link['href']]
    hyperlinks = list(set(hyperlinks))  

    logging.info(f"Found {len(hyperlinks)} hyperlinks that include '{filter_string}'.")
    return hyperlinks

def refresh_hyperlinks(hyperlinks, links_inner_frame, checkbuttons, var_all, sort_var, create_tooltip, truncate):
    for widget in links_inner_frame.winfo_children():
        widget.destroy()
    checkbuttons.clear()
    var_all.set(0)
    sort_ascending = sort_var.get()
    hyperlinks.sort(reverse=not sort_ascending)
    for link in hyperlinks:
        var = tk.BooleanVar()
        var.link = link  
        truncated_link = truncate(link, 72)  
        cb = tk.Checkbutton(links_inner_frame, text=truncated_link, variable=var)
        cb.pack(anchor='w')
        create_tooltip(cb, link)  
        checkbuttons.append((cb, var))

def fetch_hyperlinks(driver, logged_flag, original_iltis_url, login_url_entry, username_entry, password_entry, iltis_url_entry, filter_string_entry, login_status_label, access_status_label, hyperlinks_status_label, select_all_cb, sort_cb, print_button, print_status_label, stop_button, update_label, refresh_hyperlinks, links_inner_frame, checkbuttons, var_all, sort_var, create_tooltip, truncate):
    moodle_login_url = login_url_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    iltis_url = iltis_url_entry.get()
    filter_string = filter_string_entry.get()
    update_label(hyperlinks_status_label, "", "black")

    if login_to_moodle(driver, moodle_login_url, username, password, logged_flag, update_label, login_status_label):
        if access_iltis(driver, iltis_url, original_iltis_url, access_status_label, update_label):
            iltis_url_entry.delete(0, tk.END)
            iltis_url_entry.insert(0, driver.current_url[:-1])
            iltis_url = iltis_url_entry.get()
            hyperlinks = get_hyperlinks(driver, iltis_url, filter_string, update_label, hyperlinks_status_label)

            if hyperlinks:
                select_all_cb.pack(anchor='w')
                sort_cb.pack(anchor='w')
                refresh_hyperlinks(hyperlinks, links_inner_frame, checkbuttons, var_all, sort_var, create_tooltip, truncate)
                print_button.grid(row=7, column=0, padx=10, pady=5, sticky='w')
                print_status_label.grid(row=7, column=1, padx=10, pady=5, columnspan=1, sticky='w')

            else:
                select_all_cb.pack_forget()
                sort_cb.pack_forget()
                print_button.grid_forget()
                stop_button.grid_forget()
            update_label(hyperlinks_status_label, f"Found {len(hyperlinks)} hyperlinks", "green")
