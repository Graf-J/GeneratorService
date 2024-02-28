import unittest
import uuid

from app.api.dto import ProjectRequestDto, ProjectResponseDto
from app.core.entities import Project
from app.mappers import ProjectMapper


class TestProjectMapperToEntity(unittest.TestCase):
    def test(self):
        # Arrange
        dto = ProjectRequestDto(
            name='TestProject'
        )

        # Act
        entity = ProjectMapper.to_entity(dto)

        # Assert
        self.assertIsInstance(entity, Project)
        self.assertIsInstance(entity.id, str)
        self.assertEqual(entity.name, 'TestProject')


class TestProjectMapperToDto(unittest.TestCase):
    def test(self):
        # Arrange
        project_id = uuid.uuid4()
        entity = Project(
            _id=str(project_id),
            name='TestProject'
        )

        # Act
        dto = ProjectMapper.to_dto(entity)

        # Assert
        self.assertIsInstance(dto, ProjectResponseDto)
        self.assertEqual(dto.id, project_id)
        self.assertEqual(dto.name, 'TestProject')
