# -*- coding: utf-8 -*-
import os, time
import hashlib
import argparse
import pickle
import progressbar

exclude_folder = ['.git', '.svn']

HAS_NOT_INDEX = -1
FOLDER_NOT_SET = 0
FOLDER_READ_ONLY = 1
FOLDER_SYNC = 2

FILE_STATUS_NORMAL= 0
FILE_STATUS_DELETED = 1
barValue = 1

def md5sum_file(filename, blocksize=65536):
	hash = hashlib.md5()
	with open(filename, "rb") as f:
		for block in iter(lambda: f.read(blocksize), b""):
			hash.update(block)
	return hash.hexdigest()

def md5sum_str(text):
	hash = hashlib.md5()
	m.update(text)
	return m.hexdigest()

class FileChecker:
	def __init__(self, folderSlotCount):
		self.savedFileName = ""
		self.currentFilePathIndex = HAS_NOT_INDEX
		self.currentFilePath = ""
		self.folderList = list(map(lambda n: {"Index":n, "Mode":FOLDER_NOT_SET, "Path":""}, range(folderSlotCount)))
		self.fileList = list(map(lambda n: {}, range(folderSlotCount)))

	def __del__(self) :
		pass

	def createFolderInfo(self, path, mode) :
		for i in range(len(self.folderList)) :
			if self.folderList[i]["Path"]=="" :	
				self.folderList[i]["Mode"] = mode
				self.folderList[i]["Path"] = path
				return i
		return HAS_NOT_INDEX

	def getFolderIndex(self, path) :
		for i in range(len(self.folderList)) :
			if self.folderList[i]["Path"]==path :
				return i
		return HAS_NOT_INDEX

	def appendFolder(self, path, folderType):
		findIdx = self.getFolderIndex(path)
		if findIdx!=HAS_NOT_INDEX :
			self.currentFilePathIndex = findIdx
			self.folderList[findIdx]["Mode"] = folderType
		else :
			self.currentFilePathIndex = self.createFolderInfo(path, folderType)
		self.currentFilePath = path

	def appendFile(self, path):
		fileHash = md5sum_file(path)
		modifiedTime = os.path.getmtime(path)
		createTime = os.path.getctime(path)
		accessTime = os.path.getatime(path)

		newPath = path[len(self.currentFilePath):]
		self.fileList[self.currentFilePathIndex][newPath] = {"Hash":fileHash, "CTime":createTime, "MTime":modifiedTime, "ATime":accessTime, "Status":FILE_STATUS_NORMAL}

	def saveStatus(self):
		with open('data.pickle', 'wb') as f:
			pickle.dump(self.fileList, f, pickle.HIGHEST_PROTOCOL)

	def loadStatus(self):
		with open('data.pickle', 'rb') as f:
			self.fileList = pickle.load(f)

def isExcludeDir(dirName) :
	global exclude_folder
	if dirName in exclude_folder :
		return True
	return False

def countFolder(dirname) :
	cnt = 0
	filenames = os.listdir(dirname)
	for filename in filenames:
		full_filename = os.path.join(dirname, filename)
		if os.path.isdir(full_filename) and not isExcludeDir(filename):
			cnt+=1
	return cnt

def search(dirname, fchk, bar, depth=1):
	global barValue
	try:
	    filenames = os.listdir(dirname)
	    for filename in filenames:
	        full_filename = os.path.join(dirname, filename)
	        if os.path.isdir(full_filename) :
	        	if not isExcludeDir(filename):
	        		time.sleep(0.005)
	        		barValue += 1
	        		bar.update(barValue)
	        		search(full_filename, fchk, bar, depth+1)
	        else:
	            ext = os.path.splitext(full_filename)[-1]
	            fchk.appendFile(full_filename)
	except :
		pass

def main():
	parser = argparse.ArgumentParser(description='This program synchronizes two different folders.')
	parser.add_argument('-source', type=str, default=os.getcwd(),
			help='Appoint the source folder path')
	parser.add_argument('-target', type=str, required=True, 
			help='Appoint the target folder path')
	parser.add_argument('-op', type=str, default='AtoB',
			choices=['AtoB','BtoA'],
			help='Select the direction you want to sync.')
	args = parser.parse_args()
	
	sourceFolder = args.source
	targetFolder = args.target

	cntBar = 1
	print("Source Folder :", sourceFolder)
	print("Target Folder :", targetFolder)
	cntBar += countFolder(sourceFolder)
	cntBar += countFolder(targetFolder)

	# Progress Bar
	bar = progressbar.ProgressBar(maxval=cntBar, widgets=[progressbar.Bar('█', '|', '|'), ' ', progressbar.Percentage()])
	bar.start()
	
	folderSlotCount = 2
	fchk = FileChecker(folderSlotCount)
	bar.update(1)

	fchk.appendFolder(sourceFolder, FOLDER_READ_ONLY)
	search(sourceFolder, fchk, bar)

	fchk.appendFolder(targetFolder, FOLDER_SYNC)
	search(targetFolder, fchk, bar)

	bar.update(cntBar)
	bar.finish()

if __name__=="__main__":
	main()