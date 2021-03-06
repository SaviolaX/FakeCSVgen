# Generated by Django 4.0 on 2021-12-24 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemacolumnmodel',
            name='column_type',
            field=models.CharField(choices=[('name', 'Full name'), ('integer', 'Number range'), ('date', 'Date time'), ('email', 'E-mail'), ('phone', 'Phone number'), ('job', 'Job')], max_length=30),
        ),
        migrations.AlterField(
            model_name='schemacolumnmodel',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_generator.schema', verbose_name='column_in_schemas'),
        ),
        migrations.AlterField(
            model_name='schemafile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/', verbose_name='Files with data'),
        ),
    ]
