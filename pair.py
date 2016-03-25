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