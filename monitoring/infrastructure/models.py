
from peewee import Model, CharField, DateTimeField, FloatField
from shared.infrastructure.database import db

class DeviceMetricModel(Model):
    device_id = CharField()
    timestamp = DateTimeField()
    metric_type = CharField()
    value = FloatField()
    zone_id = CharField(null=True)
    unit = CharField(null=True)

    class Meta:
        database = db
        table_name = 'device_metrics'
        primary_key = False  # No primary key