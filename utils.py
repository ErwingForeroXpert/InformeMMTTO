from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime
import calendar
import time
import os
import glob


def waitElement(driver, element, by=By.ID, exist=False):
    """wait for the element appear on the Screen

    Args:
        driver (WebDriver): web driver see https://www.selenium.dev/documentation/webdriver/
        element (Object<Any>): element see https://selenium-python.readthedocs.io/locating-elements.html
        by (String, optional): Searcher. Defaults to By.ID.
        exist (bool, optional): if element already existed. Defaults to False.

    Returns:
        WebDriverWait: Constructor, takes a WebDriver instance and timeout in seconds.
    """

    return WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element(by,element) if exist else EC.visibility_of_element_located((by, element))
    )


def waitElementDisable(driver, element, by=By.ID):
    """wait for the element disappear of the screen

    Args:
        driver (WebDriver): web driver see https://www.selenium.dev/documentation/webdriver/
        element (Object<Any>): element see https://selenium-python.readthedocs.io/locating-elements.html
        by (String, optional): Searcher. Defaults to By.ID.

    Returns:
        WebDriverWait: Constructor, takes a WebDriver instance and timeout in seconds.
    """
    return WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((by, element))
    )

def waitElementClickable(driver, element, by=By.ID):
    """wait for element to be clickable

    Args:
        driver (WebDriver): web driver see https://www.selenium.dev/documentation/webdriver/
        element (Object<Any>): element see https://selenium-python.readthedocs.io/locating-elements.html
        by (String, optional): Searcher. Defaults to By.ID.

    Returns:
        WebDriverWait: Constructor, takes a WebDriver instance and timeout in seconds.
    """

    return WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((by, element))
    )

def waitDownload(path):
    """wait that elements in state downloading disappear

    Args:
        path (String): Folder of downloads
    """
    tempfiles = 0
    while tempfiles == 0:
        time.sleep(1)
        for fname in os.listdir(path):
            if "crdownload" in fname or "tmp" in fname:
                tempfiles = 0
                break
            else:
                tempfiles = 1

def createNecesaryFolders(path, folders):
    """Create folders

    Args:
        path (String): Folder parents
        folders (String): Folder childrens
    """
    for folder in folders:
        if not os.path.exists(os.path.join(path, folder)):
            os.makedirs(os.path.join(path, folder))
            
def deleteTemporals(path):
    """Delete elements of path

    Args:
        path (String): Folder parent
    """
    if not os.path.exists(path):
        return
    for fname in os.listdir(path):
        os.remove(os.path.join(path, fname))


def getMostRecentFile(path, _filter=None):
    """Get most recent file for date

    Args:
        path (String): Folder parent
        _filter (function, optional): filter name of documents. Defaults to None.

    Returns:
        String: path of file most recent
    """
    list_of_files = glob.glob(fr'{path}/*')
    list_of_files = filter(_filter, list_of_files) if _filter is not None else list_of_files
    return max(list_of_files, key=os.path.getctime)

def getIntervalDates(_dates):
    """Get Interval of dates

    Args:
        _dates (tuple): tuple of interval dates, maxlen 2

    Returns:
        list: list of interval months
    
    Example:
        getIntervalDates((
            (11,2021), (01,2022)
            ))
        returns:
            [[11,2021], [12,2021], [01,2022]]
    """
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
    """get interval of months into two dates

    Args:
        d1 (list): min date of interval
        d2 (list): max date of interval

    Returns:
        list: list with months, [[month, year],...]
    """
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
    """Get first and last day of month

    Args:
        year (int): year
        month (int): month
        init (int, optional): first day of month. Defaults to 1.

    Returns:
        tuple: first day, last day
    """
    return "{:02d}".format(init), "{:02d}".format(calendar.monthrange(year, month)[1])

def numToMonth(num):
    """Num to Spanish month 

    Args:
        num (int): num of month

    Returns:
        String: month
    """
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

