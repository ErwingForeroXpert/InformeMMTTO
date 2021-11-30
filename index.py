from logging import exception
import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utils import waitDownload, waitElement, waitElementDisable, deleteTemporals
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

if __name__ == "__main__":

    chrome_driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chromeOptions)
    try:
        deleteTemporals(files_route)

        # ejecutar macro
        parent_folder = os.path.join(os.getcwd(), "Documents")
        book_mmto = None
        for fname in os.listdir(parent_folder):
            if "xlsm" in fname and "~" not in fname:
                book_mmto = xw.Book(os.path.join(parent_folder, fname))
                break

        if book_mmto is None:
            raise Exception(f"El libro no se encuentra o no se puede abrir")

        _dates = book_mmto.macro('Módulo1.PreProcesarDatos')()
        book_mmto.save()
        book_mmto.close()
        
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

        for fecha in fechas:

            waitElement(chrome_driver, "FECHA_CREACION")
            init_date_element = chrome_driver.find_element_by_id(
                "FECHA_CREACION")
            end_data_element = chrome_driver.find_element_by_id(
                "FECHA_CREACIONFIN_GENERADO")

            init_day, end_day = calendar.monthrange(
                int(fecha[0]), int(fecha[0]))
            init_date_element.send_keys(fr"{fecha[0]}/{fecha[1]}/{init_day}")
            end_data_element.send_keys(fr"{fecha[0]}/{fecha[1]}/{end_day}")

            # descargar el reporte
            chrome_driver.find_element_by_id("exportButton").click()

            time.sleep(1)
            waitElementDisable(chrome_driver, "ETAPA-list")
            waitDownload(files_route)

        print("\n Proceso Terminado, ya puede cerrar la ventana \n")
    except ValueError as e:
        raise exception(e)
    finally:
        chrome_driver.close()
