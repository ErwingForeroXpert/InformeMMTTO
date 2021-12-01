from logging import exception
import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utils import waitDownload, waitElement, waitElementDisable, deleteTemporals, \
numToMonth, getIntervalDates,getMostRecentFile, getRangeMonth
from selenium.webdriver.common.by import By
from dotenv import dotenv_values
import xlwings as xw
import time
import calendar
import os


config = dotenv_values(".env")
date_init = "2021/10/10"  # test
date_end = "2021/11/09"
files_route = fr"{os.getcwd()}\files"

# insertar la direccion de descarga
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": files_route}
chromeOptions.add_experimental_option("prefs", prefs)

def RunMacro(nameMacro, _args=None):
    # ejecutar macro
    result = None
    parent_folder = os.path.join(os.getcwd(), "Documents")
    book_mmto = None
    for fname in os.listdir(parent_folder):
        if "xlsm" in fname and "~" not in fname:
            book_mmto = xw.Book(os.path.join(parent_folder, fname))
            break

    if book_mmto is None:
        raise Exception(f"El libro no se encuentra o no se puede abrir")
    
    result = book_mmto.macro(nameMacro)(*_args) if _args is not None else book_mmto.macro(nameMacro)()
    
    book_mmto.save()

    if len(book_mmto.app.books) == 1:
        book_mmto.app.quit()
    else:
        book_mmto.close()

    return result

if __name__ == "__main__":

    chrome_driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chromeOptions)
    try:
        deleteTemporals(files_route)
        
        _dates = RunMacro('Módulo1.PreProcesarDatos')
        
        chrome_driver.get(config["SIGMA_URL"])

        user_element = chrome_driver.find_element_by_id("user")
        user_element.send_keys(config["SIGMA_USERNAME"])

        pass_element = chrome_driver.find_element_by_id("password")
        pass_element.send_keys(config["SIGMA_PASSWORD"])

        pass_element.send_keys(Keys.ENTER)

        # Esperar el Home
        waitElement(chrome_driver, "menu")

        # seleccionar consultas rapidas
        report_element = chrome_driver.find_element_by_xpath(
            "//ul[@id='menu']/li[3]")
        report_element.click()
        time.sleep(1)
        report_element.find_element_by_xpath(".//li[2]").click()

        waitElement(
            chrome_driver,
            "//tr/td[@role='gridcell'and contains(text(),'53')]",
            By.XPATH)

        chrome_driver.find_element_by_xpath(
            "//tr/td[@role='gridcell'and contains(text(),'53')]").click()
        chrome_driver.find_element_by_xpath(
            "//div/a[contains(text(),'Consultar')]").click()

        temp_dates = getIntervalDates(_dates) if (_dates is not None or None in _dates)  else []

        if _dates is not None:
            for _date in temp_dates:
                waitElement(chrome_driver, "FECHA_CREACION")
                init_date_element = chrome_driver.find_element_by_id(
                    "FECHA_CREACION")
                end_data_element = chrome_driver.find_element_by_id(
                    "FECHA_CREACIONFIN_GENERADO")

                init_day, end_day = getRangeMonth(
                    _date[0], _date[1])

                init_date_element.clear()
                end_data_element.clear()
                init_date_element.send_keys(fr"{_date[0]}/{_date[1]}/{init_day}")
                end_data_element.send_keys(fr"{_date[0]}/{_date[1]}/{end_day}")

                # descargar el reporte
                chrome_driver.find_element_by_id("exportButton").click()

                time.sleep(1)
                waitElementDisable(chrome_driver, "ETAPA-list")
                waitDownload(files_route)

                actual_file = getMostRecentFile(files_route, lambda x: "xls" in x)
                RunMacro('Módulo1.CargarDatosArchivo', [actual_file, str(_date[0]), str(numToMonth(_date[1]))])
        else:
            print("\n No se encontraron fechas para procesar \n")
            
        print("\n Proceso Terminado, ya puede cerrar la ventana \n")

    except ValueError as e:
        raise exception(e)
    finally:
        chrome_driver.close()
