from django import forms

from .models import Schema, SchemaColumnModel


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('name', 'separator',)


ColumnFormset = forms.modelformset_factory(
    SchemaColumnModel,
    fields=('name', 'column_type', 'integer_range_from',
            'integer_range_to', 'order'),
    extra=4,
)


class RowsForm(forms.Form):
    rows = forms.IntegerField()
