import os
import unittest

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose


class ValidationController(CementBaseController):

    class Meta:

        label = 'base'
        description = "GD_cmd_tool provides developers useful utilities."
        arguments = [
            (['-mp', '--module_path'],
              dict(action='store', help='the big C option')),
            (['-mn', '--module_name'],
             dict(action='store', help='the big C option')),
            (['-ma', '--module_author'],
              dict(action='store', help='the big C option')),
            (['-mt', '--module_type'],
              dict(action='store', help='the big C option')),
            (['-mvm', '--module_validation_mode'],
              dict(action='store', help='the big C option')),
        ]

        # ValidationController.Validation.test = self.app.pargs.module_path

    @expose(hide=True)
    def default(self):
        self.app.log.info('Inside MyBaseController.default()')
        ValidationController.Validation.test = self.app.pargs.module_path
        # self.test_src_directory()
        suite = unittest.TestSuite()
        suite.addTest(self.Validation('test_src_directory'))
        suite.addTest(self.Validation('test_src_checkpoint_directory'))
        suite.addTest(self.Validation('test_src_data_directory'))
        suite.addTest(self.Validation('test_main_file'))
        suite.addTest(self.Validation('test_module_spec_file'))
        suite.addTest(self.Validation('test_requirements_file'))
        runner = unittest.TextTestRunner()
        runner.run(suite)

        # if self.app.pargs.predict:
        #     print("Recieved option: foo => %s" % self.app.pargs.predict)


    @expose(aliases=['cmd2'], help="more of nothing")
    def command2(self):
        self.app.log.info("Inside MyBaseController.command2()")
        if self.app.pargs.foo:
            print('test')

    class Validation(unittest.TestCase):

        MODULE_PATH = "/Users/Chun/Documents/workspace/momodel/goldersgreen/pyserver/user_directory/zhaofengli/weather_prediction"
        MODULE_NAME = "weather_prediction"
        MODULE_AUTHOR = "zhaofengli"
        MODULE_TYPE = 'model'
        MODULE_VALIDATION_MODE = 'basic'

        def test_src_directory(self):
            '''
                To check the [/src/] direcotary
            :return:
            '''
            self.assertTrue(os.path.isdir(
                "{}/src".format(self.MODULE_PATH)),
                msg="[/src/] directory does not exist")


        def test_src_checkpoint_directory(self):
            '''
                To check the [/src/checkpoint/] direcotary
            :return:
            '''

            self.assertTrue(os.path.isdir(
                "{}/src/checkpoint".format(self.MODULE_PATH)),
                msg="[/src/checkpoint] directory does not exist")

        def test_src_data_directory(self):
            '''
                To check the [/src/data/] direcotary
            :return:
            '''
            self.assertTrue(os.path.isdir(
                "{}/src/data".format(self.MODULE_PATH)),
                msg="[/src/data/] directory does not exist")

        def test_main_file(self):
            '''
                To check the [/src/main.py] file
            :return:
            '''
            self.assertTrue(os.path.exists(
                "{}/src/main.py".format(self.MODULE_PATH)),
                msg="[/src/main.py] does not exist")

        def test_module_spec_file(self):
            '''
                To check the [/src/module_spec.yml] file
            :return:
            '''
            self.assertTrue(os.path.exists(
                "{}/src/module_spec.yml".format(self.MODULE_PATH)),
                msg="[/src/module_sepc.yml] does not exist")

        def test_requirements_file(self):
            '''
                To check the [/requirements.txt] file
            :return:
            '''
            self.assertTrue(os.path.exists(
                "{}/requirements.txt".format(self.MODULE_PATH)),
                msg="[requirements.txt] does not exist")


class UtilityController(CementBaseController):
    class Meta:
        label = 'utility'
        stacked_on = 'base'

    @expose(help='this is some utility command', aliases=['some-cmd'])
    def second_cmd1(self):
        self.app.log.info("Inside MySecondController.second_cmd1")


class MyApp(CementApp):
    class Meta:
        label = 'GD_cmd_tool'
        base_controller = 'base'
        handlers = [ValidationController, UtilityController]



with MyApp() as app:
    app.run()
