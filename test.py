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

def setProgrammeList():
    global instituteStrVar
    print(instituteStrVar.get())
    institute = instituteStrVar.get()
    temp = ['']
    if (institute=='SLS-Nagpur'):
        temp = ['BA LLB','BBA LLB','LLM']
    elif (institute=='SLS-P'):
        temp = ['LLM','BA LLB','BBA LLB','BA LLB (HONS)','BBA LLB (HONS)',\
                'LLB','DTL','DIPL','DAC and ADRS','DIBL and CLI','DCL']
    elif (institute=='SLS-N'):
        temp = ['BA LLB','BBA LLB','LLM']
    elif (institute=='SLS-H'):
        temp = ['BA LLB','BBA LLB']
    elif (institute=='SIBM-P'):
        temp = ['MBA','MBA (EXE)','MBA (I & E)','PGDMM','PGDFM',\
                'PGDICE','DBM','PGDSCOM']
    elif (institute=='SIIB'):
        temp = ['MBA (IB)','MBA (AB)','MBA (EE)']
    elif (institute=='SCMHRD'):
        temp = ['MBA','MBA (IM)','MBA (EXE)','PGDBA','PGDHRM',\
                'MBA (ID&M)','MBA (BA)']
    elif (institute=='SIMS'):
        temp = ['MBA','MBA (EXE)','EXECUTIVE PGDM','PGDBM','PGDFM',\
                'PGDHRM','PGDBA']
    elif (institute=='SIDTM'):
        temp = ['MBA (DTM)','MBA (EXE) (TM)']
    elif (institute=='SCMS-P'):
        temp = ['BBA']
    elif (institute=='SIOM'):
        temp = ['MBA(OM)','PGDOM']
    elif (institute=='SIBM-B'):
        temp = ['MBA','MBA (EXE)','PGDMM','PGDBA']
    elif (institute=='SSBF'):
        temp = ['MBA (B&F)']
    elif (institute=='SIBM-H'):
        temp = ['MBA']
    elif (institute=='SICSR'):
        temp = ['MBA (IT)','M.SC.(CA)','BCA','BBA (IT)','M.Sc (SS)']
    elif (institute=='SCIT'):
        temp = ['MBA (ITBM)','MBA (EXE) (IT)','MBA (DS & DA)']
    elif (institute=='SIHS'):
        temp = ['MBA(HHM)','B.Sc.(MT)','M.Sc.(MT)','PGDEMS','DBI',\
                'B. Sc (RT)','MPH']
    elif (institute=='SSBS'):
        temp = ['M.Sc.(ND)','M.Sc.(BT)']
    elif (institute=='SIMC-P'):
        temp = ['MBA(CM)','MA (MC)']
    elif (institute=='SID'):
        temp = ['B.Des.']
    elif (institute=='SCMC'):
        temp = ['BA (MC)','BMS']
    elif (institute=='SSP'):
        temp = ['BA (VA & P)']
    elif (institute=='SSE'):
        temp = ['M.Sc.(Eco)','B.SC. (ECO) (HONOURS)']
    elif (institute=='SSLA'):
        temp = ['B.Sc/BA (Liberal Arts)']
    elif (institute=='SIT'):
        temp = ['B.TECH','B.TECH.(CE)','B.TECH.(CS&E)','B.TECH.(E&TCE)','M.Tech (G & ST)',\
                'B.TECH.(IT)','B.TECH.(ME)','M.Tech (CAD&M)','M.Tech (E&TCE)','M.Tech (CS&E)']
    elif (institute=='SIG'):
        temp = ['M.SC.(GEO)','M.Sc. (DS & SA)']
    elif (institute=='SSMC-B'):
        temp = ['MBA (CM)']
    elif (institute=='SSCA'):
        temp = ['B.SC. (Culinary Arts)','DB&PS']
    elif (institute=='SSSS'):
        temp = ['MBA (SM)']
    elif (institute=='SSIS'):
        temp = ['MA (IS)']
    elif (institute=='SSI'):
        temp = ['M.SC.(AS)']
    elif (institute=='SIBM -Nagpur'):
        temp = ['MBA']
    elif (institute=='SCMS-Noida'):
        temp = ['BBA']
    elif (institute=='SSPAD'):
        temp = ['B.Des']
    elif (institute=='SCMS-Nagpur'):
        temp = ['BBA']
    global programmeList
    global programmeStrVar
    programmeList = temp
    # programmeStrVar.set(next(iter(programmeList)))
    programmeStrVar.set(programmeList[0])
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

# LISTS
#region
instituteList = ['SLS-Nagpur','SLS-P','SLS-N','SLS-H','SIBM-P',\
                'SIIB','SCMHRD','SIMS','SIDTM','SCMS-P',\
                'SIOM','SIBM-B','SSBF','SIBM-H','SICSR',\
                'SCIT','SIHS','SSBS','SIMC-P','SID',\
                'SCMC','SSP','SSE','SSLA','SIT',\
                'SIG','SSMC-B','SSCA','SSSS','SSIS',\
                'SSI','SIBM -Nagpur','SCMS-Noida','SSPAD','SCMS-Nagpur']
programmeList = ['BA LLB','BBA LLB','LLM']
branchList = {}
#endregion

# STRINGVAR
#region
programmeStrVar = StringVar(root)
instituteStrVar = StringVar(root)
branchStrVar = StringVar(root)
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
#region
instituteOption = OptionMenu(root,instituteStrVar,*instituteList)
instituteOption.config(font=optionfont)
programmeOption = OptionMenu(root,programmeStrVar,*programmeList)
programmeOption.config(font=optionfont)
#endregion


# TRACE AND SET
#region
# programmeStrVar.set(next(iter(programmeList)))
instituteStrVar.trace("w",setProgrammeList())
instituteStrVar.set(instituteList[0])
#endregion


# BUTTONS
#region
submitButton = Button(root,text='SUBMIT',command=submitClick,padx=10,pady=5)
#endregion

# GRID LAYOUT
#region
# instituteLabel.grid(row=0,column=0,sticky=W,padx=5,pady=5); instituteEntry.grid(row=0,column=1,sticky=W,padx=5,pady=5)
instituteLabel.grid(row=0,column=0,sticky=W,padx=5,pady=5); instituteOption.grid(row=0,column=1,sticky=W,padx=5,pady=5)
# programmeLabel.grid(row=1,column=0,sticky=W,padx=5,pady=5); programmeEntry.grid(row=1,column=1,sticky=W,padx=5,pady=5)
programmeLabel.grid(row=1,column=0,sticky=W,padx=5,pady=5); programmeOption.grid(row=1,column=1,sticky=W,padx=5,pady=5)
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