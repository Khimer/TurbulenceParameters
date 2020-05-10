from Tests.MainWindowTest import *
if __name__ == "__main__":
    MainWindowTestSuite = unittest.TestSuite()
    MainWindowTestSuite.addTest(unittest.makeSuite(MainWindowTest))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(MainWindowTestSuite)