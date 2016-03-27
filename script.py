import time
import win32com.client
import sys
import os
import datetime
import ftplib
import ctypes
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from folder import Folder
from pair import Pair
from product import Product

WAIT = 10
driver = webdriver.Chrome('C:\ChromeDriver\chromedriver')


def initializeDriver():	return webdriver.Chrome('C:\ChromeDriver\chromedriver')
def createWebElementByName(name):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: driver.find_element_by_name(name)
			)
	except:
		printStatusToFile("errors.txt", "Element: '" + name + "' is not visible")
		sys.exit()
	return element
def createWebElementByID(ID):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: driver.find_element_by_id(ID)
			)
	except:
		printStatusToFile("errors.txt", "Element: '" + ID + "' is not visible")
		sys.exit()
	return element
def createWebElementByClassName(className):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: driver.find_element_by_class_name(className)
			)
	except:
		printStatusToFile("errors.txt", "Element: '" + className + "' is not visible")
		sys.exit()
	return element
def createNestedWebElementByClassName(container, className):
	try:
		element = WebDriverWait(driver, WAIT).until(
			lambda driver: container.find_element_by_class_name(className)
			)
	except:
		printStatusToFile("errors.txt", "Element: '" + className + "' is not visible")
		sys.exit()
	return element
def findCorrespondingImage(descriptionFile, imagesFolder):
    for file in imagesFolder.getListOfFiles():
        if(getFileName(descriptionFile) == getFileName(file)):
            return file
    return None
def associateDescriptionsWithImages(descriptionsFolder, imagesFolder):
    pairs = []
    descriptionsFolderContent = descriptionsFolder.getListOfFiles()
    for descriptionFile in descriptionsFolderContent:
        imageFile = findCorrespondingImage(descriptionFile, imagesFolder)
        if (imageFile is not None):
            pair = Pair(descriptionFile, imageFile)
            pairs.append(pair)

    return pairs
def createListOfProducts():
	products = []
	associatedFolders = associateDescriptionsWithImages(descriptionsFolder, imagesFolder)
	for associatedFiles in associatedFolders:
		productName = retrieveProductName(associatedFiles)
		productImagePath = retrieveProductImagePath(associatedFiles)
		productDescription = retrieveProductDescription(associatedFiles)

		product = Product(productName, productImagePath, productDescription)
		products.append(product)

	return products
def retrieveProductName(associatedFiles):
	descriptionFilePath = descriptionsFolder.getFolderPath() + "\\" + associatedFiles.getDescriptionFile()
	descriptionFile = open(descriptionFilePath)
	productName = descriptionFile.readline()
	descriptionFile.close()

	return productName
def retrieveProductImagePath(associatedFiles):
	imageFilePath = imagesFolder.getFolderPath() + "\\" + associatedFiles.getImageFile()

	return imageFilePath
def retrieveProductDescription(associatedFiles):
	descriptionFilePath = descriptionsFolder.getFolderPath() + "\\" + associatedFiles.getDescriptionFile()
	descriptionFile = open(descriptionFilePath)
	productDescription = descriptionFile.read()
	descriptionFile.close()

	return productDescription
def displayPairedFiles(pairedFiles):
    for pair in pairedFiles:
        print (pair.getDescriptionFile() + "#" + pair.getImageFile())
def isFoldersSizeDifferent(firstFolder, secondFolder):	return firstFolder.countFilesInDirectory() != secondFolder.countFilesInDirectory()
def isFileEmpty(file):	return (os.stat(file.name).st_size == 0)
def getFileName(file):	return os.path.splitext(file)[0]
def loginUser():
	print("halo")
	email = "a.gorczyca@jpconsulting.pl"
	password = "test123"

	emailInput = createWebElementByName("email")
	passwordInput = createWebElementByName("pass")

	emailInput.send_keys(email)
	passwordInput.send_keys(password)
	emailInput.submit()  
def isLoginRequired():
	loginURL = "https://buypolish.redcart.pl/panel/plogin/index/"
	print(driver.current_url + " # " + loginURL)
	return (driver.current_url == loginURL)
def addProduct(product):
    redirectTo('http://buypolish.redcart.pl/panel/products/edit/')
    addImage(product.getImagePath())
    addDescription(product.getDescription())
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
def redirectTo(URL):	driver.get(URL)
def getLastLineID(file):
	if(isFileEmpty(file)): return 1
	for line in file:
		pass
	stringNumber = '0'
	for i in range(0, len(line)):
		if(line[i] is not '.'):
			stringNumber += line[i]
		else:
			break
	return (int(stringNumber) + 1)
def printStatusToFile(fileName, message):
	file = open(fileName, "r+")
	lineID = getLastLineID(file)
	now = datetime.datetime.now()
	date = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
	file.write(str(lineID) + '.\t' + message + "\t" + date + '\n')
	file.close()
def successMessage(product):
	return ("Dodano " + product.getName() + ':\t'
			"Image: " + product.getImagePath() + "\t"
			"Description: " + product.getDescription)
def startAddingProducts():
	products = createListOfProducts()
	for product in products:
		addProduct(product)
		message = successMessage(product.getName(), product.getImagePath(), product.getDescription())
		printStatusToFile("log.txt", message)

if __name__ == "__main__":
	imagesFolder = Folder("images")
	descriptionsFolder = Folder("descriptions")

	if isFoldersSizeDifferent(imagesFolder, descriptionsFolder):
		print("Amount of files in those folders is different.")
		sys.exit()

	if isLoginRequired():
		loginUser()

	startAddingProducts()
	driver.quit()