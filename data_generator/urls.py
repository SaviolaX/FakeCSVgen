from django.urls import path, include

from . import views

app_name = 'data_generator'

urlpatterns = [
    path('', views.list_all_schemas, name='schemas'),

    path('', include('django.contrib.auth.urls')),

    path('create_schema/', views.create_schema, name='create_schema'),
    path('delete_schema/<int:id>/', views.delete_schema, name='delete_schema'),
    path('edit_schema/<int:id>/', views.edit_schema, name='edit_schema'),
    path('view_schema/<int:id>/', views.schema_view, name='schema_view'),

    path('view_schema/<int:schema_id>/delete_file/<int:file_id>/',
         views.delete_csv_file, name='delete_csv'),

]
