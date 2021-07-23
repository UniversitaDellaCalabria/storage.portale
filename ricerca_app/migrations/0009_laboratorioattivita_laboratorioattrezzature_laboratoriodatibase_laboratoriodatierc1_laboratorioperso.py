# Generated by Django 3.2 on 2021-07-19 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0008_alter_unitaorganizzativacontatti_id_ab'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaboratorioDatiBase',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('dt_sottomissione', models.DateTimeField(blank=True, db_column='DT_SOTTOMISSIONE', null=True)),
                ('referente_compilazione', models.CharField(blank=True, db_column='REFERENTE_COMPILAZIONE', max_length=200, null=True)),
                ('matricola_referente_compilazione', models.CharField(blank=True, db_column='MATRICOLA_REFERENTE_COMPILAZIONE', max_length=20, null=True)),
                ('email_compilazione', models.CharField(blank=True, db_column='EMAIL_COMPILAZIONE', max_length=200, null=True)),
                ('nome_laboratorio', models.CharField(blank=True, db_column='NOME_LABORATORIO', max_length=400, null=True)),
                ('acronimo', models.CharField(blank=True, db_column='ACRONIMO', max_length=100, null=True)),
                ('logo_laboratorio', models.CharField(blank=True, db_column='LOGO_LABORATORIO', max_length=400, null=True)),
                ('dipartimento_riferimento', models.CharField(blank=True, db_column='DIPARTIMENTO_RIFERIMENTO', max_length=400, null=True)),
                ('id_dipartimento_riferimento', models.IntegerField(blank=True, db_column='ID_DIPARTIMENTO_RIFERIMENTO', null=True)),
                ('laboratorio_interdipartimentale', models.CharField(blank=True, db_column='LABORATORIO_INTERDIPARTIMENTALE', max_length=400, null=True)),
                ('infrastruttura_riferimento', models.CharField(blank=True, db_column='INFRASTRUTTURA_RIFERIMENTO', max_length=400, null=True)),
                ('altre_strutture_riferimento', models.CharField(blank=True, db_column='ALTRE_STRUTTURE_RIFERIMENTO', max_length=400, null=True)),
                ('descr_altre_strutture_riferimento_it', models.TextField(blank=True, db_column='DESCR_ALTRE_STRUTTURE_RIFERIMENTO_IT', null=True)),
                ('descr_altre_strutture_riferimento_en', models.TextField(blank=True, db_column='DESCR_ALTRE_STRUTTURE_RIFERIMENTO_EN', null=True)),
                ('ambito', models.CharField(blank=True, db_column='AMBITO', max_length=100, null=True)),
                ('finalita_ricerca_it', models.TextField(blank=True, db_column='FINALITA_RICERCA_IT', null=True)),
                ('finalita_ricerca_en', models.TextField(blank=True, db_column='FINALITA_RICERCA_EN', null=True)),
                ('finalita_didattica_it', models.TextField(blank=True, db_column='FINALITA_DIDATTICA_IT', null=True)),
                ('finalita_didattica_en', models.TextField(blank=True, db_column='FINALITA_DIDATTICA_EN', null=True)),
                ('finalita_servizi_it', models.TextField(blank=True, db_column='FINALITA_SERVIZI_IT', null=True)),
                ('finalita_servizi_en', models.TextField(blank=True, db_column='FINALITA_SERVIZI_EN', null=True)),
                ('responsabile_scientifico', models.CharField(blank=True, db_column='RESPONSABILE_SCIENTIFICO', max_length=200, null=True)),
                ('matricola_responsabile_scientifico', models.CharField(blank=True, db_column='MATRICOLA_RESPONSABILE_SCIENTIFICO', max_length=20, null=True)),
                ('sede_dimensione', models.CharField(blank=True, db_column='SEDE_DIMENSIONE', max_length=100, null=True)),
                ('sede_note_descrittive', models.TextField(blank=True, db_column='SEDE_NOTE_DESCRITTIVE', null=True)),
                ('strumentazione_descrizione', models.TextField(blank=True, db_column='STRUMENTAZIONE_DESCRIZIONE', null=True)),
                ('strumentazione_valore', models.CharField(blank=True, db_column='STRUMENTAZIONE_VALORE', max_length=100, null=True)),
                ('preposto_sicurezza', models.CharField(blank=True, db_column='PREPOSTO_SICUREZZA', max_length=200, null=True)),
                ('matricola_preposto_sicurezza', models.CharField(blank=True, db_column='MATRICOLA_PREPOSTO_SICUREZZA', max_length=20, null=True)),
            ],
            options={
                'db_table': 'LABORATORIO_DATI_BASE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioUbicazione',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('edificio', models.CharField(blank=True, db_column='EDIFICIO', max_length=200, null=True)),
                ('piano', models.CharField(blank=True, db_column='PIANO', max_length=100, null=True)),
                ('sede_principale', models.CharField(blank=True, db_column='SEDE_PRINCIPALE', max_length=10, null=True)),
                ('note', models.TextField(blank=True, db_column='NOTE', null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_UBICAZIONE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioServiziOfferti',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome_servizio', models.TextField(blank=True, db_column='NOME_SERVIZIO', null=True)),
                ('descrizione_servizio', models.TextField(blank=True, db_column='DESCRIZIONE_SERVIZIO', null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_SERVIZI_OFFERTI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioServiziErogati',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descrizione', models.TextField(blank=True, null=True)),
                ('matricola_responsabile', models.CharField(blank=True, max_length=20, null=True)),
                ('responsabile_origine', models.CharField(blank=True, max_length=500, null=True)),
                ('committenti', models.CharField(blank=True, max_length=500, null=True)),
                ('anno', models.IntegerField(blank=True, null=True)),
                ('durata_mesi', models.IntegerField(blank=True, null=True)),
                ('importo_euro', models.FloatField(blank=True, null=True)),
                ('strumentazione', models.TextField(blank=True, null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_SERVIZI_EROGATI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioPersonaleTecnico',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('matricola_personale_tecnico', models.CharField(blank=True, db_column='MATRICOLA_PERSONALE_TECNICO', max_length=20, null=True)),
                ('ruolo', models.CharField(blank=True, db_column='RUOLO', max_length=400, null=True)),
                ('field_impegno', models.FloatField(blank=True, db_column='%IMPEGNO', null=True)),
                ('cognomenome_origine', models.CharField(blank=True, db_column='COGNOMENOME_ORIGINE', max_length=200, null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_PERSONALE_TECNICO',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioPersonaleRicerca',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('matricola_personale_ricerca', models.CharField(blank=True, db_column='MATRICOLA_PERSONALE_RICERCA', max_length=20, null=True)),
                ('cognomenome_origine', models.CharField(blank=True, db_column='COGNOMENOME_ORIGINE', max_length=200, null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_PERSONALE_RICERCA',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioDatiErc1',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.laboratoriodatibase')),
                ('id_ricerca_erc1', models.ForeignKey(blank=True, db_column='ID_RICERCA_ERC1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.ricercaerc1')),
            ],
            options={
                'db_table': 'LABORATORIO_DATI_ERC1',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioAttrezzature',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('tipologia', models.CharField(blank=True, max_length=500, null=True)),
                ('descrizione', models.TextField(blank=True, null=True)),
                ('fondi', models.CharField(blank=True, max_length=500, null=True)),
                ('costo_unitario', models.FloatField(blank=True, null=True)),
                ('quantita', models.IntegerField(blank=True, null=True)),
                ('tipo_rischi', models.CharField(blank=True, max_length=500, null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_ATTREZZATURE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LaboratorioAttivita',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('tipologia_attivita', models.CharField(blank=True, db_column='TIPOLOGIA_ATTIVITA', max_length=200, null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.ricercadocentelineabase')),
            ],
            options={
                'db_table': 'LABORATORIO_ATTIVITA',
                'managed': True,
            },
        ),
    ]