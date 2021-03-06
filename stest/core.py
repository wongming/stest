import sys
import os

from stest import loader, runner, notice

__stest = True

class Executor(object):
    def __init__(self, target, isPlan=False, testRunner=runner.defaultTestRunner, testLoader=loader.defaultTestLoader):
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.target = target
        self.isPlan = isPlan

    def createTests(self):
        if self.isPlan:
            self.plan, self.tests = self.testLoader.loadTestsFromPlan(self.target)
        else:
            if os.path.isdir(self.target):
                self.tests = self.testLoader.loadTestsFromDir(self.target, projectName=self.target)
            if os.path.isfile(self.target):
                self.tests = self.testLoader.loadTestsFromFile(self.target, projectName=self.target)

    def runTests(self):
        self.createTests()
        self.result = self.testRunner.run(self.tests)
        if self.isPlan:
            self.result.description = 'Test Report of [%s] from ATRS' % self.result.projectName
            self.result.emailList = self.plan['Email List']
            import notice
            noticeTool = notice.TestNotice()
            html_report = noticeTool.generateHtmlReport(self.result)
            self.result.html_report = html_report
            noticeTool.sendEmailNotice(self.result, template=html_report)
        self.tests=None
        return self.result
'''
    def sendEmailNotice(self):
        if self.isPlan:
            self.result.description = 'Test Report of [%s] from ATRS' % self.result.projectName
            self.result.emailList = self.plan['Email List']
            import notice
            noticeTool = notice.TestNotice()
            htmlReport = noticeTool.generateHtmlReport(self.result)
            noticeTool.sendEmailNotice(self.result)
'''

def runCase(target):
    target = os.path.abspath(target)
    executor = Executor(target)
    result = executor.runTests()
    return result

def runPlan(target):
    target = os.path.abspath(target)
    executor = Executor(target, isPlan=True)
    result = executor.runTests()
    #executor.sendEmailNotice()
    return result
