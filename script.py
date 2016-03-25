import time
import win32com.client
import sys
import os
import datetime
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from folder import Folder
from pair import Pair

LOG = open("log.txt", "r+")
ERRORS = open("errors.txt", "r+")
WAIT = 10

def createWebElementByName(name):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: driver.find_element_by_name(name)
			)
	except:
		printStatus(ERRORS, "Element: '" + name + "' is not visible")
		ERRORS.close()
		sys.exit()
	return element
def createWebElementByID(ID):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: driver.find_element_by_id(ID)
			)
	except:
		printStatus(ERRORS, "Element: '" + ID + "' is not visible")
		ERRORS.close()
		sys.exit()
	return element
def createWebElementByClassName(className):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: driver.find_element_by_class_name(className)
			)
	except:
		printStatus(ERRORS, "Element: '" + className + "' is not visible")
		ERRORS.close()
		sys.exit()
	return element
def createNestedWebElementByClassName(container, className):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: container.find_element_by_class_name(className)
			)
	except:
		printStatus(ERRORS, "Element: '" + className + "' is not visible")
		ERRORS.close()
		sys.exit()
	return element


def foundImage(descriptionFile, imagesFolderPath):
    for file in os.listdir(imagesFolderPath):
        if(getFileName(descriptionFile) == getFileName(file)):
            return file
    return None

def pairFiles(descriptionsFolder, imagesFolder):

    descriptionsFolderPath = descriptionsFolder.getFolderPath()
    imagesFolderPath = imagesFolder.getFolderPath()

    pairedFiles = []

    for descriptionFile in os.listdir(descriptionsFolderPath):
        imageFile = foundImage(descriptionFile, imagesFolderPath)
        if (imageFile is not None):
            pair = Pair(descriptionFile, imageFile)
            pairedFiles.append(pair)

    return pairedFiles

def displayPairedFiles(pairedFiles):
    for pair in pairedFiles:
        print (pair.getDescriptionFile() + "#" + pair.getImageFile())

def isFoldersSizeDifferent(firstFolder, secondFolder):
    return firstFolder.countFilesInDirectory() != secondFolder.countFilesInDirectory()

def isFileEmpty(file):
	return (os.stat(file.name).st_size == 0)

def getFileName(file):
    return os.path.splitext(file)[0]

def loginUser(driver):
    email = "a.gorczyca@jpconsulting.pl"
    password = "test123"

    emailInput = createWebElementByName("email")
    passwordInput = createWebElementByName("pass")

    emailInput.send_keys(email)
    passwordInput.send_keys(password)
    emailInput.submit()  

def isLoginRequired(driver):
    loginURL = "https://buypolish.redcart.pl/panel/plogin/index/"
    return (driver.current_url == loginURL)

def addProduct(imagePath, description):
    redirectToEditPanel()
    addImage(imagePath)
    addDescription(description)

def addImage(imagePath):
	addImageMenuItem = createWebElementByID("dpm_menu2")
	addImageMenuItem.click()
	buttonFirstWrapper = createWebElementByID("mp_menu2")
	addImageFirstButton = createNestedWebElementByClassName(buttonFirstWrapper, "rc_button")
	addImageFirstButton.click()
	buttonSecondWrapper = createWebElementByID("rc_window1")
	time.sleep(2)
	addImageSecondButton = createNestedWebElementByClassName(buttonSecondWrapper, "swiff-uploader-box")
	addImageSecondButton.click()
	time.sleep(2)
	win = win32com.client.Dispatch("WScript.Shell")
	win.SendKeys(imagePath)
	win.SendKeys("{ENTER}")
	time.sleep(3)
	closeWindow = createWebElementByClassName("rc_windowbtclose")
	closeWindow.click()

def addDescription(description):
	addDescriptionMenuItem = createWebElementByID("pm_menu4")
	addDescriptionMenuItem.click()

	descriptionWrapper = createWebElementByName("products_description_short")
	descriptionWrapper.send_keys(description)

def redirectToEditPanel():
    URL = "http://buypolish.redcart.pl/panel/products/edit/"
    driver.get(URL)

def getLastLineID(file):
	if(isFileEmpty(file)): return 1
	for line in file:
		pass
	stringNumber = ''
	for i in range(0, len(line)):
		if(line[i] is not '.'):
			stringNumber += line[i]
		else:
			break
	return (int(stringNumber) + 1)

def printStatus(file, message):
	lineID = getLastLineID(file)
	now = datetime.datetime.now()

	date = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
	file.write(str(lineID) + '.\t' + message + "\t" + date + '\n')

def successMessage(productName, productImage, productDescription):
	return ("Dodano " + productName + ':\t'
			"imageFile: " + productImage + "\t"
			"descriptionFile: " + productDescription)


if __name__ == "__main__":

	imagesFolder = Folder()
	imagesFolder.setFolderPath("images")
	imagesFolderSize = imagesFolder.countFilesInDirectory()

	descriptionsFolder = Folder();
	descriptionsFolder.setFolderPath("descriptions")
	descriptionsFolderSize = descriptionsFolder.countFilesInDirectory()

	if isFoldersSizeDifferent(imagesFolder, descriptionsFolder):
		print ("Amount of files in those folders is different.")
	else:
		pairedFiles = pairFiles(descriptionsFolder, imagesFolder)

		driver = webdriver.Chrome('C:\ChromeDriver\chromedriver')  # Optional argument, if not specified will search path.
		driver.get('http://buypolish.redcart.pl/panel/products/edit/');

		if isLoginRequired(driver):
			loginUser(driver)

		for pair in pairedFiles:
			imagePath = imagesFolder.getFolderPath() + "\\" + pair.getImageFile()
			descriptionsPath = descriptionsFolder.getFolderPath() + "\\" + pair.getDescriptionFile()
			descriptionFile = open(descriptionsPath)
			productDescription = descriptionFile.read()

			addProduct(imagePath, productDescription)

			printStatus(LOG, successMessage("productName", pair.getImageFile(), pair.getDescriptionFile()))
			#zanim puscisz skrypt sprawdz na pusto ( co wypisuje w pliku LOG [naawa produktu zdjecie itp itd])




 




        # Let the user actually see something!
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # for pair in pairedFiles:

        #     uploadElement = WebDriverWait(driver, 10).until(
        #         lambda driver: driver.find_element_by_name("uploaded_file")
        #         )

        #     descriptionElement = WebDriverWait(driver, 10).until(
        #         lambda driver: driver.find_element_by_name("file_description")
        #         )

        #     imagePath = imagesFolder.getFolderPath() + "\\" + pair.getImageFile()
        #     descriptionsPath = descriptionsFolder.getFolderPath() + "\\" + pair.getDescriptionFile()

        #     descriptionFile = open(descriptionsPath)
        #     productDescription = descriptionFile.read()

        #     uploadElement.send_keys(imagePath)
        #     descriptionElement.send_keys(productDescription)

        #     descriptionElement.submit()

        #     driver.get('http://www.tinyupload.com/')


        