import sys
import numpy as np
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
# from PyMca5.PyMcaIO import specfilewrapper as specfile
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget
import orangecanvas.resources as resources
import sys,os

class OWdyndiffraction(widget.OWWidget):
    name = "dyndiffraction"
    id = "orange.widgets.datadyndiffraction"
    description = "Application to compute..."
    icon = "icons/dyndiffraction.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["oasysaddontemplate", "dyndiffraction"]
    outputs = [{"name": "oasysaddontemplate-data",
                "type": np.ndarray,
                "doc": "transfer numpy arrays"},
               # another possible output
               # {"name": "oasysaddontemplate-file",
               #  "type": str,
               #  "doc": "transfer a file"},
                ]

    # widget input (if needed)
    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    ENERGY = Setting(10000.0)
    MIN_ANGLE = Setting(0.995)
    MAX_ANGLE = Setting(1.005)
    NPOINTS = Setting(500)
    N_LAYERS = Setting(2)
    ORIENTATION_INPUT = Setting(0)
    CRYSTAL_NAME_0 = Setting(0)
    MILLER_0 = Setting("0,0,1")
    V_PERP_0 = Setting("0,0,1")
    PSI_0 = Setting(0.0)
    V_PAR_0 = Setting("1,0,0")
    CRYSTAL_NAME_1 = Setting(0)
    THICKNESS_1 = Setting("1000.0")
    V_PERP_1 = Setting("0,0,1")
    PSI_1 = Setting(0.0)
    V_PAR_1 = Setting("1,0,0")
    CRYSTAL_NAME_2 = Setting(0)
    THICKNESS_2 = Setting("1000.0")
    V_PERP_2 = Setting("0,0,1")
    PSI_2 = Setting(0.0)
    V_PAR_2 = Setting("1,0,0")
    DUMP_TO_FILE = Setting(0)
    FILE_NAME = Setting("tmp.dat")


    def __init__(self):
        super().__init__()

        box0 = gui.widgetBox(self.controlArea, " ",orientation="horizontal") 
        #widget buttons: compute, set defaults, help
        gui.button(box0, self, "Compute", callback=self.compute)
        gui.button(box0, self, "Defaults", callback=self.defaults)
        gui.button(box0, self, "Help", callback=self.get_doc)
        self.process_showers()
        box = gui.widgetBox(self.controlArea, " ",orientation="vertical") 
        
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MIN_ANGLE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MAX_ANGLE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "N_LAYERS",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['substrate only', '1', '2'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ORIENTATION_INPUT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['angle', 'vector'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_NAME_0",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Si', 'Ge', 'GaAs'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MILLER_0",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "V_PERP_0",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PSI_0",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "V_PAR_0",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_NAME_1",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Si', 'Ge', 'GaAs'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THICKNESS_1",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "V_PERP_1",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PSI_1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "V_PAR_1",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_NAME_2",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Si', 'Ge', 'GaAs'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THICKNESS_2",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "V_PERP_2",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PSI_2",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "V_PAR_2",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "DUMP_TO_FILE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Yes', 'No'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Energy [eV]','Minimum angle (as a fraction of the Bragg angle)','Maximum angle (as a fraction of the Bragg angle)','Number of points','Number of layers','Crystal orientation specified by','Substrate: Crystal', 'Substrate: Miller indices','Substrate: Vector normal to the surface (coordinates in reciprocal space system)','Substrate: psi (orientation of the scattering plane) [rad]','Substrate: Vector parallel to the surface and to the scattering plane (coordinate in reciprocal space system)','Layer 1: Crystal', 'Layer 1: Thickness [Angstrom]', 'Layer 1: Vector normal to the surface (coordinates in reciprocal space system)','Layer 1: psi (orientation of the scattering plane)','Layer 1: Vector parallel to the surface and to the scattering plane (coordinate in reciprocal space system)','Layer 2: Crystal', 'Layer 2: Thickness [Angstrom]', ' Layer 2: Vector normal to the surface (coordinates in reciprocal space system)','Layer 2: psi (orientation of the scattering plane)','Layer 2: Vector parallel to the surface and to the scattering plane (coordinate in reciprocal space system)','Dump to file','File name']


    def unitFlags(self):
         return ['True', 'True', 'True', 'True', 'True','True', 'True','True','True', 'self.ORIENTATION_INPUT==0','self.ORIENTATION_INPUT==1', 'self.N_LAYERS>0', 'self.N_LAYERS>0', 'self.N_LAYERS>0', 'self.N_LAYERS>0 & self.ORIENTATION_INPUT==0', 'self.N_LAYERS>0 & self.ORIENTATION_INPUT==1', 'self.N_LAYERS>1','self.N_LAYERS>1','self.N_LAYERS>1', 'self.N_LAYERS>1 & self.ORIENTATION_INPUT==0','self.N_LAYERS>1 & self.ORIENTATION_INPUT==1', 'True','self.DUMP_TO_FILE == 0']


    def compute(self):
        dataArray = OWdyndiffraction.calculate_external_dyndiffraction(ENERGY=self.ENERGY,MIN_ANGLE=self.MIN_ANGLE,MAX_ANGLE=self.MAX_ANGLE,NPOINTS=self.NPOINTS,N_LAYERS=self.N_LAYERS,ORIENTATION_INPUT=self.ORIENTATION_INPUT,CRYSTAL_NAME_0=self.CRYSTAL_NAME_0,MILLER_0=self.MILLER_0,V_PERP_0=self.V_PERP_0,PSI_0=self.PSI_0,V_PAR_0=self.V_PAR_0,CRYSTAL_NAME_1=self.CRYSTAL_NAME_1,THICKNESS_1=self.THICKNESS_1,V_PERP_1=self.V_PERP_1,PSI_1=self.PSI_1,V_PAR_1=self.V_PAR_1,CRYSTAL_NAME_2=self.CRYSTAL_NAME_2,THICKNESS_2=self.THICKNESS_2,V_PERP_2=self.V_PERP_2,PSI_2=self.PSI_2,V_PAR_2=self.V_PAR_2,DUMP_TO_FILE=self.DUMP_TO_FILE,FILE_NAME=self.FILE_NAME)

        # if fileName == None:
        #     print("No file to send")
        # else:
        #     self.send("oasysaddontemplate-file",fileName)

        self.send("oasysaddontemplate-data",dataArray)


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def get_doc(self):
        print("help pressed.")
        home_doc = resources.package_dirname("orangecontrib.oasysaddontemplate") + "/doc_files/"
        filename1 = os.path.join(home_doc,'dyndiffraction'+'.txt')
        print("Opening file %s"%filename1)
        if sys.platform == 'darwin':
            command = "open -a TextEdit "+filename1+" &"
        elif sys.platform == 'linux':
            command = "gedit "+filename1+" &"
        os.system(command)


    #
    # this is the calculation method to be implemented by the user
    # It is defined as static method to get all inputs from the arguments so it
    # can easily moved outside the class
    #
    @staticmethod
    def calculate_external_dyndiffraction(ENERGY=10000.0,MIN_ANGLE=0.995,MAX_ANGLE=1.005,NPOINTS=500,N_LAYERS=2,ORIENTATION_INPUT=0,CRYSTAL_NAME_0=0,MILLER_0="0,0,1",V_PERP_0="0,0,1",PSI_0=0.0,V_PAR_0="1,0,0",CRYSTAL_NAME_1=0,THICKNESS_1="1000.0",V_PERP_1="0,0,1",PSI_1=0.0,V_PAR_1="1,0,0",CRYSTAL_NAME_2=0,THICKNESS_2="1000.0",V_PERP_2="0,0,1",PSI_2=0.0,V_PAR_2="1,0,0",DUMP_TO_FILE=0,FILE_NAME="tmp.dat"):
        print("Inside calculate_external_dyndiffraction. ")
        return(None)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWdyndiffraction()
    w.show()
    app.exec()
    w.saveSettings()
