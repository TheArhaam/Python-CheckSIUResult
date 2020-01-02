import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import threading
import time

url = "https://www.examination.siu.edu.in/examination/exam_results.php"
resulturl = "https://www.examination.siu.edu.in/examination/result.html"
myBatch = '2018-20'
myBranch = 'B.TECH.(IT)'
myInstitute = 'SIT'
myPRN = '17070124502'
mySeatNo1 = ''
mySeatNo2 = ''
rowSampleRange = 15
possibleResult = False
result = False

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(
    executable_path='C:/Users/thear/PythonProjects/chromedriver.exe',
    chrome_options=options)
count = 0
while(result!=True):
    driver.get(url)
    print('\nCHECK -',count)
    tabledata = driver.find_element_by_css_selector(
        '#campus > div > div > div > table')

    tablerows = tabledata.find_elements_by_tag_name('tr')
    maxrows = len(tablerows)

    for i in range(len(tablerows)):
        row = tablerows[i].text
        temp = row.split()
        if (temp[1] == myInstitute):
            iindex = i + 1
            break

    i = iindex

    while (i < (iindex + rowSampleRange) and i < maxrows and result == False):
        #SPECIFIC SEARCH
        branch = tablerows[i].text.split()[0]
        if myBatch in tablerows[i].text:
            possibleResult = True
        batches = tablerows[i].text.split()[1].split(',')
        for batch in batches:
            if (batch == myBatch and branch == myBranch):
                result = True
                break
            elif (batch == myBatch):
                possibleResult = True

        i = i + 1

    if (possibleResult):
        print("=====RESULT MAY BE OUT=====")
    else:
        print('Result may not be out')

    if (result):
        print("====================RESULT IS OUT====================")
    else:
        print('Result is not out')
    
    print('CHECKED')
    count = count + 1

    if (possibleResult or result):
        driverOpen = webdriver.Chrome(
            executable_path='C:/Users/thear/PythonProjects/chromedriver.exe')
        driverOpen.get(resulturl)

        prnInput = driverOpen.find_element_by_class_name('form-control')
        prnInput.send_keys(myPRN)

        loginButton = driverOpen.find_element_by_css_selector('#form1 > div > div:nth-child(4) > div > div > div > input')
        loginButton.click()
        break
    time.sleep(900)
