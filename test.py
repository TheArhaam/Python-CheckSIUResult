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
# Implement a drop down menu to select the data instead of entering all of it
# Get data from website table instead of hardcoding it in


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

# FUNCTIONS
#region
def submitClick():
    updateValues()

def updateValues():
    global myInstitute
    myInstitute = instituteEntry.get()
    global myProgramme
    myProgramme = programmeEntry.get()
    global myBranch
    myBranch = branchEntry.get()
    global myBatch
    myBatch = batchEntry.get()
    global myPRN
    myPRN = prnEntry.get()
    global mySeatNos
    mySeatNos = seatNumEntry.get().split(',')
    global delay
    delay = int(delayEntry.get())
    printValues()

def printValues():
    print('myInstitute='+myInstitute)
    print('myProgramme='+myProgramme)
    print('myBranch='+myBranch)
    print('myBatch='+myBatch)
    print('myPRN='+myPRN)
    print('mySeatNos='+str(mySeatNos))
    print('delay='+str(delay))

def getProgrammeList(institute):
    temp = {}
    if (institute=='SLS-Nagpur'):
        temp = {'BA LLB','BBA LLB','LLM'}
    elif (institute=='SLS-P'):
        temp = {'LLM','BA LLB','BBA LLB','BA LLB (HONS)','BBA LLB (HONS)',\
                'LLB','DTL','DIPL','DAC and ADRS','DIBL and CLI','DCL'}
    elif (institute=='SLS-N'):
        temp = {'BA LLB','BBA LLB','LLM'}
    elif (institute=='SLS-H'):
        temp = {'BA LLB','BBA LLB'}
    elif (institute=='SIBM-P'):
        temp = {'MBA','MBA (EXE)','MBA (I & E)','PGDMM','PGDFM',\
                'PGDICE','DBM','PGDSCOM'}
    elif (institute=='SIIB'):
        temp = {'MBA (IB)','MBA (AB)','MBA (EE)'}
    elif (institute=='SCMHRD'):
        temp = {'MBA','MBA (IM)','MBA (EXE)','PGDBA','PGDHRM',\
                'MBA (ID&M)','MBA (BA)'}
    elif (institute=='SIMS'):
        temp = {'MBA','MBA (EXE)','EXECUTIVE PGDM','PGDBM','PGDFM',\
                'PGDHRM','PGDBA'}
    elif (institute=='SIDTM'):
        temp = {'MBA (DTM)','MBA (EXE) (TM)'}
    elif (institute=='SCMS-P'):
        temp = {'BBA'}
    elif (institute=='SIOM'):
        temp = {}
    elif (institute=='SIBM-B'):
        temp = {}
    elif (institute=='SSBF'):
        temp = {}
    elif (institute=='SIBM-H'):
        temp = {}
    elif (institute=='SICSR'):
        temp = {}
    elif (institute=='SCIT'):
        temp = {}
    elif (institute=='SIHS'):
        temp = {}
    elif (institute=='SSBS'):
        temp = {}
    elif (institute=='SIMC-P'):
        temp = {}
    elif (institute=='SID'):
        temp = {}
    elif (institute=='SCMC'):
        temp = {}
    elif (institute=='SSP'):
        temp = {}
    elif (institute=='SSE'):
        temp = {}
    elif (institute=='SSLA'):
        temp = {}
    elif (institute=='SIT'):
        temp = {}
    elif (institute=='SIG'):
        temp = {}
    elif (institute=='SSMC-B'):
        temp = {}
    elif (institute=='SSCA'):
        temp = {}
    elif (institute=='SSSS'):
        temp = {}
    elif (institute=='SSIS'):
        temp = {}
    elif (institute=='SSI'):
        temp = {}
    elif (institute=='SIBM -Nagpur'):
        temp = {}
    elif (institute=='SCMS-Noida'):
        temp = {}
    elif (institute=='SSPAD'):
        temp = {}
    elif (institute=='SCMS-Nagpur'):
        temp = {}
#endregion

# FONTS
#region
labelfont = ('','15')
entryfont = ('','12')
optionfont = ('','12')
#endregion

