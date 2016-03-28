class Product:
	name = None
	imagePath = None
	description = None

	def __init__(self, name, imagePath, description):
		self.name = name
		self.imagePath = imagePath
		self.description = description

	def getName(self):
		return self.name
	def getImagePath(self):
		return self.imagePath
	def getDescription(self):
		return self.description	

