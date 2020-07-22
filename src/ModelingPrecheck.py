import logging
import os
import maya.cmds as cmds
import re

import pymel.core as pmc
from   pymel.core.system import Path

from array import *

from pymel.core.system import versions

log = logging.getLogger(__name__)

class SceneFile(object):
    """Class used to represent a DCC software scene file

    can be used to manipulate scene files without needing direct influence on the scene

    Attributes:
    dir(str, optional): Directory to the scene file, defaults to ''
    descriptor(str, optional): Short descriptor of the scene file, defaults to main
    version (int, optional): Version number, defaults to 1
    ext (str, optional): extension defaults to "ma"
    """
    def __init__(self, dir='', descriptor='main', version=1, ext="ma"):
        FilePath = cmds.file(q=True, sn=True)
        if(FilePath == ""):
            self._dir = Path(dir)
            self.descriptor = descriptor
            self.version = version
            self.ext = ext
        else:
            parts = os.path.split(FilePath)
            self._dir = parts[0]
            Name = parts[1].split('_v')
            self.descriptor = Name[0]
            Split2 = Name[1].split('.')
            self.version = int(Split2[0])
            self.ext = Split2[1]

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, val):
        self._dir = Path(val)

    def basename(self):
        """Returns the DCC scene file's name

        Returns:
            STR: THE NAME OF THE SCENE FILE"""
        name_pattern = "{descriptor}_{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor, version=self.version, ext=self.ext)
        return name

    def path(self):
        """The function returns a path to scene file
        includes drive letter, any directory path and the file name

        Returns:
            Path: The path to the scene file
            """
        return Path(self.dir) / self.basename()

    def save(self):
        """Saves the scene file.

        Returns:
            :obj:'Path': The path to the scene file if successful, None, otherwise
            """
        try:
            Path = self.dir+ "\\" + self.descriptor + '_v0' + str(self.version) + '.' + self.ext
            pmc.system.saveAs(Path)
        except RuntimeError:
            log.warning("Missing directories. creating directories")
            self.dir.makedirs_p()
            Path = self.dir + "\\" + self.descriptor + '_v0' + str(self.version) + '.' + self.ext
            pmc.system.saveAs(Path)

    def Trifecta(self):
        #select all objects in the scene
        pmc.select(all=True)
        #delete the construction history of the object
        pmc.delete(ch = True)
        #center the pivot on the object
        pmc.xform(cp=True)
        #Freeze all transformations
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    def MergeVertices(self):
        #select all objects in the scene
        pmc.select(all=True)
        #change selection mode to component
        pmc.selectMode( component=True )

        pmc.selectType(v=True)


    def CheckNames(self):
        count = 0
        RegPattern = "[A-Z][a-z]+_objShape"
        ProblemObjects = {}
        ObjectNames = pmc.ls( o = True, g = True)
        for Object in ObjectNames:
            if not(bool(re.match(RegPattern, str(Object)))):
                ProblemObjects[count] = Object
                count = count + 1
        return ProblemObjects


    def FinalSave(self):
        """Saves the scene file."""
        try:
            Path = self.dir + "\\" + self.descriptor + '_Final' + '.' + self.ext
            pmc.system.saveAs(Path)
        except RuntimeError:
            log.warning("Missing directories. creating directories")
            self.dir.makedirs_p()
            Path = self.dir + "\\" + self.descriptor + '_Final' + '.' + self.ext
            pmc.system.saveAs(Path)