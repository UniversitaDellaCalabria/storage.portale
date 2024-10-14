from rest_framework.schemas.openapi_agid import AgidAutoSchema


class ApiStudyActivityDetailSchema(AgidAutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        if "studyplans" in path:
            operation["operationId"] = "retrieveCdsStudyPlanActivity"
        else:
            operation["operationId"] = "retrieveStudyActivityInfo"
        return operation
