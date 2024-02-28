import unittest

from app.api.dto import BuildRequestDto
from app.core.entities import Build
from app.mappers import BuildMapper


class TestBuildMapperToEntity(unittest.TestCase):
    def test_without_volume(self):
        # Arrange
        dto = BuildRequestDto(
            port=3000
        )

        # Act
        entity = BuildMapper.to_entity(dto)

        # Assert
        self.assertIsInstance(entity, Build)
        self.assertEqual(entity.port, 3000)
        self.assertEqual(entity.volume, None)

    def test_with_volume(self):
        # Arrange
        dto = BuildRequestDto(
            port=3000,
            volume='volume'
        )

        # Act
        entity = BuildMapper.to_entity(dto)

        # Assert
        self.assertIsInstance(entity, Build)
        self.assertEqual(entity.port, 3000)
        self.assertEqual(entity.volume, 'volume')
