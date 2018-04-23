import os
import re
import importlib
import unittest
import yaml
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose


class ValidationController(CementBaseController):

    class Meta:

        label = 'base'
        description = "GD_cmd_tool provides developers useful utilities."
        arguments = [
            (['-p', '--module_path'],
              dict(action='store', help='the big C option')),
            (['-n', '--module_name'],
             dict(action='store', help='the big C option')),
            (['-a', '--module_author'],
              dict(action='store', help='the big C option')),
            (['-t', '--module_type'],
              dict(action='store', help='the big C option')),
            (['-m', '--module_validation_mode'],
              dict(action='store', help='the big C option'))

        ]

    @expose(hide=True)
    def default(self):
        self.app.log.info('Inside MyBaseController.default()')
        ValidationController.Validation.test = self.app.pargs.module_path

        if self.app.pargs.module_path:
            ValidationController.Validation.MODULE_PATH = \
                self.app.pargs.module_path

        if self.app.pargs.module_name:
            ValidationController.Validation.MODULE_NAME = \
                self.app.pargs.module_name

        if self.app.pargs.module_author:
            ValidationController.Validation.MODULE_AUTHOR = \
                self.app.pargs.module_author

        if self.app.pargs.module_type:
            ValidationController.Validation.MODULE_TYPE = \
                self.app.pargs.module_type

        if self.app.pargs.module_validation_mode:
            ValidationController.Validation.MODULE_VALIDATION_MODE = \
                self.app.pargs.module_validation_mode

        suite = unittest.TestSuite()
        suite.addTest(self.Validation('test_src_directory'))
        suite.addTest(self.Validation('test_src_checkpoint_directory'))
        suite.addTest(self.Validation('test_src_data_directory'))
        suite.addTest(self.Validation('test_main_file'))
        suite.addTest(self.Validation('test_module_spec_file'))
        suite.addTest(self.Validation('test_requirements_file'))
        suite.addTest(self.Validation('test_signature'))
        suite.addTest(self.Validation('test_yaml'))
        runner = unittest.TextTestRunner()
        runner.run(suite)

        # if self.app.pargs.predict:
        #     print("Recieved option: foo => %s" % self.app.pargs.predict)


    @expose(aliases=['cmd2'], help="more of nothing")
    def command2(self):
        self.app.log.info("Inside MyBaseController.command2()")
        # if self.app.pargs.foo:
        #     print('test')

    class Validation(unittest.TestCase):

        # MODULE_PATH = "/Users/Chun/Documents/workspace/momodel/mo/pyserver/user_directory/zhaofengli/weather_prediction"
        MODULE_PATH = "../"

        MODULE_NAME = {{cookiecutter.module_name}}
        # MODULE_NAME = "weather_prediction"

        MODULE_AUTHOR = {{cookiecutter.module_author}}
        # MODULE_AUTHOR = "zhaofengli"


        MODULE_TYPE = {{cookiecutter.module_type}}
        # MODULE_TYPE = 'model'
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

        # Step 2: main.py
        def test_signature(self):
            with open("{}/src/main.py".format(self.MODULE_PATH), 'r') as f:
                read_data = f.read()

                # Check class name
                with self.subTest(name='class name in main.py'):
                    self.assertIsNotNone(
                        re.search(r'class\s+{}'.format(self.MODULE_NAME),
                                  read_data),
                        msg="class name is not eqaul to {}".format(
                            self.MODULE_NAME))

                if self.MODULE_TYPE == 'model':
                    # Check [def __init__()] section
                    with self.subTest(name="[def __init__()] in main.py"):
                        self.assertIsNotNone(
                            re.search(r'def\s+__init__\(self', read_data),
                            msg="[def __init__()] signature is missing")

                    # Check [def train()] section
                    with self.subTest(name="[def train()] in main.py"):
                        self.assertIsNotNone(
                            re.search(r'def\s+train\(self,\s+input={}', read_data),
                            msg="[def train()] signature is missing")

                    # Check [def predict()] section
                    with self.subTest(name="[def predict()] in main.py"):
                        self.assertIsNotNone(
                            re.search(r'def\s+predict\(self,\s+input={}', read_data),
                            msg="[def predict()] signature is missing")

                    # Check [def load_model()] section
                    with self.subTest(name="[def load_model()] in main.py"):
                        self.assertIsNotNone(
                            re.search(r'def\s+load_model\(self', read_data),
                            msg="[def load_model()] signature is missing")

                elif self.MODULE_TYPE == 'toolkit':
                    # Check [def __init__()] section
                    with self.subTest(name="[def __init__()] in main.py"):
                        self.assertIsNotNone(
                            re.search(r'def\s+__init__\(self', read_data),
                            msg="[def __init__()] signature is missing")

                    # Check [def run()] section
                    with self.subTest(name="[def train()] in main.py"):
                        self.assertIsNotNone(
                            re.search(r'def\s+run\(self,\s+input={}', read_data),
                            msg="[def run()] signature is missing")


        # Step 3: YAML
        def test_yaml(self):
            '''
                To check the content of [module_spec.yaml] file
            :return:
            '''


            # Check yml file can be loaded correctly
            with open("{}/src/module_spec.yml".format(self.MODULE_PATH)) as stream:
                # Load yaml file
                try:
                    yaml_obj = yaml.load(stream)
                except Exception as e:
                    self.fail(msg="yaml cannot be loaded")

                # Check [input] section
                with self.subTest(name="[input] section"):
                    self.assertIsNotNone(
                        yaml_obj.get("input"),
                        msg="[input] section missing in module_spec.yml")

                # Check value_name / value_type / default_value of each parameter
                required_predict_items = {"value_name": "name",
                                          "value_type": "value_type",
                                          "default_value": "default"}

                prefix = ''
                if self.MODULE_TYPE == 'model':
                    prefix = 'predict'
                elif self.MODULE_TYPE == 'toolkit':
                    prefix = 'run'


                # Check [input:predict or input:run] section
                with self.subTest(name="[input:{}] section".format(prefix)):
                    yaml_input = yaml_obj.get("input", {}).get(prefix, None)
                    self.assertIsNotNone(
                        yaml_input,
                        msg="[input/{}] section missing in module_spec.yml".
                            format(prefix))

                input_feed = {}
                for k, v in yaml_input.items():
                    # Check value_name
                    with self.subTest(name="[input:{}:{}]".format(prefix, k)):
                        name = v.get(required_predict_items["value_name"], None)
                        self.assertIsNotNone(
                            name,
                            msg="[{}/name] missing in module_spec.yml".format(
                                k, name))

                    # Check value_type
                    with self.subTest(name="[input:{}:{}]".format(prefix, k)):
                        value_type = v.get(required_predict_items["value_type"],
                                           None)
                        self.assertIsNotNone(
                            value_type,
                            msg="[{}/value_type] missing in module_spec.yml".format(
                                k, value_type))

                    # Check default_value
                    if self.MODULE_VALIDATION_MODE == 'advance':
                        with self.subTest(name="[input:{}:{}]".format(prefix, k)):
                            default_value = v.get(
                                required_predict_items["default_value"], None)
                            self.assertIsNotNone(
                                default_value,
                                msg="[{}/default] missing in module_spec.yml".format(
                                    k, default_value))

                        # Check if type of default_value is matched with value_type
                        with self.subTest(name=
                                          "[input:{}:{}] - "
                                          "Type Checking".format(prefix, k)):
                            assert_result, value = \
                                self.check_value_type(value_type, default_value)
                            self.assertTrue(
                                assert_result,
                                msg="[{}/default] value is not match "
                                    "with [{}/value_type]".format(k, k))

                        input_feed[name] = value

                # print("input_feed", input_feed)

                if input_feed:
                    # Check predict() with default_value of each parameter
                    with self.subTest(name="{}()".format(prefix)):
                        try:
                            module_import_path = \
                                "{}.src.main".format(
                                    self.MODULE_NAME)
                            print("module_import_path", module_import_path)

                            my_module = importlib. \
                                import_module(module_import_path)
                            m = getattr(my_module, self.MODULE_NAME)()

                            if self.MODULE_TYPE == 'model':
                                result = m.predict(input=input_feed)
                            elif self.MODULE_TYPE == 'toolkit':
                                result = m.run(input=input_feed)

                            # print("result", result)
                            # Check result type

                        except Exception as e:
                            self.fail(
                                msg=
                                "{}() cannot be executed correctly - {}".format(
                                    prefix, str(e)))
                else:
                    if self.MODULE_VALIDATION_MODE == 'advance':
                        self.fail(msg="MODULE_INPUT cannot be generated")

        def check_value_type(self, value_type, default_value):
            # available Types: int, str, float, img, datetime, [int], [str], [float]
            check_fucns = {
                "int": self.check_int(default_value),
                "float": self.check_float(default_value),
                "str": self.check_str(default_value),
                "datetime": self.check_datetime(default_value),
                "img": self.check_img(default_value),
                "['int']": self.check_array_int(default_value),
                "[int]": self.check_array_int(default_value),
                "[str]": self.check_array_str(default_value),
                "['str']": self.check_array_str(default_value),
                "[float]": self.check_array_float(default_value),
                "['float']": self.check_array_float(default_value)
            }

            # print('value_type', value_type)
            try:
                return check_fucns[str(value_type)]
            except Exception as e:
                self.fail(msg="[value_type] is not valid")

        @staticmethod
        def check_int(value):
            return type(value) is int, value

        @staticmethod
        def check_float(value):
            return type(value) is float, value

        @staticmethod
        def check_str(value):
            return type(value) is str, value

        @staticmethod
        def check_img(value):
            try:
                base64_data = re.sub('^data:image/.+;base64,', '', value)
                byte_data = base64.b64decode(base64_data)
                image_data = BytesIO(byte_data)
                Image.open(image_data)
                return True, value
            except Exception as e:
                print(str(e))
                return False, None


        @staticmethod
        def check_datetime(value):
            return type(value) is datetime, value

        @staticmethod
        def check_array_int(value):
            if type(value) is list:
                # print("in check_array_int()")
                return all(isinstance(item, int) for item in value), value
            else:
                return False, None

        @staticmethod
        def check_array_str(value):
            if type(value) is list:
                return all(isinstance(item, str) for item in value), value
            else:
                return False, None

        @staticmethod
        def check_array_float(value):
            if type(value) is list:
                return all(isinstance(item, float) for item in value)
            else:
                return False, None

class UtilityController(CementBaseController):

    PROJECT_ID = ""

    class Meta:
        label = 'utility'
        stacked_on = 'base'

    @expose(help='this is some utility command', aliases=['push'])
    def second_cmd1(self):
        self.app.log.info("Inside MySecondController.second_cmd1")


class MyApp(CementApp):
    class Meta:
        label = 'MO_dev_cmd_tool'
        base_controller = 'base'
        handlers = [ValidationController, UtilityController]



with MyApp() as app:
    app.run()
