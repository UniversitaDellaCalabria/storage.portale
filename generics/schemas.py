from drf_spectacular.openapi import AutoSchema
from drf_spectacular.generators import SchemaGenerator

class AgidAutoSchema(AutoSchema):
    def map_serializer_field(self, field, direction):
        # Get the default mapping for the field
        schema = super().map_serializer_field(field, direction)

        # Add custom formats for IntegerField
        if schema.get('type') == 'integer' and 'format' not in schema:
            schema['format'] = 'int32'  # Set the desired format
        return schema
    
class AgidSchemaGenerator(SchemaGenerator):
    def get_paths(self, request=None):
        paths = super().get_paths(request)
        # Strip prefix logic
        new_paths = {key.replace(r'.*{3}', ''): value for key, value in paths.items()}
        return new_paths
