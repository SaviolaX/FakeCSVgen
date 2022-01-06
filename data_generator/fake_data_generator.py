import random

from faker import Faker

from data_generator.models import SchemaColumnModel, ColumnTypeChoices


fake = Faker()


def random_int_data(column):
    """Return random number between 2 got numbers"""
    return(
        str(random.randint(column.integer_range_from, column.integer_range_to))
    )


def generate_csv_data(column_id):
    """Generates random data depends wich field was chosen"""

    column = SchemaColumnModel.objects.get(id=column_id)

    if column.column_type == ColumnTypeChoices.INT:
        return random_int_data(column)
    elif column.column_type == ColumnTypeChoices.DATE:
        return fake.date()
    elif column.column_type == ColumnTypeChoices.JOB:
        return fake.job()
    elif column.column_type == ColumnTypeChoices.EMAIL:
        return fake.email()
    elif column.column_type == ColumnTypeChoices.PHONE:
        return fake.phone_number()
    elif column.column_type == ColumnTypeChoices.NAME:
        return fake.name()
    else:
        return "Unsupported data type"
