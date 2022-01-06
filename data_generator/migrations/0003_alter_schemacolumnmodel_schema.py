# Generated by Django 4.0 on 2021-12-24 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0002_alter_schemacolumnmodel_column_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemacolumnmodel',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='column_in_schemas', to='data_generator.schema', verbose_name='Schema'),
        ),
    ]
