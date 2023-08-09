from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=128, null=False)
    email = fields.CharField(max_length=128, null=False, unique=True)
    register_at = fields.DatetimeField(auto_now_add=True)
    hashed_password = fields.CharField(max_length=128, null=False)
    is_active = fields.BooleanField(default=True)


class File(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='users')
    file_name = fields.CharField(max_length=128, null=False, unique=True)
    data_file = fields.BinaryField()


