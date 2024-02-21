import unittest
from unittest.mock import Mock

from app.core.entities import Project
from app.infrastructure.storage import PickleStorage


class TestPickleStorageGetProjects(unittest.TestCase):
    def setUp(self):
        self.filemanager_mock = Mock()

    def test_with_no_project_files(self):
        # Arrange
        self.filemanager_mock.get_project_files.return_value = []
        storage = PickleStorage(self.filemanager_mock)

        # Act
        projects = storage.get_projects()

        # Assert
        self.assertEqual(projects, [])

    def test_with_project_files(self):
        # Arrange
        self.filemanager_mock.get_project_files.return_value = [
            'Project-1_f573eb01-ba2e-4eb4-8530-5412d827b429',
            'Project-2_e657629e-41de-408c-972a-600dac615dbc'
        ]
        storage = PickleStorage(self.filemanager_mock)

        # Act
        projects = storage.get_projects()

        # Assert
        self.assertEqual(len(projects), 2)
        self.assertIsInstance(projects[0], Project)
        self.assertEqual(projects[0].id, 'f573eb01-ba2e-4eb4-8530-5412d827b429')
        self.assertEqual(projects[0].name, 'Project-1')
        self.assertIsInstance(projects[1], Project)
        self.assertEqual(projects[1].id, 'e657629e-41de-408c-972a-600dac615dbc')
        self.assertEqual(projects[1].name, 'Project-2')


class TestPickleStorageGetProject(unittest.TestCase):
    def setUp(self):
        self.filemanager_mock = Mock()

    def test_with_non_existing_project_id(self):
        # Arrange
        self.filemanager_mock.get_project_files.return_value = ['Project-1_f573eb01-ba2e-4eb4-8530-5412d827b429']
        storage = PickleStorage(self.filemanager_mock)

        # Act
        with self.assertRaises(ValueError) as context:
            storage.get_project('non-existing-id')

        # Assert
        self.assertEqual(str(context.exception), 'Project not found')

    def test_with_existing_project_id(self):
        # Arrange
        self.filemanager_mock.get_project_files.return_value = ['Project-1_f573eb01-ba2e-4eb4-8530-5412d827b429']
        storage = PickleStorage(self.filemanager_mock)

        # Act
        project = storage.get_project('f573eb01-ba2e-4eb4-8530-5412d827b429')

        # Assert
        self.assertIsInstance(project, Project)
        self.assertEqual(project.id, 'f573eb01-ba2e-4eb4-8530-5412d827b429')
        self.assertEqual(project.name, 'Project-1')
