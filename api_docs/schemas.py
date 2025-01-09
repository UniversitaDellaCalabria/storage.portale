
from drf_spectacular import openapi
from drf_spectacular.types import OPENAPI_TYPE_MAPPING

class AutoSchema(openapi.AutoSchema):
    """
    Custom schema generator that marks all integer fields as `int32`.
    """
    def _map_field(self, field):
        schema = super()._map_field(field)
        if schema.get('type') == 'integer':
            schema['format'] = 'int32'
        return schema