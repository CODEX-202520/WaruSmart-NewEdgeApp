# shared/infrastructure/database.py

from peewee import SqliteDatabase

db = SqliteDatabase('waru-smart.db')

def init_db() -> None:
    """
    Initializes the database connection and creates tables for monitoring and iam modules.
    """
    db.connect()
    from monitoring.infrastructure.models import DeviceMetricModel, DeviceConfigModel
    from iam.infrastructure.models import Device
    db.create_tables([Device, DeviceMetricModel, DeviceConfigModel], safe=True)
    db.close()