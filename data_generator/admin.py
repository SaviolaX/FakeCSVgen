from django.contrib import admin

from .models import Schema, SchemaColumnModel, SchemaFile


class ColumnInLine(admin.StackedInline):
    model = SchemaColumnModel


class FileInLine(admin.TabularInline):
    model = SchemaFile


@admin.register(SchemaFile)
class FileInSchemaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "file", "status"]


@admin.register(SchemaColumnModel)
class ColumnInSchemaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "column_type", "schema"]


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    inlines = [ColumnInLine, FileInLine]
    list_display = ["__str__", "status", "created_at"]
