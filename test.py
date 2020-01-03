import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import threading
import time

url = "https://www.examination.siu.edu.in/examination/exam_results.php"
resulturl = "https://www.examination.siu.edu.in/examination/result.html"
myBatch = '2016-20'
myBranch = 'B.TECH.(IT)'
myInstitute = 'SIT'
myPRN = '12345678'
mySeatNo1 = ''
mySeatNo2 = ''
rowSampleRange = 15
possibleResult = False
result = False
delay = 900  #in seconds

#For keeping the browser out of view
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(
    executable_path='C:/Users/thear/PythonProjects/chromedriver.exe',
    chrome_options=options)

count = 0

#To repeat as long as result has not been declared
while (result != True):
    driver.get(url)
    print('\nCHECK -', count)

    #Getting the entire table of Result Declarations
    tabledata = driver.find_element_by_css_selector(
        '#campus > div > div > div > table')

    #Getting individual rows
    tablerows = tabledata.find_elements_by_tag_name('tr')
    maxrows = len(tablerows)

    #Finding index of myInstitute in tablerows
    for i in range(len(tablerows)):
        row = tablerows[i].text
        temp = row.split()
        if (temp[1] == myInstitute):
            iindex = i + 1
            break

    i = iindex

    #Searching for myBatch
    while (i < (iindex + rowSampleRange) and i < maxrows and result == False):
        #GENERAL SEARCH
        if myBatch in tablerows[i].text:
            possibleResult = True

        #SPECIFIC SEARCH
        if (myBranch in tablerows[i].text) and (myBatch in tablerows[i].text):
            result = True

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

    if (result or possibleResult):
        driver2 = webdriver.Chrome(
            executable_path='C:/Users/thear/PythonProjects/chromedriver.exe')
        driver2.get(resulturl)
        #IMPORTANT TO SWITCH TO THE FRAME
        driver2.switch_to_frame(
            driver2.find_element_by_css_selector('body > iframe'))

        prnInput = driver2.find_element_by_css_selector('#login')
        prnInput.send_keys(myPRN)

        loginButton = driver2.find_element_by_css_selector(
            '#form1 > div > div:nth-child(4) > div > div > div > input')
        loginButton.click()

        if (result):
            driver.close()
            break     
    time.sleep(delay)
