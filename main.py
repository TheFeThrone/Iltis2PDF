import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gui import setup_gui
from utils.helpers import load_config, update_config

def reset():
    update_config("config.json", 'original_iltis_url', "")
    update_config("config.json", 'logged_flag', False)
    update_config("config.json", 'stop_flag', False)

def on_close(driver,root):
    reset()
    driver.quit()
    root.destroy()
    print("Application closed successfully.")

def main():
    config = load_config("config.json")
    reset()
    root = tk.Tk()
    root.title("Iltis2PDF")

    # Initialize the WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)

    setup_gui(root, driver, config)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(driver,root))
    root.mainloop()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_close(driver)

if __name__ == "__main__":
    main()
