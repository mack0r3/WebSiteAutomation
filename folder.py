import os

class Folder:
	rootFolder = "C:\\Users\\Bogus\\Desktop\\buy-polish\\"
	folderPath = None

	def __init__(self, folderName):
		self.folderPath = self.rootFolder + folderName

	def getFolderPath(self):	return self.folderPath
	def getListOfFiles(self):	return os.listdir(self.folderPath)
	def countFilesInDirectory(self):
		if(self.folderPath is None):
			return "You have to set folder path first!"
		else:
			return len(os.listdir(self.folderPath))