from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebDriver:
	waitUntilClock = None
	driver = None

	def setWebDriverPath(self, path):
		self.driver = webdriver.Chrome(path)

	def setWaitUntilClock(self, time):
		self.waitUntilClock = time

	def redirectTo(self, URL):
		self.driver.get(URL)

	def currentURL(self):
		return self.driver.current_url

	def createWebElementByName(self, name):
		try:
			element = WebDriverWait(self.driver, self.waitUntilClock).until(
				lambda driver: self.driver.find_element_by_name(name)
				)
		except:
			printStatusToFile("errors.txt", "Element: '" + name + "' is not visible")
			sys.exit()
		return element

	def createWebElementByID(self, ID):
		try:
			element = WebDriverWait(self.driver, self.waitUntilClock).until(
				lambda driver: self.driver.find_element_by_id(ID)
				)
		except:
			printStatusToFile("errors.txt", "Element: '" + ID + "' is not visible")
			sys.exit()
		return element

	def createWebElementByClassName(self, className):
		try:
			element = WebDriverWait(self.driver, self.waitUntilClock).until(
				lambda driver: self.driver.find_element_by_class_name(className)
				)
		except:
			printStatusToFile("errors.txt", "Element: '" + className + "' is not visible")
			sys.exit()
		return element

	def createNestedWebElementByClassName(self, container, className):
		try:
			element = WebDriverWait(self.driver, self.waitUntilClock).until(
				lambda driver: container.find_element_by_class_name(className)
				)
		except:
			printStatusToFile("errors.txt", "Element: '" + className + "' is not visible")
			sys.exit()
		return element

	def printStatusToFile(fileName, message):
		file = open(fileName, "r+")
		lineID = getLastLineID(file)
		now = datetime.datetime.now()
		date = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
		file.write(str(lineID) + '.\t' + message + "\t" + date + '\n')
		file.close()

