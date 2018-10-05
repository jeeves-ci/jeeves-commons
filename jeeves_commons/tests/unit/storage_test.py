import yaml
import json

from base_storage_test import BaseStorageTest

from pkg_resources import resource_filename


class StorageTests(BaseStorageTest):

    def test_create_workflow(self):
        workflow_yaml = resource_filename('jeeves_commons.tests.resources',
                                          'jeeves_workflow.yaml')
        with open(workflow_yaml, 'r') as workflow_stream:
            workflow = yaml.load(workflow_stream)
        # create a workflow
        wf = self.storage.workflows.create(name='test_workflow',
                                           tenant_id=1,
                                           content=json.dumps(workflow),
                                           env=json.dumps({'ENV_VAR': 'var'}))
        # assert field values
        created = self.storage.workflows.get(name='test_workflow')
        self.assertEquals(created.workflow_id, wf.workflow_id)
        self.assertEquals(created.content, json.dumps(workflow))
