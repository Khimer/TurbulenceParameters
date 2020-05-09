import unittest
from TurbulenceParameters.MainWindowTest import *

MainWindowTestSuite = unittest.TestSuite()
MainWindowTestSuite.addTest(unittest.makeSuite(MainWindowTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(MainWindowTestSuite)