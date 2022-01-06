import random
import csv
import time
from django.core.files.storage import default_storage

from celery_progress.backend import ProgressRecorder

from .models import Schema, SchemaStatusChoises, SchemaFile
from .fake_data_generator import generate_csv_data
from core.celery import app


@app.task(bind=True)
def create_csv_file(self, schema_id, rows):
    """Create csv file with generated data and save it to db"""
    schema = Schema.objects.get(id=schema_id)
    number = random.randint(1, 999999)
    progress_recorder = ProgressRecorder(self)
    schema_file = SchemaFile.objects.create(
        status=SchemaStatusChoises.PROCESSING, schema=schema)

    try:
        columns = [
            column for column in schema.column_in_schemas.all().order_by("order")
        ]
        filename = f"/schema-{schema.id}--{number}.csv"

        with default_storage.open(filename, "w") as csv_file:
            csv_file.truncate()
            writer = csv.writer(csv_file,
                                delimiter=schema.separator)
            writer.writerow([column.name for column in columns])

            for i in range(rows):
                row_to_write = []
                time.sleep(1)
                for column in columns:
                    row_to_write.append(
                        " ".join(generate_csv_data(column.id).split()))
                writer.writerow(row_to_write)

                progress_recorder.set_progress(i, rows,
                                               description="Generating")

                self.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': rows})

        # updating model instance
        schema_file.file = filename
        schema_file.status = SchemaStatusChoises.READY
        schema_file.save()
        return 'Done'

    except Exception as ex:
        print(ex)
        schema.schema_files.create(file='', status=SchemaStatusChoises.FAILED)
        return 'Failed'
    finally:
        schema.save()
