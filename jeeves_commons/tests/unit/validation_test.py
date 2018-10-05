import unittest
import yaml

from jeeves_commons.dsl.validate import validate_workflow, ValidationError

from pkg_resources import resource_filename


class ValidationTests(unittest.TestCase):

    def setUp(self):
        workflow_yaml = resource_filename('jeeves_commons.tests.resources',
                                          'jeeves_workflow.yaml')
        with open(workflow_yaml, 'r') as workflow_stream:
            self.workflow = yaml.load(workflow_stream)

    def test_valid_workflow(self):
        validate_workflow(self.workflow)

    def test_cyclic_dependencies(self):
        self.workflow['install']['dependencies'] = ['publish']
        self.workflow['publish']['dependencies'] = ['install']
        self.assertRaises(ValidationError, validate_workflow, self.workflow)

    def test_task_execution_env(self):
        # remove {'image': centos:latest} from task
        self.workflow['install']['env'] = {}
        self.assertRaises(ValidationError, validate_workflow, self.workflow)

    def test_no_script(self):
        # remove 'script' from task
        self.workflow['install']['script'] = ''
        self.assertRaises(ValidationError, validate_workflow, self.workflow)
