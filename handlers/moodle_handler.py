from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from utils.helpers import wait_for_page_load, update_config, load_config

config_file = "config.json"

def login_to_moodle(driver, login_url, username, password, logged_flag, update_label, login_status_label):

    logged_flag = load_config(config_file)['logged_flag']
    if not logged_flag:
        logging.info("Logging into Moodle...")
        update_label(login_status_label, "Logging into Moodle", "black")
        driver.get(login_url)

        # Wait for the login form to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginbtn")))

        # Find and fill the login form fields
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "loginbtn").click()
        
        # Wait for the dashboard to be present
        wait_for_page_load(driver)
        logged_flag = "Dashboard" in driver.page_source
        if logged_flag:
            update_label(login_status_label, "Logged in", "green")
            logged_flag = True
        else:
            update_label(login_status_label, "Login failed", "red")
            logged_flag = False
        logging.info(f"Logged in to Moodle: {logged_flag}")
        update_config(config_file, 'logged_flag', logged_flag)
        return logged_flag
    else:
        update_label(login_status_label, "Logged in", "green")
        logging.info("Already logged in to Moodle")
        return True

def first_iltis_access(driver, access_status_label, update_label):
    # Wait for the confirmation button to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn iltis-button') and contains(span, 'Verstanden')]")))

    # Handle the confirmation dialog
    try:
        confirm_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn iltis-button') and contains(span, 'Verstanden')]")
        confirm_button.click()
        
        # Wait for the page to load after confirmation
        wait_for_page_load(driver)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error confirming on Iltis: {e}")
        logging.error(f"Error confirming on Iltis: {e}")
        update_label(access_status_label, "Failed confirming on Iltis", "red")
        return False    

def access_iltis(driver, iltis_url, original_iltis_url, access_status_label, update_label):
    
    logging.info("Accessing Iltis...")
    update_label(access_status_label, "Accessing Iltis", "black")
    original_iltis_url = load_config(config_file)['original_iltis_url']
    if original_iltis_url=="":
        driver.get(iltis_url)
        original_iltis_url = iltis_url
        update_config(config_file, 'original_iltis_url', original_iltis_url)
        if not first_iltis_access(driver, access_status_label, update_label):
            return False
    else:
        driver.get(original_iltis_url)

    accessible = "Diese Instanz kann nur im Kontext einer Lernplattform" not in driver.page_source
    if accessible:
        update_label(access_status_label, "Accessed Iltis", "green")
    else:
        update_label(access_status_label, "Failed to access Iltis", "red")
    logging.info(f"Accessed Iltis: {accessible}")
    return accessible
