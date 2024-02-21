import unittest
from unittest.mock import Mock

from app.core.entities import Project
from app.core.exceptions import ProjectException
from app.core.repositories import ProjectRepository


class TestProjectRepositoryCreateProject(unittest.TestCase):
    def setUp(self):
        self.storage_mock = Mock()

    def test_with_duplicate_project(self):
        # Arrange
        project = Project(_id='3', name='Project-1')
        self.storage_mock.get_projects.return_value = [
            Project(_id='1', name='Project-1'),
            Project(_id='2', name='Project-2')
        ]
        repository = ProjectRepository(self.storage_mock)

        # Act
        with self.assertRaises(ProjectException) as context:
            repository.create_project(project)

        # Assert
        self.assertEqual(context.exception.message, "Project 'Project-1' already exists")
        self.assertEqual(self.storage_mock.create_project.call_count, 0)

    def test_with_no_existing_project(self):
        # Arrange
        project = Project(_id='3', name='Project-1')
        self.storage_mock.get_projects.return_value = []
        repository = ProjectRepository(self.storage_mock)

        # Act
        repository.create_project(project)

        # Assert
        self.assertEqual(self.storage_mock.create_project.call_count, 1)

    def test_with_no_duplicate_project(self):
        # Arrange
        project = Project(_id='3', name='New-Project')
        self.storage_mock.get_projects.return_value = [
            Project(_id='1', name='Project-1'),
            Project(_id='2', name='Project-2')
        ]
        repository = ProjectRepository(self.storage_mock)

        # Act
        repository.create_project(project)

        # Assert
        self.assertEqual(self.storage_mock.create_project.call_count, 1)
