import unittest

from pydantic import ValidationError

from app.api.dto import PropertyDto
from app.api.dto import VertexRequestDto
from app.api.dto.common.propertydto import Datatype


class TestVertexRequestDto(unittest.TestCase):
    def test_with_missing_name(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                position_x=1,
                position_y=1,
                radius=1,
                properties=[]
            )

    def test_with_empty_name(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[]
            )

    def test_with_starting_number_name(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='1name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[]
            )

    def test_with_starting_underscores_name(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='__name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[]
            )

    def test_with_special_character_name(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='a-name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[]
            )

    def test_with_missing_position_x(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_y=1,
                radius=1,
                properties=[]
            )

    def test_with_missing_position_y(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                radius=1,
                properties=[]
            )

    def test_with_missing_radius(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                position_y=1,
                properties=[]
            )

    def test_with_missing_properties(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                position_y=1,
                radius=1
            )

    def test_with_duplicate_property_keys(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[
                    PropertyDto(key='key', required=True, datatype=Datatype.STRING),
                    PropertyDto(key='key', required=False, datatype=Datatype.INT)
                ]
            )

    def test_with_id_in_property_keys(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[
                    PropertyDto(key='id', required=False, datatype=Datatype.INT)
                ]
            )

    def test_with_label_in_property_keys(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[
                    PropertyDto(key='label', required=False, datatype=Datatype.INT)
                ]
            )

    def test_with_property_with_starting_underscores(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[
                    PropertyDto(key='__key', required=False, datatype=Datatype.INT)
                ]
            )

    def test_with_invalid_datatype(self):
        with self.assertRaises(ValidationError):
            VertexRequestDto(
                name='name',
                position_x=1,
                position_y=1,
                radius=1,
                properties=[
                    PropertyDto(key='key', required=False, datatype='ID')
                ]
            )
