import unittest
import uuid

from pydantic import ValidationError

from app.api.dto import EdgeRequestDto
from app.api.dto import PropertyDto
from app.api.dto.common.propertydto import Datatype


class TestEdgeRequestDto(unittest.TestCase):
    def test_with_missing_name(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                properties=[],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_empty_name(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='',
                properties=[],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_starting_number_name(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='1name',
                properties=[],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_starting_underscores_name(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='__name',
                properties=[],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_special_character_name(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='a-name',
                properties=[],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_missing_properties(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_duplicate_property_keys(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                properties=[
                    PropertyDto(key='key', required=True, datatype=Datatype.STRING),
                    PropertyDto(key='key', required=False, datatype=Datatype.INT)
                ],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_id_in_property_keys(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                properties=[
                    PropertyDto(key='id', required=False, datatype=Datatype.INT)
                ],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_label_in_property_keys(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                properties=[
                    PropertyDto(key='label', required=False, datatype=Datatype.INT)
                ],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_property_with_starting_underscores(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                properties=[
                    PropertyDto(key='__key', required=False, datatype=Datatype.INT)
                ],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_invalid_datatype(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                properties=[
                    PropertyDto(key='key', required=False, datatype='ID')
                ],
                source_vertex_id=uuid.uuid4(),
                target_vertex_id=uuid.uuid4()
            )

    def test_with_missing_source_vertex_id(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                properties=[],
                target_vertex_id=uuid.uuid4()
            )

    def test_with_missing_target_vertex_id(self):
        with self.assertRaises(ValidationError):
            EdgeRequestDto(
                name='name',
                properties=[],
                source_vertex_id=uuid.uuid4()
            )
