import time
import win32com.client
import sys
import os
import datetime
import ftplib
import ctypes
from webdriver import WebDriver
from folder import Folder
from pair import Pair
from product import Product

def initializeDriver():
	driver = WebDriver()
	driver.setWebDriverPath('C:\ChromeDriver\chromedriver')
	driver.setWaitUntilClock(10)
	return driver

def isFoldersSizeDifferent(firstFolder, secondFolder):	return firstFolder.countFilesInDirectory() != secondFolder.countFilesInDirectory()

def printDifferentSizeErrorAndQuit():
	print("Amount of files in those folders is different.")
	driver.quit()
	sys.exit()

def isLoginRequired():
	loginURL = "https://buypolish.redcart.pl/panel/plogin/index/"
	return (driver.currentURL() == loginURL)

def loginUser():
	email = "a.gorczyca@jpconsulting.pl"
	password = "test123"

	emailInput = driver.createWebElementByName("email")
	passwordInput = driver.createWebElementByName("pass")

	emailInput.send_keys(email)
	passwordInput.send_keys(password)
	emailInput.submit()  

def startAddingProducts():
	products = createListOfProducts()
	for product in products:
		addProduct(product)
		message = successMessage(product)
		printStatusToFile("log.txt", message)

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

def associateDescriptionsWithImages(descriptionsFolder, imagesFolder):
    pairs = []
    descriptionsFolderContent = descriptionsFolder.getListOfFiles()
    for descriptionFile in descriptionsFolderContent:
        imageFile = findCorrespondingImage(descriptionFile, imagesFolder)
        if (imageFile is not None):
            pair = Pair(descriptionFile, imageFile)
            pairs.append(pair)

    return pairs

def findCorrespondingImage(descriptionFile, imagesFolder):
    for file in imagesFolder.getListOfFiles():
        if(getFileName(descriptionFile) == getFileName(file)):
            return file
    return None

def getFileName(file):	return os.path.splitext(file)[0]

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

def addProduct(product):
    driver.redirectTo('http://buypolish.redcart.pl/panel/products/edit/')
    addImage(product.getImagePath())
    addDescription(product.getDescription())

def addDescription(description):
	addDescriptionMenuItem = driver.createWebElementByID("pm_menu4")
	addDescriptionMenuItem.click()

	descriptionWrapper = driver.createWebElementByName("products_description_short")
	descriptionWrapper.send_keys(description)

def addImage(imagePath):
	addImageMenuItem = driver.createWebElementByID("dpm_menu2")
	addImageMenuItem.click()
	buttonFirstWrapper = driver.createWebElementByID("mp_menu2")
	addImageFirstButton = driver.createNestedWebElementByClassName(buttonFirstWrapper, "rc_button")
	addImageFirstButton.click()
	buttonSecondWrapper = driver.createWebElementByID("rc_window1")
	time.sleep(2)
	addImageSecondButton = driver.createNestedWebElementByClassName(buttonSecondWrapper, "swiff-uploader-box")
	addImageSecondButton.click()
	time.sleep(2)
	win = win32com.client.Dispatch("WScript.Shell")
	win.SendKeys(imagePath)
	win.SendKeys("{ENTER}")
	time.sleep(3)
	closeWindow = driver.createWebElementByClassName("rc_windowbtclose")
	closeWindow.click()

def successMessage(product):
	return ("Dodano: " + product.getName() + '\t'
			"Image: " + product.getImagePath() + "\t"
			"Description: " + product.getDescription())

def printStatusToFile(fileName, message):
	file = open(fileName, "r+")
	lineID = getLastLineID(file)
	now = datetime.datetime.now()
	date = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
	file.write(str(lineID) + '.\t' + message + "\t" + date + '\n')
	file.close()

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

def isFileEmpty(file):	return (os.stat(file.name).st_size == 0)

def displayPairedFiles(pairedFiles):
    for pair in pairedFiles:
        print (pair.getDescriptionFile() + "#" + pair.getImageFile())



if __name__ == "__main__":

	driver = initializeDriver()

	imagesFolder = Folder("images")
	descriptionsFolder = Folder("descriptions")

	if isFoldersSizeDifferent(imagesFolder, descriptionsFolder):
		printDifferentSizeErrorAndQuit()
		
	driver.redirectTo("https://buypolish.redcart.pl/panel/plogin/index/")#change path

	if isLoginRequired():
		loginUser()

	startAddingProducts()
	driver.quit()