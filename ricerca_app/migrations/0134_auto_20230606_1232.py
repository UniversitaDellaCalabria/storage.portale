# Generated by Django 3.2.19 on 2023-06-06 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ricerca_app', '0133_auto_20230531_1043'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SitoWebCdsTipologiaArticolo',
        ),
        # migrations.RemoveField(
            # model_name='sitowebcdsarticoliregaltridati',
            # name='stato',
        # ),
        migrations.RemoveField(
            model_name='sitowebcdsarticoliregolamento',
            name='contenuto_en',
        ),
        migrations.RemoveField(
            model_name='sitowebcdsarticoliregolamento',
            name='contenuto_it',
        ),
        migrations.RemoveField(
            model_name='sitowebcdsarticoliregolamento',
            name='stato',
        ),
        migrations.RemoveField(
            model_name='sitowebcdsarticoliregolamento',
            name='titolo_en',
        ),
        migrations.RemoveField(
            model_name='sitowebcdsarticoliregolamento',
            name='titolo_it',
        ),
        # migrations.RemoveField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='aa_regdid_id',
        # ),
        # migrations.RemoveField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='id_classe_oggetto_portale',
        # ),
        # migrations.RemoveField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='id_oggetto_portale',
        # ),
        # migrations.RemoveField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='id_sito_web_cds_articoli_regolamento',
        # ),
        # migrations.RemoveField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='stato',
        # ),
        migrations.RemoveField(
            model_name='sitowebcdstopic',
            name='num_articolo',
        ),
        migrations.RemoveField(
            model_name='sitowebcdstopic',
            name='topic_cod',
        ),
        migrations.RemoveField(
            model_name='sitowebcdstopicarticolireg',
            name='cds_id',
        ),
        migrations.RemoveField(
            model_name='sitowebcdstopicarticolireg',
            name='topic_cod',
        ),
        # migrations.AddField(
            # model_name='sitowebcdsarticoliregaltridati',
            # name='visibile',
            # field=models.IntegerField(db_column='VISIBILE', default=0),
            # preserve_default=False,
        # ),
        migrations.AddField(
            model_name='sitowebcdsarticoliregolamento',
            name='testo_en',
            field=models.TextField(blank=True, db_column='TESTO_EN', null=True),
        ),
        migrations.AddField(
            model_name='sitowebcdsarticoliregolamento',
            name='testo_it',
            field=models.TextField(db_column='TESTO_IT', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitowebcdsarticoliregolamento',
            name='titolo_articolo_en',
            field=models.CharField(blank=True, db_column='TITOLO_ARTICOLO_EN', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='sitowebcdsarticoliregolamento',
            name='titolo_articolo_it',
            field=models.CharField(db_column='TITOLO_ARTICOLO_IT', default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitowebcdsarticoliregolamento',
            name='visibile',
            field=models.IntegerField(db_column='VISIBILE', default=0),
            preserve_default=False,
        ),
        # migrations.AddField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='tipo_dato',
            # field=models.CharField(db_column='TIPO_DATO', default='', max_length=100),
            # preserve_default=False,
        # ),
        # migrations.AddField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='visibile',
            # field=models.IntegerField(db_column='VISIBILE', default=0),
            # preserve_default=False,
        # ),
        migrations.AddField(
            model_name='sitowebcdstopic',
            name='visibile',
            field=models.IntegerField(db_column='VISIBILE', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitowebcdstopicarticolireg',
            name='titolo_en',
            field=models.CharField(blank=True, db_column='TITOLO_EN', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='sitowebcdstopicarticolireg',
            name='titolo_it',
            field=models.CharField(db_column='TITOLO_IT', default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitowebcdstopicarticolireg',
            name='visibile',
            field=models.IntegerField(db_column='VISIBILE', default=0),
            preserve_default=False,
        ),
        # migrations.AlterField(
            # model_name='sitowebcdsarticoliregaltridati',
            # name='id_user_mod',
            # field=models.ForeignKey(db_column='ID_USER_MOD', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.user'),
        # ),
        migrations.AlterField(
            model_name='sitowebcdsarticoliregolamento',
            name='id_user_mod',
            field=models.ForeignKey(db_column='ID_USER_MOD', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.user'),
        ),
        # migrations.AlterField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='id_user_mod',
            # field=models.IntegerField(db_column='ID_USER_MOD'),
        # ),
        # migrations.AlterField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='ordine',
            # field=models.PositiveIntegerField(db_column='ORDINE'),
        # ),
        migrations.AlterField(
            model_name='sitowebcdstopic',
            name='dt_mod',
            field=models.DateField(db_column='DT_MOD'),
        ),
        migrations.AlterField(
            model_name='sitowebcdstopic',
            name='id_user_mod',
            field=models.ForeignKey(db_column='ID_USER_MOD', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.user'),
        ),
        migrations.AlterField(
            model_name='sitowebcdstopicarticolireg',
            name='id_sito_web_cds_articoli_regolamento',
            field=models.ForeignKey(blank=True, db_column='ID_SITO_WEB_CDS_ARTICOLI_REGOLAMENTO', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.sitowebcdsarticoliregolamento'),
        ),
        migrations.AlterField(
            model_name='sitowebcdstopicarticolireg',
            name='id_user_mod',
            field=models.IntegerField(db_column='ID_USER_MOD'),
        ),
        # migrations.AddField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='id_sito_web_cds_oggetti_portale',
            # field=models.ForeignKey(db_column='ID_SITO_WEB_CDS_OGGETTI_PORTALE', default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.sitowebcdsoggettiportale'),
            # preserve_default=False,
        # ),
        # migrations.AddField(
            # model_name='sitowebcdstopicarticolireg',
            # name='id_sito_web_cds_oggetti_portale',
            # field=models.ForeignKey(blank=True, db_column='ID_SITO_WEB_CDS_OGGETTI_PORTALE', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.sitowebcdsoggettiportale'),
        # ),
    ]
