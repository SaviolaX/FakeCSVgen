import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required

from .models import Schema, SchemaColumnModel
from .forms import SchemaForm, ColumnFormset, RowsForm
from .tasks import create_csv_file


@login_required
def list_all_schemas(request):
    """Display all schemas belong to current user"""
    user = User.objects.get(id=request.user.id)
    all_schemas = Schema.objects.filter(user=user)

    context = {"schemas": all_schemas}
    return render(request, 'data_generator/list_all_schemas.html', context)


@login_required
def create_schema(request):
    """Create schema instance with chosen columns"""
    user = User.objects.get(id=request.user.id)
    schema_form = SchemaForm(request.GET or None)
    formset = ColumnFormset(queryset=SchemaColumnModel.objects.none())

    if request.method == 'POST':
        schema_form = SchemaForm(request.POST)
        formset = ColumnFormset(request.POST)
        if schema_form.is_valid() and formset.is_valid():
            schema = schema_form.save(commit=False)
            schema.user = user
            schema = schema_form.save()

            for form in formset:
                column = form.save(commit=False)
                column.schema = schema
                column.save()
            return redirect('data_generator:schemas')
        else:
            return HttpResponse(
                'Some of your fields filled incorrect. Try again.')

    context = {'schema_form': schema_form, 'formset': formset}
    return render(request, 'data_generator/create_schema.html', context)


@login_required
def edit_schema(request, id):
    """Edit schema instance"""
    schema = Schema.objects.get(id=id)
    schema_form = SchemaForm(instance=schema)
    Formset = forms.modelformset_factory(SchemaColumnModel,
                                         extra=0,
                                         fields=[
                                             'id',
                                             'name',
                                             'column_type',
                                             'integer_range_from',
                                             'integer_range_to',
                                             'order'
                                         ])
    formset = Formset(
        initial=[{"id": x.id} for x in schema.column_in_schemas.all()],
        queryset=SchemaColumnModel.objects.filter(schema_id=id))

    if request.method == 'POST':
        schema_form = SchemaForm(request.POST, instance=schema)
        formset = ColumnFormset(request.POST, initial=[
                                x for x in schema.column_in_schemas.all()])
        if schema_form.is_valid() and formset.is_valid():
            schema = schema_form.save()
            formset.save()
            return redirect('data_generator:schemas')
        else:
            return HttpResponse(
                'Some of your fields filled incorrect. Try again.')

    context = {'schema_form': schema_form, 'formset': formset}
    return render(request, 'data_generator/edit_schema.html', context)


@login_required
def delete_schema(request, id):
    """Delete schema instance with all columns"""
    schema = Schema.objects.get(id=id)
    schema.delete()
    return redirect('data_generator:schemas')


@login_required
def schema_view(request, id):
    """Display a list of created csv files and their status"""
    schema = Schema.objects.get(id=id)
    form = RowsForm(request.POST or None)

    if request.method == 'POST':
        rows = int(request.POST.get('rows'))

        generating_task = create_csv_file.delay(schema.id, rows)

        task_id = generating_task.task_id

        context = {'schema': schema, 'form': form, 'task_id': task_id}
        return render(request, 'data_generator/schema_view.html', context)
    else:
        form = RowsForm()
    context = {'schema': schema, 'form': form}
    return render(request, 'data_generator/schema_view.html', context)


@login_required
def delete_csv_file(request, schema_id, file_id):
    """Delete created csv file from db and local storage"""
    schema = Schema.objects.get(id=schema_id)
    file = schema.schema_files.get(id=file_id)
    try:
        path_to_csv_file = settings.MEDIA_ROOT + str(file.file)
        os.remove(path_to_csv_file)
    except:
        pass

    file.delete()
    return redirect('data_generator:schema_view', schema.id)
