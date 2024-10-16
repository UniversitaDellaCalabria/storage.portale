from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext as _

from .forms import UserDataForm
from .jwts import encrypt_to_jwe, decrypt_from_jwe
from .settings import EDITABLE_FIELDS, MSG_FOOTER, MSG_HEADER, CHANGE_EMAIL_TOKEN_LIFE


@login_required
def account(request):
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Account"),
    }
    template = "account.html"
    context = {"breadcrumbs": breadcrumbs}
    return render(request, template, context)


@login_required
def changeData(request):
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("accounts:account"): _("Account"),
        "#": _("Edit"),
    }
    initial = {}
    for field in EDITABLE_FIELDS:
        initial[field] = getattr(request.user, field)
    form = UserDataForm(initial=initial)
    template = "change_user_data.html"
    user = request.user
    user_email = user.email

    if request.POST:
        form = UserDataForm(request.POST, instance=user)
        if form.is_valid():
            email = form.cleaned_data.pop("email", "")
            if len(form.cleaned_data) > 1:
                user = form.save(commit=False)
                user.manual_user_update = timezone.now()
                user.save()
                messages.add_message(
                    request, messages.SUCCESS, _("Data saved successfully")
                )

            if "email" in EDITABLE_FIELDS and email != user_email:
                base_url = request.build_absolute_uri(reverse("accounts:confirm_email"))
                token = f"{request.user.id}|{email}|{timezone.now()}"
                encrypted_data = encrypt_to_jwe(token)
                url = f"{base_url}?token={encrypted_data}"
                body = _("Confirm your email by clicking here {}").format(url)
                msg_body = f"{MSG_HEADER.format(hostname=settings.DEFAULT_HOST)}{body}{MSG_FOOTER}"
                send_mail(
                    subject=_("Email confirmation"),
                    message=msg_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
                messages.add_message(
                    request,
                    messages.INFO,
                    _(
                        "An email has been sent to the address you indicated. Click on the link in the message to confirm the new data"
                    ),
                )
            return redirect("accounts:change_data")
        else:
            messages.add_message(request, messages.ERROR, _("Wrong data"))

    context = {
        "form": form,
        "title": _("Edit personal data"),
        "breadcrumbs": breadcrumbs,
    }
    return render(request, template, context)


@login_required
def confirmEmail(request):
    token = request.GET.get("token")
    if not token:
        messages.add_message(request, messages.ERROR, _("Missing token"))
        return redirect("accounts:change_data")

    try:
        data = decrypt_from_jwe(token).decode()
        items = data.split("|")
    except Exception:
        messages.add_message(request, messages.ERROR, _("Invalid token"))
        return redirect("accounts:change_data")

    user_id = items[0]
    email = items[1]
    timestamp = items[2]

    user = get_object_or_404(get_user_model(), pk=user_id)
    token_date = parse_datetime(timestamp)
    time_diff = timezone.now() - token_date

    token_life_expired = time_diff.total_seconds() / 60 > CHANGE_EMAIL_TOKEN_LIFE
    token_invalid = user.manual_user_update and token_date < user.manual_user_update

    if token_life_expired or token_invalid:
        messages.add_message(request, messages.ERROR, _("Expired token"))
        return redirect("accounts:change_data")

    user.email = email
    user.manual_user_update = timezone.now()
    user.save(update_fields=["email", "manual_user_update"])
    messages.add_message(request, messages.SUCCESS, _("Email updated successfully"))
    return redirect("accounts:account")
