import time
import os
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Folder:
    rootFolder = "C:\\Users\\Korzonkie\\Desktop\\buy-polish\\"
    folderPath = None

    def setFolderPath(self, folderName):
        self.folderPath = self.rootFolder + folderName

    def getFolderPath(self):
        return self.folderPath

    def countFilesInDirectory(self):
        if(self.folderPath is None):
            return "You have to set folder path first!"
        else: return len(os.listdir(self.folderPath))

class Pair:
    descriptionFile = None
    imageFile = None
    def __init__(self, descriptionFile, imageFile):
        self.descriptionFile = descriptionFile
        self.imageFile = imageFile

    def getDescriptionFile(self):
        return self.descriptionFile

    def getImageFile(self):
        return self.imageFile


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

def getFileName(file):
    return os.path.splitext(file)[0]



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
        driver.get('http://www.tinyupload.com/');



        # Let the user actually see something!
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        for pair in pairedFiles:

            uploadElement = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_name("uploaded_file")
                )

            descriptionElement = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_name("file_description")
                )

            imagePath = imagesFolder.getFolderPath() + "\\" + pair.getImageFile()
            descriptionsPath = descriptionsFolder.getFolderPath() + "\\" + pair.getDescriptionFile()

            descriptionFile = open(descriptionsPath)
            productDescription = descriptionFile.read()

            uploadElement.send_keys(imagePath)
            descriptionElement.send_keys(productDescription)

            descriptionElement.submit()

            driver.get('http://www.tinyupload.com/')


        