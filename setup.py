# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable
import requests.certs

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit',
        'include_files':[(requests.certs.where(),'cacert.pem')]
    },
    
}



executables = [
    Executable('wepush.py', base=base,icon='./wechat.ico'),
    
]

setup(name='wepush',
      version='0.1',
      requires = ["requests"],
      description='wxpush',
      options=options,
      executables=executables
      )
