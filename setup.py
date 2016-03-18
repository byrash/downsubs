from setuptools import setup

setup(name="downsubs",
	version="1.0",
	description="Downloads subtitles in english (if not exists) and renames files and folders to a single name",
	author="Shivaji Byrapaneni",
	py_module=['downsubs'],
	install_requires=[
		'Click',
		'subliminal',
	],
	entry_points='''
 		[console_scripts]
 		downsubs=downsubs:down
	''',
	)