from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from advanced_training.models import (
    AltaFormazioneDatiBase,
    AltaFormazioneConsiglioScientificoInterno,
)
from advanced_training.management.forms import (
    MasterDatiBaseForm,
    IncaricoDidatticoFormSet,
    PianoDidatticoFormSet,
    PartnerFormSet,
    # ConsiglioScientificoEsternoFormSet,
    # ConsiglioScientificoInternoFormSet,
)
from django.contrib import messages
from django.utils import timezone
from generics.utils import encrypt, decrypt, log_action
from generics.forms import ChoosenPersonForm
from addressbook.models import Personale
from django.contrib.admin.models import CHANGE


@login_required
def advancedtraining_masters(request):
    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        "#": _("Advanced Training"),
    }
    context = {
        "breadcrumbs": breadcrumbs,
        "url": reverse("advanced-training:apiv2:advanced-training-list"),
    }
    return render(request, "advanced-training.html", context)


@login_required
def advancedtraining_info_edit(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _(
            "Advanced Training"
        ),
        "#": _("Edit Master"),
    }

    tab_form_dict = {
        "Dati generali": MasterDatiBaseForm(instance=master),
        "Incarichi Didattici": IncaricoDidatticoFormSet(instance=master),
        "Piano Didattico": PianoDidatticoFormSet(instance=master),
        "Partner": PartnerFormSet(instance=master),
        "Consiglio Scientifico Interno": ChoosenPersonForm(),
    }

    internal_council = get_object_or_404(
        AltaFormazioneConsiglioScientificoInterno,
        alta_formazione_dati_base_id=pk,
    )

    initial = {}
    if internal_council.matricola_cons:
        member_mat = internal_council.matricola_cons
        initial = {"choosen_person": encrypt(member_mat.matricola_cons)}
    else:
        initial = {"nome_origine_cons": internal_council.nome_origine_cons}

    internal_form = ChoosenPersonForm(initial=initial, required=True)

    last_viewed_tab = request.GET.get("tab")

    if request.method == "POST":
        form_name = request.POST.get("tab_form_dict_key")
        form = None

        match form_name:
            case "Dati generali":
                form = MasterDatiBaseForm(request.POST, instance=master)
            case "Incarichi Didattici":
                form = IncaricoDidatticoFormSet(request.POST, instance=master)
            case "Piano Didattico":
                form = PianoDidatticoFormSet(request.POST, instance=master)
            case "Partner":
                form = PartnerFormSet(request.POST, instance=master)
            case "Consiglio Scientifico Interno":
                form = internal_form
                
        last_viewed_tab = form_name

        if form and form.is_valid():
            if isinstance(form, (IncaricoDidatticoFormSet, PianoDidatticoFormSet)):
                objs = form.save(commit=False)
                for obj in objs:
                    obj.dt_mod = timezone.now()
                    obj.save()
                form.save_m2m()

                for deleted_obj in form.deleted_objects:
                    deleted_obj.delete()

            else:
                obj = form.save(commit=False)
                obj.dt_mod = timezone.now()
                obj.save()

            messages.success(
                request, f"({form_name}) - Dati master aggiornati con successo"
            )

            return redirect(
                f"{reverse('advanced-training:management:advanced-training-detail', args=[master.id])}?tab={form_name}"
            )
        else:
            if form:
                tab_form_dict[form_name] = form
                if isinstance(form, (IncaricoDidatticoFormSet, PianoDidatticoFormSet)):
                    for subform_errors in form.errors:
                        for field, errors in subform_errors.items():
                            for error in errors:
                                messages.error(request, f"{field}: {error}")
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")

    return render(
        request,
        "advanced-training-info.html",
        {
            "master": master,
            "forms": tab_form_dict,
            "last_viewed_tab": last_viewed_tab,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
def advancedtraining_info_create(request):
    master = AltaFormazioneDatiBase()

    tab_form_dict = {
        "Dati generali": MasterDatiBaseForm(instance=master),
        "Incarichi Didattici": IncaricoDidatticoFormSet(instance=master),
        "Piano Didattico": PianoDidatticoFormSet(instance=master),
        "Partner": PartnerFormSet(instance=master),
        "Consiglio Scientifico Interno": ChoosenPersonForm(),
        # "Consiglio Scientifico Esterno": ConsiglioScientificoEsternoFormSet(
        #     instance=master
        # ),
        # "Consiglio Scientifico Interno": ConsiglioScientificoInternoFormSet(
        #     instance=master
        # ),
    }

    if request.method == "POST":
        form = MasterDatiBaseForm(request.POST, instance=master)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dt_mod = timezone.now()
            obj.save()
            messages.success(request, "Nuovo master creato con successo")
            return redirect(
                reverse(
                    "advanced-training:management:advanced-training-detail",
                    args=[obj.id],
                )
            )
        else:
            tab_form_dict["Dati generali"] = form

    return render(
        request,
        "advanced-training-info.html",
        {
            "master": master,
            "forms": tab_form_dict,
            "last_viewed_tab": "Dati generali",
        },
    )


@login_required
def advancedtraining_info_delete(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    if request.method == "POST":
        master.delete()
        messages.success(request, _("Master eliminato con successo"))
        return redirect("advanced-training:management:advanced-training")

    messages.error(request, _("Richiesta non valida"))
    return redirect("advanced-training:management:advanced-training-detail", pk=pk)


@login_required
def advancedtraining_internal_scientific_council_edit(request, pk):
    internal_council = get_object_or_404(
        AltaFormazioneConsiglioScientificoInterno, alta_formazione_dati_base_id=pk
    )

    member_mat = None
    member_mat_ecode = None
    old_label = None
    initial = {}
    if internal_council.matricola_cons:
        member_mat = internal_council.matricola_cons
        old_label = f"{member_mat.nome_origine_cons}"
        member_mat_ecode = encrypt(member_mat.matricola_cons)
        initial = {"choosen_person": member_mat_ecode}
    else:
        old_label = internal_council.nome_origine_cons
        initial = {"nome_origine_cons": old_label}

    internal_form = ChoosenPersonForm(initial=initial, required=True)

    if request.POST:
        internal_form = ChoosenPersonForm(data=request.POST, required=True)
        if internal_form.is_valid():
            if internal_form.cleaned_data("choosen_person"):
                member_mat = get_object_or_404(
                    Personale,
                    matricola=decrypt(internal_form.cleaned_data["choosen_person"]),
                )
                internal_council.matricola_cons = member_mat
                internal_council.nome_origine_cons = f"{member_mat.nome_origine_cons}"
            else:
                internal_council.matricola_cons = None
                internal_council.nome_origine_cons = request.POST.get(
                    "nome_origine_cons"
                )
        internal_council.dt_mod = timezone.now()
        internal_council.save()

        if old_label != internal_council.nome_origine_cons:
            log_action(
                user=request.user,
                obj=internal_council,
                flag=CHANGE,
                msg=f"Sostituito membro {old_label} con {internal_council.nome_origine_cons}",
            )
        messages.add_message(
            request,
            messages.SUCCESS,
            _("Member of the Internal Scientific Council updated successfully."),
        )

        return redirect(
            reverse(
                "advanced-training:management:advanced-training-detail",
                pk=pk,
            )
        )
    else:
        for k, v in internal_form.errors.items():
            messages.add_message(
                request, messages.ERROR, f"<b>{internal_form.fields[k].label}</b>: {v}"
            )

    breadcrumbs = {
        reverse("generics:dashboard"): _("Dashboard"),
        reverse("advanced-training:management:advanced-training"): _(
            "Advanced Training"
        ),
        "#": _("Edit Master"),
        reverse(
            "advanced-training:management:advancedtraining-scientific-council-edit",
            args=[pk],
        ): _("Edit Internal Scientific Council"),
    }
    return render(
        request,
        "advanced_training_choose_person.html",
        {
            "breadcrumbs": breadcrumbs,
            # ecc...
        },
    )
