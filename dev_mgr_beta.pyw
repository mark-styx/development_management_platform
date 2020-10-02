import sys
from os.path import basename,dirname,abspath
from inspect import getsourcefile
sys.path.append( dirname(abspath(getsourcefile(lambda:0))) + '\\classes\\gui' )

from main_menu import Main_Menu
if __name__ == "__main__":
    Main_Menu()