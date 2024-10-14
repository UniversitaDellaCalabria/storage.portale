from rest_framework.schemas.openapi_agid import AgidAutoSchema


class ApiPersonIdSchema(AgidAutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation["operationId"] = "getPersonId"
        return operation


class ApiDecryptedPersonIdSchema(AgidAutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation["operationId"] = "getDecryptedPersonId"
        return operation
