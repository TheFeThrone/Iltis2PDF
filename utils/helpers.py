from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import json

def _on_mouse_wheel(event, links_canvas):
    links_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def truncate(text, length):
    text = text.replace("https://", "")
    overflow = len(text) - length - 3
    if overflow <= 0:
        return text
    else:
        return text[:-overflow] + '...'

def wait_for_page_load(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def wait_for_loading_indicator(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "iltis-fullscreen-loading-indicator"))
        )
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "iltis-fullscreen-loading-indicator"))
        )
    except Exception as e:
        logging.warning(f"Loading indicator not found or disappeared")

def update_label(label, text, color):
    label.config(text=text, foreground=color)
    label.master.update_idletasks()


def load_config(file_path):
    """Load the JSON configuration file."""
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config

def save_config(file_path, config):
    """Save the JSON configuration file."""
    with open(file_path, 'w') as f:
        json.dump(config, f, indent=4)

def update_config(file_path, key, value):
    """Update a value in the JSON configuration file."""
    config = load_config(file_path)
    config[key] = value
    save_config(file_path, config)