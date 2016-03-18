from click import echo
import click
from fnmatch import fnmatch
from os.path import isdir,join
from os import rename,listdir,remove
from constants import *
from util import flatDirectory,getMovieFileInDir,deleteAllSrtFiles,deleteUnNeededFilesIfAny
from subprocess import call


@click.command()
@click.argument('dir')
@click.argument('name')
def down(dir,name) :
		""" Download Subtitiles and renames the files to the name passedusing -nm parameter"""
		echo('Working on Directory -- %s' %dir)
		echo('New name will be set to -- %s' %name)
		if not dir or not isdir(dir) or not name:
			raise ValueError("This command works only on directorys, and should be supplied with directory and new name")
		existingSrt = getSubtitleFileLocationIfExists(dir)
		if not existingSrt:
			echo('Do download SRT files')
			flatDirectory(dir,dir)
			fileName = getMovieFileInDir(dir)
			deleteAllSrtFiles(dir)
			echo('Download Subtitles for %s' %fileName)
			call(['subliminal','download','-l','en',fileName])
			call(['syncnames','-f', dir,'-nm', name])
			deleteUnNeededFilesIfAny(dir)
		else:
			rename(existingSrt,join(dir,'english.srt'))


# gets the main movie file on which subtitles need to be download on
# assumes the biggest file in the directory or sub directory is the one we want
def getMainMovieFile(dir):
	for file in listdir(dir):
		if not isdir(join(dir,file)):
			echo('Ignoring Sub Directory -- %s' %file)
		else:
			echo('Ignoring sub folder %s' %file)

# Check if subtitles already exists and gives that file
def getSubtitleFileLocationIfExists(dir):
	for file in listdir(dir):
		# Check sub directories
		if isdir(join(dir,file)):
			sub = getSubtitleFileLocationIfExists(join(dir,file))
			if not sub:
				continue
			else:
				return sub
		# Check passed directory		
		for file in listdir(dir):
			if fnmatch(file,'*english*.srt'):
				echo('A file found that looks like english %s' %file)
				return join(dir,file)
		return ''