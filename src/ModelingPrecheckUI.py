import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import ModelingPrecheck

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class ModelingPrecheck(QtWidgets.QDialog):
    """performs last minute surface fixes before Freezing transformation of the object"""
    """centering the pivot and deleting the history. as well as checking the naming conventions"""
    """for combined objects. then saving a file with final subdescriptor"""