# LABELS
#region
instituteLabel = Label(root,text='Institute: ')
instituteLabel.config(font=labelfont)
programmeLabel = Label(root,text='Programme: ')
programmeLabel.config(font=labelfont)
branchLabel = Label(root,text='Branch: ')
branchLabel.config(font=labelfont)
batchLabel = Label(root,text='Batch: ')
batchLabel.config(font=labelfont)
prnLabel = Label(root,text='PRN: ')
prnLabel.config(font=labelfont)
seatNumLabel = Label(root,text='Seat Numbers: ')
seatNumLabel.config(font=labelfont)
delayLabel = Label(root,text='Delay in seconds:')
delayLabel.config(font=labelfont)
#endregion

# STRINGVAR
#region
instituteStrVar = StringVar(root)
instituteStrVar.set('SLS-Nagpur')
programmeStrVar = StringVar(root)
branchStrVar = StringVar(root)
#endregion

# LISTS
#region
instituteList = {'SLS-Nagpur','SLS-P','SLS-N','SLS-H','SIBM-P',\
                'SIIB','SCMHRD','SIMS','SIDTM','SCMS-P',\
                'SIOM','SIBM-B','SSBF','SIBM-H','SICSR',\
                'SCIT','SIHS','SSBS','SIMC-P','SID',\
                'SCMC','SSP','SSE','SSLA','SIT',\
                'SIG','SSMC-B','SSCA','SSSS','SSIS',\
                'SSI','SIBM -Nagpur','SCMS-Noida','SSPAD','SCMS-Nagpur'}
programmeList = {}
branchList = {}
#endregion

# ENTRY
#region
instituteEntry = Entry(root,width=50)
instituteEntry.config(font=entryfont)
programmeEntry = Entry(root,width=50)
programmeEntry.config(font=entryfont)
branchEntry = Entry(root,width=50)
branchEntry.config(font=entryfont)
batchEntry = Entry(root,width=50)
batchEntry.config(font=entryfont)
prnEntry = Entry(root,width=50)
prnEntry.config(font=entryfont)
seatNumEntry = Entry(root,width=50)
seatNumEntry.config(font=entryfont,justify=LEFT)
delayEntry = Entry(root,width=50)
delayEntry.config(font=entryfont,justify=LEFT)
#endregion

# OPTIONMENU
instituteOption = OptionMenu(root,instituteStrVar,*instituteList)
instituteOption.config(font=optionfont)

# BUTTONS
#region
submitButton = Button(root,text='SUBMIT',command=submitClick,padx=10,pady=5)
#endregion

# GRID LAYOUT
#region
# instituteLabel.grid(row=0,column=0,sticky=W,padx=5,pady=5); instituteEntry.grid(row=0,column=1,sticky=W,padx=5,pady=5)
instituteLabel.grid(row=0,column=0,sticky=W,padx=5,pady=5); instituteOption.grid(row=0,column=1,sticky=W,padx=5,pady=5)
programmeLabel.grid(row=1,column=0,sticky=W,padx=5,pady=5); programmeEntry.grid(row=1,column=1,sticky=W,padx=5,pady=5)
branchLabel.grid(row=2,column=0,sticky=W,padx=5,pady=5);    branchEntry.grid(row=2,column=1,sticky=W,padx=5,pady=5)
batchLabel.grid(row=3,column=0,sticky=W,padx=5,pady=5);    batchEntry.grid(row=3,column=1,sticky=W,padx=5,pady=5)
prnLabel.grid(row=4,column=0,sticky=W,padx=5,pady=5);       prnEntry.grid(row=4,column=1,sticky=W,padx=5,pady=5)
seatNumLabel.grid(row=5,column=0,sticky=W,padx=5,pady=5);   seatNumEntry.grid(row=5,column=1,sticky=W,padx=5,pady=5)
delayLabel.grid(row=6,column=0,sticky=W,padx=5,pady=5);     delayEntry.grid(row=6,column=1,sticky=W,padx=5,pady=5)
submitButton.grid(row=7,padx=5,pady=5)
#endregion

#POSITIONING
#region
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
#endregion

#this actually launches the UI
root.mainloop()