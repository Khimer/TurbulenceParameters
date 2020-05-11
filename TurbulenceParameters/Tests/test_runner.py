#from .MainWindowTest import *
from .utest import *

MainWindowTestSuite = unittest.TestSuite()
#MainWindowTestSuite.addTest(unittest.makeSuite(MainWindowTest))
MainWindowTestSuite.addTest(unittest.makeSuite(DownloaderTest))
MainWindowTestSuite.addTest(unittest.makeSuite(ParserTest))
MainWindowTestSuite.addTest(unittest.makeSuite(WriterTest))
MainWindowTestSuite.addTest(unittest.makeSuite(ReaderTest))
MainWindowTestSuite.addTest(unittest.makeSuite(AggregatorTest))
MainWindowTestSuite.addTest(unittest.makeSuite(CalculatorTest))
MainWindowTestSuite.addTest(unittest.makeSuite(CommonTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(MainWindowTestSuite)