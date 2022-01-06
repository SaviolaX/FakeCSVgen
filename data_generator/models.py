from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class SchemaStatusChoises:
    READY = "Ready"
    PROCESSING = "Processing"
    FAILED = "Failed"

    CHOICES = (
        (READY, "Ready to download"),
        (PROCESSING, "In progress"),
        (FAILED, "Error"),
    )


class ColumnTypeChoices:
    INT = "integer"
    DATE = "date"
    EMAIL = "email"
    PHONE = "phone"
    JOB = "job"
    NAME = "name"

    CHOICES = (
        (NAME, "Full name"),
        (INT, "Number range"),
        (DATE, "Date time"),
        (EMAIL, "E-mail"),
        (PHONE, "Phone number"),
        (JOB, "Job"),
    )


class Schema(models.Model):
    """Parameters for schema for csv files"""
    name = models.CharField(max_length=255, verbose_name='Name')
    separator = models.CharField(max_length=1,
                                 default=',',
                                 verbose_name='Separator')
    status = models.CharField(choices=SchemaStatusChoises.CHOICES,
                              max_length=255,
                              verbose_name='Status')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             verbose_name='User')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'The schema {} created at {}'.format(self.name, self.created_at)


class SchemaFile(models.Model):
    """Parameters for csv files"""
    file = models.FileField(blank=True, null=True,
                            verbose_name="Files with data")
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,
                               related_name='schema_files')
    status = models.CharField(choices=SchemaStatusChoises.CHOICES,
                              max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-created_at',)


class SchemaColumnModel(models.Model):
    """Parameters and columns for generating csv file"""
    name = models.CharField(max_length=255, verbose_name='Name')
    column_type = models.CharField(choices=ColumnTypeChoices.CHOICES,
                                   max_length=30)
    integer_range_from = models.PositiveSmallIntegerField(null=True,
                                                          blank=True,
                                                          verbose_name='From')
    integer_range_to = models.PositiveSmallIntegerField(null=True,
                                                        blank=True,
                                                        verbose_name='To')
    order = models.PositiveSmallIntegerField(default=1,
                                             validators=[MinValueValidator(1)],
                                             verbose_name='Column order')
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True,
                               blank=True, verbose_name='Schema',
                               related_name='column_in_schemas')

    class Meta:
        verbose_name = "Column in schema"
        verbose_name_plural = "Columns in schema"

    def __str__(self):
        return "Column {} in schema".format(self.name)
