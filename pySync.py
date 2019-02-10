import os
import argparse

exclude_folder = ['.git', '.svn']

def isExcludeDir(dirName) :
	global exclude_folder
	if dirName in exclude_folder :
		return True
	return False

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename) and not isExcludeDir(filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                print(full_filename)
    except PermissionError:
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

	search(sourceFolder)
	print "Source Folder :", sourceFolder
	print "Target Folder :", targetFolder

if __name__=="__main__":
	main()