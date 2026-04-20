import io
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

from advanced_training.models import AltaFormazioneDatiBase
from advanced_training.management.views import get_current_status, _check_cfu_piano_didattico

# ── palette colori ──────────────────────────────────────────────────────────
PRIMARY = colors.HexColor("#0066cc")
LIGHT_BG = colors.HexColor("#f0f4f8")
ROW_ALT = colors.HexColor("#f8f9fa")
BORDER = colors.HexColor("#dee2e6")
TEXT_MUTED = colors.HexColor("#6c757d")

STATUS_COLORS = {
    "0": colors.HexColor("#6c757d"),  # Bozza       → grigio
    "1": colors.HexColor("#ffc107"),  # In validaz. → giallo
    "2": colors.HexColor("#17a2b8"),  # Da corregg. → azzurro
    "3": colors.HexColor("#28a745"),  # Approvato   → verde
    "4": colors.HexColor("#dc3545"),  # Rifiutato   → rosso
}

_TABLE_MAX_CHARS = 120
_FIELD_MAX_CHARS = 300


def _val(v, max_chars=_FIELD_MAX_CHARS):
    """Restituisce una stringa leggibile o '—' se vuoto."""
    if v is None or v == "":
        return "—"
    if isinstance(v, bool):
        return "Sì" if v else "No"
    s = str(v)
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\u2026", "...")
    s = " ".join(s.split())
    if len(s) > max_chars:
        s = s[:max_chars] + "..."
    return s


def _tval(v):
    return _val(v, max_chars=_TABLE_MAX_CHARS)


def _styles():
    base = getSampleStyleSheet()
    extra = {
        "DocTitle": ParagraphStyle(
            "DocTitle",
            fontSize=20,
            textColor=PRIMARY,
            spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "SectionTitle": ParagraphStyle(
            "SectionTitle",
            fontSize=13,
            textColor=PRIMARY,
            spaceBefore=14,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "FieldLabel": ParagraphStyle(
            "FieldLabel",
            fontSize=8,
            textColor=TEXT_MUTED,
            fontName="Helvetica",
            spaceAfter=1,
        ),
        "FieldValue": ParagraphStyle(
            "FieldValue",
            fontSize=10,
            textColor=colors.black,
            fontName="Helvetica",
            spaceAfter=4,
            wordWrap="LTR",
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            fontSize=9,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            wordWrap="LTR",
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            fontSize=9,
            textColor=colors.black,
            fontName="Helvetica",
            wordWrap="LTR",
            allowWidows=1,
            allowOrphans=1,
        ),
        "StatusBadge": ParagraphStyle(
            "StatusBadge",
            fontSize=10,
            textColor=colors.white,
            fontName="Helvetica-Bold",
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            fontSize=10,
            textColor=TEXT_MUTED,
            spaceAfter=2,
            fontName="Helvetica",
        ),
        "ModuleText": ParagraphStyle(
            "ModuleText",
            fontSize=9,
            textColor=colors.black,
            fontName="Helvetica",
            spaceAfter=6,
            spaceBefore=2,
            wordWrap="LTR",
            leading=11,
        ),
    }
    extra["Normal"] = base["Normal"]
    return extra


def _section_title(title, styles):
    return [
        Spacer(1, 0.3 * cm),
        Paragraph(title, styles["SectionTitle"]),
        HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=6),
    ]


def _field_pair(label, value, styles):
    return [
        Paragraph(label.upper(), styles["FieldLabel"]),
        Paragraph(_val(value), styles["FieldValue"]),
    ]


def _two_col_table(pairs, styles):
    """
    Costruisce una tabella a 2 colonne di coppie (label, valore).
    `pairs` è una lista di tuple (label, value).
    """
    rows = []
    for i in range(0, len(pairs), 2):
        left_label = Paragraph(pairs[i][0].upper(), styles["FieldLabel"])
        left_value = Paragraph(_val(pairs[i][1]), styles["FieldValue"])
        if i + 1 < len(pairs):
            right_label = Paragraph(pairs[i + 1][0].upper(), styles["FieldLabel"])
            right_value = Paragraph(_val(pairs[i + 1][1]), styles["FieldValue"])
        else:
            right_label = Paragraph("", styles["FieldLabel"])
            right_value = Paragraph("", styles["FieldValue"])

        rows.append([[left_label, left_value], [right_label, right_value]])

    data = [[r[0], r[1]] for r in rows]
    t = Table(data, colWidths=["50%", "50%"], splitByRow=1)
    t.canSplit = 1
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("WORDWRAP", (0, 0), (-1, -1), "LTR"),
            ]
        )
    )
    return t


