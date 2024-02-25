import unittest

from app.core.entities import Property
from app.core.entities.property import Datatype


class TestPropertyToDict(unittest.TestCase):
    def test(self):
        # Arrange
        prop = Property(key='name', required=True, datatype=Datatype.STRING)

        # Act
        prop_dict = prop.to_dict()

        # Assert
        self.assertEqual(prop_dict, {'field_name': 'name'})
