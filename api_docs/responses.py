from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from generics.serializers import GenericErrorSerializer
from rest_framework import status


def COMMON_LIST_RESPONSES(serializer=None, include_bad_request=True):
    """
    Returns a dictionary of common responses for list methods
    """
    return (
        RESPONSE_HTTP_200_OK(serializer) | RESPONSE_HTTP_400_BAD_REQUEST
        if include_bad_request
        else RESPONSE_HTTP_200_OK(serializer)
    )


def COMMON_RETRIEVE_RESPONSES(serializer=None):
    """
    Returns a dictionary of common responses for retrieve methods
    """
    return (
        RESPONSE_HTTP_200_OK(serializer)
        | RESPONSE_HTTP_400_BAD_REQUEST
        | RESPONSE_HTTP_404_NOT_FOUND
    )


def RESPONSE_HTTP_200_OK(serializer=None):
    return {
        status.HTTP_200_OK: OpenApiResponse(
            response=serializer or None,
            description="Success",
        ),
    }


RESPONSE_HTTP_400_BAD_REQUEST = {
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        description="Bad Request",
        response=GenericErrorSerializer,
        examples=[
            OpenApiExample(
                name="Bad Request",
                value={"detail": "Invalid input."},
            )
        ],
    )
}
RESPONSE_HTTP_401_UNAUTHORIZED = {
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        description="Unauthorized",
        response=GenericErrorSerializer,
        examples=[
            OpenApiExample(
                name="Unauthorized",
                value={
                    "detail": "Authentication credentials were not provided or are invalid."
                },
            )
        ],
    )
}
RESPONSE_HTTP_403_FORBIDDEN = {
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        description="Forbidden",
        response=GenericErrorSerializer,
        examples=[
            OpenApiExample(
                name="Forbidden",
                value={"detail": "You do not have permission to perform this action."},
            )
        ],
    )
}
RESPONSE_HTTP_404_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: OpenApiResponse(
        description="Not Found",
        response=GenericErrorSerializer,
        examples=[
            OpenApiExample(
                name="Not Found",
                value={"detail": "The requested resource was not found."},
            )
        ],
    )
}
RESPONSE_HTTP_500_INTERNAL_SERVER_ERROR = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        description="Internal Server Error",
        response=GenericErrorSerializer,
        examples=[
            OpenApiExample(
                name="Internal Server Error",
                value={"detail": "An unexpected error occurred on the server."},
            )
        ],
    )
}
