from gremlin_python.structure.io import graphsonV3d0
from gremlin_python.structure.io.util import HashableDict


# Define Custom Objectify Method which convertes "true" and "false" into Boolean types
def custom_maptype_objectify(cls, l, reader):
    new_dict = {}
    if len(l) > 0:
        x = 0
        while x < len(l):
            value = l[x + 1]
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            new_dict[HashableDict.of(reader.to_object(l[x]))] = reader.to_object(value)
            x = x + 2
    return new_dict

# Overwrite Function Pointer to Custom Method
graphsonV3d0.MapType.objectify = classmethod(custom_maptype_objectify)

# Define custom Deserializer for Edge-ID
class RelationIdentifierJanusDeserializer(graphsonV3d0._GraphSONTypeIO):
    graphson_type = "janusgraph:RelationIdentifier"

    @classmethod
    def objectify(cls, d, reader):
        return d['relationId']

# Add custom Deserializer for Edge-ID
graphsonV3d0._deserializers['janusgraph:RelationIdentifier'] = RelationIdentifierJanusDeserializer