from distutils.core import setup
import
import py2exe
import sys
includes = ["encodings", "encodings.*"]
sys.argv.append("py2exe")
options = {"py2exe":  { "bundle_files": 1 }
                }
setup(options = options,
      zipfile=None,
      console = [{"script":'C:/Users/Alance/PycharmProjects/Python/base.py', 'icon_resources':[(1, 'C:/Users/Alance/PycharmProjects/Python/logo.ico')]}],)


