## POSTPROCESSING HOOKS

def set_int_format_to_int32(result, generator, request, public):
    """
    Modify the schema to add a specific format for integer fields.
    """

    def process_schema(schema):
        if isinstance(schema, dict):
            if schema.get("type") == "integer":
                schema["format"] = "int32"
            # Recursively process nested schemas
            for key, value in schema.items():
                if isinstance(value, dict):
                    process_schema(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            process_schema(item)

    process_schema(result)
    return result


def set_servers_from_request(result, generator, request, public):
    if request:
        scheme = request.scheme
        host = request.get_host()
        result['servers'] = [{
            'url': f'{scheme}://{host}',
            'description': 'Current server'
        }]
    return result
