from os.path import join,isfile,isdir,dirname,getsize
from os import listdir,rmdir,remove
from click import echo
from fnmatch import fnmatch
from constants import FILE_FORMATS
from os import rename


def getMovieFileInDir(path):
	files = []
	for file in listdir(path):
		fileName = join(path,file)
		if isfile(fileName):
			for format in FILE_FORMATS:
				if fnmatch(fileName,format):
					files.append(fileName)
				else:
					echo('Ignoring %s' %fileName)
		else:
			echo('Ignoring %s as its not a file' %fileName)

	for i in range(len(files)):
		files[i] = (files[i], getsize(files[i]))

	files.sort(key=lambda fileName:fileName[1], reverse=True)
	return files[0][0]


def flatDirectory(rootdir, dir):
	for file in listdir(dir):
		fileName = join(dir,file)
		if isdir(fileName):
			flatDirectory(rootdir,fileName)
			rmdir(fileName)
		elif dirname(fileName) != rootdir:
			try:
				rename(fileName,join(rootdir,file))
			except:
				echo('Unable to rename file %s' %fileName)
		else:
			echo('File %s is already on root' %fileName)

def deleteAllSrtFiles(dir):
	for file in listdir(dir):
		if fnmatch(file,'*.srt'):
			remove(join(dir,file))

def deleteUnNeededFilesIfAny(dir):
	movieFile = getMovieFileInDir(dir)
	for file in listdir(dir):
		if join(dir,file) != movieFile and not fnmatch(file,'*.srt'):
			remove(join(dir,file))