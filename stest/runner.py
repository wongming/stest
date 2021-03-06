import sys
import time, datetime

from stest import result

__stest = True

class TestRunner(object):
    def __init__(self, stream=sys.stderr,resultclass=None):
        if resultclass is not None:
            self.resultclass = resultclass
        else:
            self.resultclass = result.TestResult
        self.stream = stream

    def _makeResult(self):
        return self.resultclass(stream=self.stream)

    def run(self, test):
        result = self._makeResult()
        result.projectName = test.projectName
        startTime = datetime.datetime.now()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = datetime.datetime.now()
        timeTaken = stopTime - startTime
        result.startTime = datetime.datetime.strftime(startTime, '%Y.%m.%d %H:%M:%S.%f');
        result.stopTime = datetime.datetime.strftime(stopTime, '%Y.%m.%d %H:%M:%S.%f');
        result.timeTaken = timeTaken.total_seconds()
        result.printResult()
        return result

defaultTestRunner = TestRunner()
