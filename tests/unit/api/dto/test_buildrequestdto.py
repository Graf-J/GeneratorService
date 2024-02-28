import unittest

from pydantic import ValidationError

from app.api.dto import BuildRequestDto


class TestBuildRequestDto(unittest.TestCase):
    def test_with_missing_port(self):
        with self.assertRaises(ValidationError):
            BuildRequestDto(
                volume='volume'
            )

    def test_with_empty_volume(self):
        with self.assertRaises(ValidationError):
            BuildRequestDto(
                port=3000,
                volume=''
            )

    def test_with_missing_volume(self):
        dto = BuildRequestDto(
            port=3000
        )
        self.assertEqual(dto.volume, None)

    def test_with_negative_port(self):
        with self.assertRaises(ValidationError):
            BuildRequestDto(
                port=-1
            )

    def test_with_too_big_port(self):
        with self.assertRaises(ValidationError):
            BuildRequestDto(
                port=65536
            )

    def test_with_non_alphanumeric_volume(self):
        with self.assertRaises(ValidationError):
            BuildRequestDto(
                volume='asdf?1'
            )
