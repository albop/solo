
__author__="Pablo Winant"
__date__ ="$10 august 2012 16:32:00$"
__version__ = 0.1


from setuptools import setup,find_packages
import py2exe

from glob import glob



data_files = [(
    "Microsoft.VC90.CRT",
    glob("C:\\Program Files\\pythonxy\\console\\Microsoft.VC90.CRT\\*.*")
)]

excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list",
            "Tkconstants","Tkinter","tcl","numpy","scipy","wx","matplotlib"
            "cython","PyQt4"," libmp","wx","matplotlibb"]

import sys
sys.path.append("C:\\Program Files\\pythonxy\\console\\Microsoft.VC90.CRT\\")

import sys
sys.path.append("C:\\Program Files\\pythonxy\\console\\Microsoft.VC90.CRT\\")
setup (
    name = 'solo',
    version = __version__,

    # Declare your packages' dependencies here, for eg:

    # Fill in these to make your Egg ready for upload to
    # PyPI
    author = 'Pablo Winant',
    author_email = '',

    url = 'www.mosphere.fr',
    license = 'BSD',
	
	packages = find_packages('.'),
    package_dir = {'':'.'},

    scripts = ['./solo.py'],
 
	data_files = data_files,
 
    options = {
            "py2exe" : {
                #"includes" : ["sip"],
				"excludes" : excludes,
                "dist_dir" : "../windist/",
                "bundle_files" : 3
            }
    },
    console = ['solo.py'],
    )
