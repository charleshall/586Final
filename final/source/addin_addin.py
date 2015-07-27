import arcpy
import pythonaddins

class GetAlmanacData(object):
    """Implementation for addin_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(r'G:\586\final\Final.tbx', 'Wunderground')