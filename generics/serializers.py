from rest_framework import serializers


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    """
    A custom serializer that enforces all fields to be read-only.

    This serializer is designed to provide a read-only representation of the model,
    ensuring that no field can be modified during serialization or deserialization.
    It extends the default `ModelSerializer` functionality by overriding the `get_fields`
    method to set the `read_only` attribute for every field dynamically.

    Attributes:
        - Inherits all attributes from `serializers.ModelSerializer`.

    Methods:
        - get_fields(*args, **kwargs):
            Dynamically retrieves all fields and marks them as read-only.

    Example Usage:
        ```
        class ExampleModelSerializer(ReadOnlyModelSerializer):
            class Meta:
                model = ExampleModel
                fields = ['id', 'name', 'created_at']
        ```

        This will ensure that the `id`, `name`, and `created_at` fields are all read-only.
    """

    def get_fields(self, *args, **kwargs):
        """
        Overrides the default `get_fields` method of `ModelSerializer` to mark all
        fields as read-only.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            OrderedDict: A dictionary of fields with their `read_only` attribute set to `True`.

        Example:
            For a model with fields `id`, `name`, and `created_at`, the resulting
            fields dictionary will have all fields marked as read-only:
            {
                'id': Field(read_only=True),
                'name': Field(read_only=True),
                'created_at': Field(read_only=True)
            }
        """
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields
