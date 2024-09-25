from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from locks.concurrency import LOCK_MESSAGE, acquire_lock, get_lock_from_cache
from locks.exceptions import LockCannotBeAcquiredException
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LockView(APIView):
    description = ""
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    schema = None

    def get(self, request, *args, **kwargs):
        content_type_id = self.kwargs["content_type_id"]
        object_id = self.kwargs["object_id"]
        lock = get_lock_from_cache(content_type_id, object_id)
        if lock[0] and not lock[0] == request.user.pk:  # pragma: no cover
            owner_user = get_user_model().objects.filter(pk=lock[0]).first()
            return Response(
                {
                    "lock": lock,
                    "message": LOCK_MESSAGE.format(user=owner_user, ttl=lock[1]),
                }
            )
        return Response({})


class LockSetView(APIView):
    description = ""
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    schema = None

    def post(self, request, *args, **kwargs):
        content_type_id = request.data.get("content_type_id", None)
        object_id = request.data.get("object_id", None)

        if not all([content_type_id, object_id]):
            raise Http404

        ct = get_object_or_404(ContentType, pk=content_type_id)
        obj = get_object_or_404(ct.model_class(), pk=object_id)

        try:
            permissions_and_offices = obj.get_user_permissions_and_offices(request.user)
            if not permissions_and_offices["permissions"]["lock"]:
                raise PermissionDenied()

            acquire_lock(
                user_id=request.user.pk,
                content_type_id=content_type_id,
                object_id=object_id,
            )
            return Response({"message": _("Lock successfully set")})

        except AttributeError:
            raise PermissionDenied()

        except LockCannotBeAcquiredException as lock_exception:
            return Response(
                {
                    "lock": lock_exception.lock,
                    "message": LOCK_MESSAGE.format(
                        user=get_user_model()
                        .objects.filter(pk=lock_exception.lock[0])
                        .first(),
                        ttl=lock_exception.lock[1],
                    ),
                }
            )
