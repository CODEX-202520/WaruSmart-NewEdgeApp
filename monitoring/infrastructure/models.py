import peewee
from peewee import Model, CharField, DateTimeField, FloatField, BooleanField
from shared.infrastructure.database import db
import datetime

class DeviceMetricModel(peewee.Model):
    id = peewee.AutoField()  # Clave primaria autoincremental
    device_id = peewee.CharField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    zone = peewee.CharField(null=True)
    soil_moisture = peewee.FloatField()
    temperature = peewee.FloatField()
    humidity = peewee.FloatField()

    class Meta:
        database = db
        table_name = 'device_metrics'

class DeviceConfigModel(peewee.Model):
    id = peewee.AutoField()
    device_id = peewee.CharField(unique=True)
    parcela_id = peewee.CharField()
    soil_moisture_min_device = peewee.FloatField()
    temperature_max_device = peewee.FloatField()
    humidity_min_device = peewee.FloatField()
    overwrite_automation = peewee.BooleanField(default=False)
    manually_active = peewee.BooleanField(default=False)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'device_configs'



class ActuatorModel(peewee.Model):
    id = peewee.AutoField()  # Clave primaria autoincremental
    device_id = peewee.CharField()
    status = peewee.CharField(default="inactive")
    actuator_type = peewee.CharField(default="relay")
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'actuators'