def _generic_table(headers, rows_data, styles, col_widths=None):
    """Tabella generica con intestazione colorata."""
    header_row = [Paragraph(h, styles["TableHeader"]) for h in headers]
    data = [header_row]
    for row in rows_data:
        data.append([Paragraph(_tval(cell), styles["TableCell"]) for cell in row])

    n_cols = len(headers)
    if col_widths is None:
        col_widths = [f"{100 / n_cols:.1f}%"] * n_cols

    t = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    t.canSplit = 1
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("WORDWRAP", (0, 0), (-1, -1), "LTR"),
    ]
    t.setStyle(TableStyle(style))
    return t


def _empty_table_note(text, styles):
    return Paragraph(f"<i>{text}</i>", styles["Subtitle"])


# ── VIEW ────────────────────────────────────────────────────────────────────


@login_required
def advancedtraining_export_pdf(request, pk):
    master = get_object_or_404(AltaFormazioneDatiBase, pk=pk)

    # ── recupera stato corrente ──────────────────────────────────────────
    status = get_current_status(master)
    status_cod = status["cod"]
    status_desc = status["description"]

    # ── setup documento ──────────────────────────────────────────────────
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"Master – {master.titolo_it or 'Scheda'}",
        author="storage.portale.unical.it - Università della Calabria",
        allowSplitting=1,
    )

    styles = _styles()
    story = []

    # ── INTESTAZIONE ─────────────────────────────────────────────────────
    status_color = STATUS_COLORS.get(str(status_cod), TEXT_MUTED)
    badge_text = f'<font color="white"><b> {status_desc} </b></font>'
    badge = Paragraph(badge_text, styles["StatusBadge"])
    badge_cell = Table([[badge]], colWidths=["100%"])
    badge_cell.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), status_color),
                ("ROUNDEDCORNERS", (0, 0), (0, 0), [4, 4, 4, 4]),
                ("LEFTPADDING", (0, 0), (0, 0), 6),
                ("RIGHTPADDING", (0, 0), (0, 0), 6),
                ("TOPPADDING", (0, 0), (0, 0), 2),
                ("BOTTOMPADDING", (0, 0), (0, 0), 2),
            ]
        )
    )

    style_titolo = styles["DocTitle"].clone('DocTitleAuto')
    style_titolo.leading = style_titolo.fontSize * 1.25   # Questo evita l'accavallamento delle righe

    badge_table = Table(
        [
            [
                badge_cell,
            ]
        ],
        colWidths=["100%"],
    )
    badge_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                # Aggiungiamo un padding verticale per dare "aria" al titolo
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(badge_table)

    story.append(
        HRFlowable(
            width="100%", thickness=1, color="#ffffff", spaceBefore=5, spaceAfter=5
        )
    )
    
    header_table = Table(
        [
            [
                Paragraph(master.titolo_it or "Scheda Master", style_titolo),
            ]
        ],
        colWidths=["100%"],
    )
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                # Aggiungiamo un padding verticale per dare "aria" al titolo
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(header_table)

    if master.titolo_en:
        story.append(Paragraph(master.titolo_en, styles["Subtitle"]))

    story.append(
        HRFlowable(
            width="100%", thickness=2, color=PRIMARY, spaceBefore=10, spaceAfter=10
        )
    )

    # ── TAB 1: DATI GENERALI ─────────────────────────────────────────────
    story += _section_title("Dati Generali", styles)
    
    dati_generali = [
        ("Titolo (IT)", master.titolo_it),
        ("Titolo (EN)", master.titolo_en),
        ("Dipartimento", master.dipartimento_riferimento),
        ("Anno Erogazione", getattr(master, "anno_erogazione", None)),
        ("Tipo Master", getattr(master, "alta_formazione_tipo_corso", None)),
        # ~ ("Livello", getattr(master, "livello", None)),
        ("Durata (mesi)", getattr(master, "mesi", None)),
        ("CFU Totali", str(_check_cfu_piano_didattico(master)[1])),
        ("N. Max Iscritti", getattr(master, "num_max_partecipanti", None)),
        ("N. Min Iscritti", getattr(master, "num_min_partecipanti", None)),
        ("Quota Iscrizione", getattr(master, "quota_iscrizione", None)),
        ("Sede", getattr(master, "sede_corso", None)),
    ]
    story.append(_two_col_table(dati_generali, styles))

    # Direttore scientifico
    story += _section_title("Direttore Scientifico", styles)
    ds_nome = master.nome_origine_direttore_scientifico or "—"
    ds_matricola = (
        str(master.matricola_direttore_scientifico)
        if master.matricola_direttore_scientifico
        else "—"
    )
    story.append(
        _two_col_table(
            [
                ("Matricola", ds_matricola),
                ("Nome e Cognome", ds_nome),
            ],
            styles,
        )
    )

    # Proponente
    story += _section_title("Proponente", styles)
    prop_matricola = (
        str(master.matricola_proponente) if master.matricola_proponente else "—"
    )
    prop_nome = master.nome_proponente or "—"
    prop_cognome = master.cognome_proponente or "—"
    story.append(
        _two_col_table(
            [
                ("Matricola", prop_matricola),
                ("Nome", prop_nome),
                ("Cognome", prop_cognome),
                ("", ""),
            ],
            styles,
        )
    )

    # Stato corrente
    story += _section_title("Stato Corrente", styles)
    story.append(
        _two_col_table(
            [
                ("Stato", status_desc),
                ("Data", status.get("data_status") or "—"),
                ("Utente", status.get("utente") or "—"),
                ("Dip. utente", status.get("dipartimento_utente") or "—"),
                ("Dip. master", status.get("dipartimento_master") or "—"),
                ("Motivazione", status.get("motivazione") or "—"),
            ],
            styles,
        )
    )

    # ── TAB 2: INCARICHI DIDATTICI ───────────────────────────────────────
    story += _section_title("Incarichi Didattici", styles)
    incarichi = master.altaformazioneincaricodidattico_set.all().order_by("modulo")
    if incarichi.exists():
        rows = [
            (
                i.modulo,
                i.docente,
                i.qualifica,
                i.ente,
                _val(i.num_ore) + " h",
                i.tipologia,
            )
            for i in incarichi
        ]
        story.append(
            _generic_table(
                ["Modulo", "Docente", "Qualifica", "Ente", "Ore", "Tipologia"],
                rows,
                styles,
                col_widths=["22%", "18%", "15%", "18%", "8%", "19%"],
            )
        )
    else:
        story.append(_empty_table_note("Nessun incarico didattico presente.", styles))

    # ── TAB 3: PIANO DIDATTICO ───────────────────────────────────────────
    story += _section_title("Piano Didattico", styles)
    piano = master.altaformazionepianodidattico_set.all().order_by("modulo")
    if piano.exists():
        for idx, p in enumerate(piano, 1):
            modulo_text = str(p.modulo) if p.modulo else ""
            is_long = len(modulo_text) > 200

            if is_long:
                story.append(Spacer(1, 0.2 * cm))
                story.append(Paragraph(f"<b>Modulo {idx}</b>", styles["FieldValue"]))
                story.append(
                    Paragraph(_val(p.modulo, max_chars=2000), styles["ModuleText"])
                )
                story.append(Spacer(1, 0.15 * cm))

                modulo_data = [
                    ("SSD", p.ssd),
                    ("Ore", _val(p.num_ore) + " h" if p.num_ore else "—"),
                    ("CFU", _val(p.cfu) + " CFU" if p.cfu else "—"),
                    ("Verifica Finale", "Sì" if p.verifica_finale else "No"),
                ]
                story.append(_two_col_table(modulo_data, styles))
            else:
                rows = [
                    [
                        (
                            modulo_text[:120] + "..."
                            if len(modulo_text) > 120
                            else modulo_text
                        ),
                        p.ssd or "—",
                        _val(p.num_ore) + " h" if p.num_ore else "—",
                        _val(p.cfu) + " CFU" if p.cfu else "—",
                        "Sì" if p.verifica_finale else "No",
                    ]
                ]
                story.append(
                    _generic_table(
                        ["Modulo", "SSD", "Ore", "CFU", "Verifica Finale"],
                        rows,
                        styles,
                        col_widths=["32%", "20%", "12%", "12%", "24%"],
                    )
                )
    else:
        story.append(_empty_table_note("Nessun modulo nel piano didattico.", styles))

    # ── TAB 4: PARTNER ───────────────────────────────────────────────────
    story += _section_title("Partner", styles)
    partners = master.altaformazionepartner_set.all().order_by("denominazione")
    if partners.exists():
        rows = [
            (p.denominazione, getattr(p, "tipo", ""), getattr(p, "nazione", ""))
            for p in partners
        ]
        story.append(
            _generic_table(
                ["Denominazione", "Tipo", "Nazione"],
                rows,
                styles,
                col_widths=["50%", "25%", "25%"],
            )
        )
    else:
        story.append(_empty_table_note("Nessun partner presente.", styles))

    # ── TAB 5: CONSIGLIO SCIENTIFICO ESTERNO ─────────────────────────────
    story += _section_title("Consiglio Scientifico Esterno", styles)
    cons_est = master.altaformazioneconsiglioscientificoesterno_set.all().order_by(
        "nome_cons"
    )
    if cons_est.exists():
        rows = [
            (c.nome_cons, getattr(c, "ruolo_cons", ""), getattr(c, "ente_cons", ""))
            for c in cons_est
        ]
        story.append(
            _generic_table(
                ["Nome", "Ruolo", "Ente"],
                rows,
                styles,
                col_widths=["35%", "30%", "35%"],
            )
        )
    else:
        story.append(
            _empty_table_note(
                "Nessun membro del consiglio scientifico esterno.", styles
            )
        )

    # ── TAB 6: CONSIGLIO SCIENTIFICO INTERNO ─────────────────────────────
    story += _section_title("Consiglio Scientifico Interno", styles)
    cons_int = master.altaformazioneconsiglioscientificointerno_set.select_related(
        "matricola_cons"
    ).order_by("nome_origine_cons")
    if cons_int.exists():
        rows = []
        for c in cons_int:
            tipologia = "Personale interno" if c.matricola_cons else "Membro esterno"
            matricola = c.matricola_cons.matricola if c.matricola_cons else "—"
            rows.append((c.nome_origine_cons, tipologia, matricola))
        story.append(
            _generic_table(
                ["Nome e Cognome", "Tipologia", "Matricola"],
                rows,
                styles,
                col_widths=["45%", "35%", "20%"],
            )
        )
    else:
        story.append(
            _empty_table_note(
                "Nessun membro del consiglio scientifico interno.", styles
            )
        )

    # ── piè di pagina personalizzato ─────────────────────────────────────
    def _footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(TEXT_MUTED)
        page_num = f"Pagina {doc.page}"
        canvas.drawRightString(A4[0] - 1.8 * cm, 1.2 * cm, page_num)
        canvas.drawString(
            1.8 * cm, 1.2 * cm, f"Advanced Training – {master.titolo_it or ''}"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)

    buffer.seek(0)
    safe_title = (
        "".join(
            c
            for c in (master.titolo_it or "master")
            if c.isalnum() or c in (" ", "_", "-")
        )
        .strip()
        .replace(" ", "_")[:60]
    )

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="master_{pk}_{safe_title}.pdf"'
    )
    return response
