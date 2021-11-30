from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob


def waitElement(driver, element, by=By.ID):
    return WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((by, element))
    )


def waitElementDisable(driver, element, by=By.ID):
    return WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((by, element))
    )


def waitDownload(path):
    if not os.path.exists(path):
        os.makedirs(path)

    tempfiles = 0
    while tempfiles == 0:
        time.sleep(1)
        for fname in os.listdir(path):
            if "crdownload" in fname or "tmp" in fname:
                tempfiles = 0
                break
            else:
                tempfiles = 1


def deleteTemporals(path):
    if not os.path.exists(path):
        return
    for fname in os.listdir(path):
        os.remove(os.path.join(path, fname))


def getMostRecentFile(path, _filter=None):
    list_of_files = glob.glob(fr'{path}/*')
    list_of_files = _filter(
        list_of_files) if _filter is not None else list_of_files
    return max(list_of_files, key=os.path.getctime)

def numToMonth(num):
    return {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4:  "Abril",
        5: "Mayo",
        6: "Junio",
        7:"Julio",
        8:"Agosto",
        9:"Septiembre",
        10:"Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }[num]