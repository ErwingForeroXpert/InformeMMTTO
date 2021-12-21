from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime
import calendar
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

def waitElementClickable(driver, element, by=By.ID):
    return WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((by, element))
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
    list_of_files = filter(_filter, list_of_files) if _filter is not None else list_of_files
    return max(list_of_files, key=os.path.getctime)

def getIntervalDates(_dates):

    if len(_dates) > 2:
        _dates = _dates[:2]

    conv_dates = []
    for temp_date in _dates:
        conv_dates.append(sorted([int(float(sub_num)) for sub_num in temp_date if ''.join(char for char in str(sub_num) if char.isdigit()) != ''])) #month, year

    conv_dates = sorted(conv_dates, key=lambda x: (date(x[1], x[0], 1) - date.today()).days) #order from smallest to largest

    end_date = conv_dates[-1] #lastest date
    if (date(end_date[1], end_date[0], 1) - date(datetime.today().year, datetime.today().month, 1)).days < 0: #if the lastest date is less than the current one
        if len(conv_dates) == 1:
            conv_dates.append([datetime.today().month, datetime.today().year])
        else:
            conv_dates[-1] = [datetime.today().month, datetime.today().year]
    
    interval_dates = intervalOfMonths(conv_dates[0], conv_dates[1]) if len(conv_dates) > 1 else conv_dates #get interval of months

    return interval_dates

def intervalOfMonths(d1, d2):
    init = d1[0]
    limit = 12 + d2[0] if d2[0] < d1[0] else d2[0]
    months = []
    while init <= limit:
        if init <= 12:
            months.append([init, d1[1]])
        else:
            months.append([init-12, d2[1]])
        init+=1
    return months

def getRangeMonth(year, month, init=1):
    return "{:02d}".format(init), "{:02d}".format(calendar.monthrange(year, month)[1])

def numToMonth(num):
    return {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4:  "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }[num]

