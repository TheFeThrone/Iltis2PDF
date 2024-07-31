
import logging
import base64
import os
from utils.helpers import wait_for_page_load, wait_for_loading_indicator, load_config

def save_page_as_pdf(driver, link, output_path):
    driver.get(link)
    
    # Wait for the page content to load and loading indicator to disappear
    wait_for_page_load(driver)
    wait_for_loading_indicator(driver)

    # Use Chrome DevTools Protocol to print the page to PDF
    result = driver.execute_cdp_cmd("Page.printToPDF", {
        "landscape": False,
        "printBackground": True,
        "preferCSSPageSize": False,
        "paperWidth": 8.3,
        "paperHeight": 11.7
    })

    # Decode the base64 PDF and save to a file
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(result['data']))
    logging.info(f"Saved {link} as PDF at {output_path}")

def save_hyperlinks_as_pdf(output_dir, driver, iltis_url_entry, checkbuttons, stop_flag, stop_button, update_label, print_status_label, print_error_status_label, root):
    iltis_url = iltis_url_entry.get()
    stop_button.grid(row=7, column=2, padx=10, pady=5, sticky='w')
    for cb, var in checkbuttons:
        if var.get():  # Check if the checkbox is selected
            if load_config("config.json")['stop_flag']:
                update_label(print_status_label, "Stopped printing", "red")
                logging.info("Printing stopped by user.")
                return
            original_link = var.link
            update_label(print_status_label, "Printing", "blue")
            try:
                cb.config(foreground='blue')  # Set link color to blue while processing
                root.update_idletasks()

                # Replace '/' with '_' to create a valid file name
                relative_path = original_link.replace(iltis_url, "").strip("/")
                relative_path = relative_path.replace("/", "_")
                relative_path = relative_path.replace("#", "Kapitel-")
                relative_path = relative_path.replace("00-Tutorial_", "Thema-")
                output_path = os.path.join(output_dir, relative_path)
                
                # Append .pdf extension to the file name
                if not output_path.endswith(".pdf"):
                    output_path += ".pdf"
                
                save_page_as_pdf(driver, original_link, output_path)
                cb.config(foreground='green')  # Set link color to green on success
            except Exception as e:
                logging.error(f"Error saving {original_link} as PDF: {e}")
                cb.config(foreground='red')  # Set link color to red on failure
                update_label(print_error_status_label, "Error saving as PDF", "red")