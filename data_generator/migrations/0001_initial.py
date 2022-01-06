# Generated by Django 4.0 on 2021-12-24 13:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('separator', models.CharField(default=',', max_length=1, verbose_name='Separator')),
                ('status', models.CharField(choices=[('Ready', 'Ready to download'), ('Processing', 'In progress'), ('Failed', 'Error')], max_length=255, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='User')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='SchemaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='media/', verbose_name='File with data')),
                ('status', models.CharField(blank=True, choices=[('Ready', 'Ready to download'), ('Processing', 'In progress'), ('Failed', 'Error')], max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_generator.schema')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='SchemaColumnModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('column_type', models.CharField(choices=[('integer', 'Number range'), ('date', 'Date time'), ('email', 'E-mail'), ('phone', 'Phone number'), ('job', 'Job')], max_length=30)),
                ('integer_range_from', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='From')),
                ('integer_range_to', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='To')),
                ('order', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Column order')),
                ('schema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_generator.schema', verbose_name='Column in schemas')),
            ],
            options={
                'verbose_name': 'Column in schema',
                'verbose_name_plural': 'Columns in schema',
            },
        ),
    ]