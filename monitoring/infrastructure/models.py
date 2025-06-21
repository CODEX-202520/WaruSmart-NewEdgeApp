import peewee
from peewee import Model, CharField, DateTimeField, FloatField
from shared.infrastructure.database import db
import datetime

class DeviceMetricModel(peewee.Model):
    id = peewee.AutoField()  # Clave primaria autoincremental
    device_id = peewee.CharField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    metric_type = peewee.CharField()
    value = peewee.FloatField()
    zone = peewee.CharField(null=True)
    unit = peewee.CharField(null=True)
    status = peewee.CharField(max_length=50, null=True)  # <-- Nuevo campo

    class Meta:
        database = db
        table_name = 'device_metrics'
        primary_key = False  # No primary key