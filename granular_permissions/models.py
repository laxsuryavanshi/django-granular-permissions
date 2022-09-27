from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import models
from guardian.models import GroupObjectPermissionAbstract, UserObjectPermissionAbstract

UserModel = get_user_model()


class BaseFieldPermission(models.Model):
    field = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        model = self.permission.content_type.model_class()
        meta = model._meta.concrete_model._meta
        meta.get_field(self.field)  # ensure field exists on model
        return super().save(*args, **kwargs)


class AbstractFieldPermission(BaseFieldPermission):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AbstractUserFieldPermission(AbstractFieldPermission):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta(AbstractFieldPermission.Meta):
        abstract = True
        unique_together = (('user', 'permission', 'field'),)


class UserFieldPermission(AbstractUserFieldPermission):
    pass


class AbstractGroupFieldPermission(AbstractFieldPermission):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta(AbstractFieldPermission.Meta):
        abstract = True
        unique_together = (('group', 'permission', 'field'),)


class GroupFieldPermission(AbstractGroupFieldPermission):
    pass


class AbstractUserObjectFieldPermission(
    BaseFieldPermission, UserObjectPermissionAbstract
):
    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = True
        unique_together = (('user', 'permission', 'object_pk', 'field'),)


class UserObjectFieldPermission(AbstractUserObjectFieldPermission):
    pass


class AbstractGroupObjectFieldPermission(
    BaseFieldPermission, GroupObjectPermissionAbstract
):
    class Meta(GroupObjectPermissionAbstract.Meta):
        abstract = True
        unique_together = (('group', 'permission', 'object_pk', 'field'),)


class GroupObjectFieldPermission(AbstractGroupObjectFieldPermission):
    pass
