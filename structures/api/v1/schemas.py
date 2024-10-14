from rest_framework.schemas.openapi_agid import AgidAutoSchema


class StructureDetailSchema(AgidAutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        if "addressbookstructures" in path:
            operation["operationId"] = "retrieveAddressbookStructure"
        else:
            operation["operationId"] = "retrieveStructure"
        return operation
