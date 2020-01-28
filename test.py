import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import threading
import time
import tkinter
from tkinter import *

# ====================== TO DO LIST ====================== 
# Add GUI to make it more usable to general SIU Students

# def getResult(driver2,seatno):
#     driver2.get(resulturl)
#     #IMPORTANT TO SWITCH TO THE FRAME
#     driver2.switch_to_frame(
#         driver.find_element_by_css_selector('body > iframe'))

#     prnInput = driver2.find_element_by_css_selector('#login')
#     prnInput.send_keys(myPRN)

#     loginButton = driver2.find_element_by_css_selector(
#         '#form1 > div > div:nth-child(4) > div > div > div > input')
#     loginButton.click()

#     seatInput = driver2.find_element_by_css_selector('#login')
#     seatInput.send_keys(seatno)
#     nextButton = driver2.find_element_by_css_selector('#form1 > div > div:nth-child(4) > div > div > div > input')
#     nextButton.click()


url = "https://www.examination.siu.edu.in/examination/exam_results.php"
resulturl = "https://www.examination.siu.edu.in/examination/result.html"

# GET EXACT VALUES FROM THE WEBSITE
myBatch = '2016-20'
myProgramme = 'B.TECH'
myBranch = 'B.TECH.(IT)'
myInstitute = 'SIT'
myPRN = '17070124501'
mySeatNos = ['501551','439016']
rowSampleRange = 15
delay = 900  #in seconds

#For keeping the browser out of view
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(
    executable_path='C:/Users/thear/PythonProjects/chromedriver.exe',
    chrome_options=options)

def beginResultCheck():
    possibleResult = False
    result = False
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
                iindex = i #+ 1
                break

        i = iindex

        #Searching for myBatch
        while (i < (iindex + rowSampleRange) and i < maxrows and result == False):
            # print(tablerows[i].text)
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
            n = len(mySeatNos)
            driversList = [webdriver.Chrome(executable_path='C:/Users/thear/PythonProjects/chromedriver.exe') for i in range(n)]
            # driver2 = webdriver.Chrome(
            #     executable_path='C:/Users/thear/PythonProjects/chromedriver.exe')
            # driver2.get(resulturl)

            for i in range(n):
                driversList[i].get(resulturl)
                #IMPORTANT TO SWITCH TO THE FRAME
                driversList[i].switch_to_frame(
                    driversList[i].find_element_by_css_selector('body > iframe'))

                prnInput = driversList[i].find_element_by_css_selector('#login')
                prnInput.send_keys(myPRN)

                loginButton = driversList[i].find_element_by_css_selector(
                    '#form1 > div > div:nth-child(4) > div > div > div > input')
                loginButton.click()

                seatInput = driversList[i].find_element_by_css_selector('#login')
                seatInput.send_keys(mySeatNos[i])
                nextButton = driversList[i].find_element_by_css_selector('#form1 > div > div:nth-child(4) > div > div > div > input')
                nextButton.click()

                if (result):
                    driver.close()
                    break     
        time.sleep(delay)


#================================ UI ================================
#root represents the main window
root = tkinter.Tk()
root.title('SIU Result')

# FONTS
labelfont = ('','15')
entryfont = ('','12')

# LABELS
instituteLabel = Label(root,text='Institute: ')
instituteLabel.config(font=labelfont)
programmeLabel = Label(root,text='Programme: ')
programmeLabel.config(font=labelfont)
branchLabel = Label(root,text='Branch: ')
branchLabel.config(font=labelfont)
prnLabel = Label(root,text='PRN: ')
prnLabel.config(font=labelfont)
seatNumLabel = Label(root,text='Seat Numbers: ')
seatNumLabel.config(font=labelfont)
delayLabel = Label(root,text='Delay in seconds:')
delayLabel.config(font=labelfont)

# ENTRY
instituteEntry = Entry(root,width=50)
instituteEntry.config(font=entryfont)
programmeEntry = Entry(root,width=50)
programmeEntry.config(font=entryfont)
branchEntry = Entry(root,width=50)
branchEntry.config(font=entryfont)
prnEntry = Entry(root,width=50)
prnEntry.config(font=entryfont)
seatNumEntry = Entry(root,width=50)
seatNumEntry.config(font=entryfont,justify=LEFT)
delayEntry = Entry(root,width=50)
delayEntry.config(font=entryfont,justify=LEFT)

# GRID LAYOUT
instituteLabel.grid(row=0,column=0,sticky=W,padx=5,pady=5); instituteEntry.grid(row=0,column=1,sticky=W,padx=5,pady=5)
programmeLabel.grid(row=1,column=0,sticky=W,padx=5,pady=5); programmeEntry.grid(row=1,column=1,sticky=W,padx=5,pady=5)
branchLabel.grid(row=2,column=0,sticky=W,padx=5,pady=5);    branchEntry.grid(row=2,column=1,sticky=W,padx=5,pady=5)
prnLabel.grid(row=3,column=0,sticky=W,padx=5,pady=5);       prnEntry.grid(row=3,column=1,sticky=W,padx=5,pady=5)
seatNumLabel.grid(row=4,column=0,sticky=W,padx=5,pady=5);   seatNumEntry.grid(row=4,column=1,sticky=W,padx=5,pady=5)
delayLabel.grid(row=5,column=0,sticky=W,padx=5,pady=5);     delayEntry.grid(row=5,column=1,sticky=W,padx=5,pady=5)

#POSITIONING
# Apparently a common hack to get the window size. Temporarily hide the
# window to avoid update_idletasks() drawing the window in the wrong
# position.
root.withdraw()
root.update_idletasks()  # Update "requested size" from geometry manager
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
# This seems to draw the window frame immediately, so only call deiconify()
# after setting correct window position
root.deiconify()

#this actually launches the UI
root.mainloop()