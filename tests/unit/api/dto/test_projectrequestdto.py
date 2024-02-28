import unittest

from pydantic import ValidationError

from app.api.dto import ProjectRequestDto


class TestProjectRequestDto(unittest.TestCase):
    def test_missing_name(self):
        with self.assertRaises(ValidationError):
            ProjectRequestDto()

    def test_with_empty_name(self):
        with self.assertRaises(ValidationError):
            ProjectRequestDto(name='')

    def test_with_invalid_character_in_name(self):
        with self.assertRaises(ValidationError):
            ProjectRequestDto(name='Hi/Hello')

    def test_with_underscore_in_name(self):
        with self.assertRaises(ValidationError):
            ProjectRequestDto(name='hello_world')

    def test_with_special_character_in_name(self):
        with self.assertRaises(ValidationError):
            ProjectRequestDto(name='Spaß')
