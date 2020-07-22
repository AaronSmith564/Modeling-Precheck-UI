import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import pymel.core as pmc

import ModelingPrecheck

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class ModelingPrecheckUI(QtWidgets.QDialog):
    """performs last minute surface fixes before Freezing transformation of the object"""
    """centering the pivot and deleting the history. as well as checking the naming conventions"""
    """for combined objects. then saving a file with final subdescriptor"""

    def __init__(self):
        """function called whenever you create an object of this class"""
        """Constructor"""
        # Passing the object Simple UI as an argument to super()
        # makes this line python 2 and 3 compatible
        super(ModelingPrecheckUI, self).__init__(parent=maya_main_window()) # runs the init of the Qdialog class
        self.scene = ModelingPrecheck.SceneFile()
        self.setWindowTitle("Modeling Precheck")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # removes the help button from the default flags in the window

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create widgets for our UI"""
        self.title_lbl = QtWidgets.QLabel("Modeling Precheck")
        self.title_lbl.setStyleSheet("font: bold 40px")
        self.dir_lbl = QtWidgets.QLabel("Save Directory")
        self.dir_le = QtWidgets.QLineEdit()  # widget that takes an input
        self.dir_le.setText(self.scene.dir)
        self.browse_btn = QtWidgets.QPushButton("Browse...")

        self.finalize_lbl = QtWidgets.QLabel("Freeze Transforms, center pivot, Delete History")
        self.finalize_btn = QtWidgets.QPushButton("Finalize Objects")

        self.scan_lbl = QtWidgets.QLabel("Scan Object Names")
        self.scan_btn = QtWidgets.QPushButton("Scan")
        self.obj_selected_lbl = QtWidgets.QLabel()
        self.obj_lw = QtWidgets.QListWidget()
        self._populate_object_list()  # function to populate the list

        self.save_btn = QtWidgets.QPushButton("Save Final File")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        """lay out our widgets in the UI"""

        self.directory_lay = QtWidgets.QHBoxLayout()
        self.directory_lay.addWidget(self.dir_lbl)
        self.directory_lay.addWidget(self.dir_le)
        self.directory_lay.addWidget(self.browse_btn)

        self.finalize_lay = QtWidgets.QHBoxLayout()
        self.finalize_lay.addWidget(self.finalize_lbl)
        self.finalize_lay.addWidget(self.finalize_btn)

        self.scan_lay = QtWidgets.QHBoxLayout()
        self.scan_lay.addWidget(self.scan_lbl)
        self.scan_lay.addWidget(self.scan_btn)
        self.scan_lay.addWidget(self.obj_selected_lbl)
        self.scan_lay.addWidget(self.obj_lw)

        self.bottom_btn_lay = QtWidgets.QHBoxLayout()
        self.bottom_btn_lay.addWidget(self.save_btn)
        self.bottom_btn_lay.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_lbl)
        self.main_layout.addLayout(self.directory_lay)
        self.main_layout.addLayout(self.finalize_lay)
        self.main_layout.addLayout(self.scan_lay)
        self.main_layout.addStretch() # adds a space between the bottom buttons and the rest of the widgets
        self.main_layout.addLayout(self.bottom_btn_lay)
        self.setLayout(self.main_layout)

    def create_connections(self):
        """connects our widgit signals to slots"""
        #connects the bool output of a button to a object attribute
        self.browse_btn.clicked.connect(self.browse)
        self.finalize_btn.clicked.connect(self.Finalize)
        self.scan_btn.clicked.connect(self.scan)
        self.obj_lw.itemSelectionChanged.connect(self._update_file_selected_lbl)
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)

    @QtCore.Slot()
    def _update_file_selected_lbl(self):
        #self.obj_selected_lbl.setText(self.obj_lw.currentItem().text())
        Object = self.obj_lw.currentItem().text().split('Shape')
        pmc.select(Object[0])

    def _populate_object_list(self):
        pass

    @QtCore.Slot()
    def save(self):
        """saves the dialog"""
        self.scene.save()

    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog"""
        self.close()

    @QtCore.Slot()
    def browse(self):
        """Opens the file browser"""
        NewDirectory = QtWidgets.QFileDialog.getExistingDirectory()
        self.scene.dir = NewDirectory
        self.dir_le.setText(self.scene.dir)

    @QtCore.Slot()
    def Finalize(self):
        """Finalize the objects"""
        self.scene.Trifecta()

    @QtCore.Slot()
    def scan(self):
        """scans the object names"""
        self.obj_lw.clear()
        Count = 0
        ProblemObjects = self.scene.CheckNames()
        for Object in ProblemObjects:
            lw_item = QtWidgets.QListWidgetItem(str(ProblemObjects[Count]) + "  Incorrect syntax")
            self.obj_lw.addItem(lw_item)
            Count = Count + 1
