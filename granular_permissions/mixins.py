from django.contrib.contenttypes.models import ContentType
from rest_framework.fields import empty
from rest_framework.serializers import ALL_FIELDS, ModelSerializer

from granular_permissions.models import (
    GroupFieldPermission,
    GroupObjectFieldPermission,
    UserFieldPermission,
    UserObjectFieldPermission,
)


class GranularPermissionMixin:
    model_class = None
    perms_map = {
        'GET': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete',
    }

    def get_model_class(self):
        assert self.model_class is not None, (
            f'`{self.__class__.__name__}` should either include a `model_class`'
            'attribute, or override the `get_model_class()` method.'
        )
        return self.model_class

    def get_required_perm(self, method, model_class):
        app_label = model_class._meta.app_label
        model_name = model_class._meta.model_name
        return f'{app_label}.{self.perms_map[method]}_{model_name}'

    def get_fields(self, user, model_class, perm, instance=None):
        content_type = ContentType.objects.get_for_model(model_class)
        querysets = [
            UserFieldPermission.objects.filter(
                user=user,
                permission__content_type=content_type,
                permission__codename=perm,
            ),
            GroupFieldPermission.objects.filter(
                group__user=user,
                permission__content_type=content_type,
                permission__codename=perm,
            ),
        ]

        if instance is not None:
            querysets += [
                UserObjectFieldPermission.objects.filter(
                    user=user,
                    content_type=content_type,
                    object_pk=instance.pk,
                    permission__codename=perm,
                ),
                GroupObjectFieldPermission.objects.filter(
                    group__user=user,
                    content_type=content_type,
                    object_pk=instance.pk,
                    permission__codename=perm,
                ),
            ]

        read_fields = set()
        write_fields = set()
        for qs in querysets:
            qs = list(
                qs.select_related('permission').values_list(
                    'field', 'permission__codename'
                )
            )
            for field, perm in qs:
                if perm.startswith('view_'):
                    read_fields.add(field)
                else:
                    write_fields.add(field)
        return (
            list(read_fields.union(write_fields)),
            list(read_fields - write_fields),
            {field: {'write_only': True} for field in write_fields - read_fields},
        )

    def get_serializer_class(self, instance=None):
        model_class = self.get_model_class()
        perm = self.get_required_perm(self.request.method, model_class)
        user = self.request.user

        class Serializer(ModelSerializer):
            class Meta:
                pass

        setattr(Serializer.Meta, 'model', model_class)
        if user.has_perm(perm, instance):
            setattr(Serializer.Meta, 'fields', ALL_FIELDS)
        else:
            _, perm = perm.split('.', 1)
            fields, read_only_fields, extra_kwargs = self.get_fields(
                user, model_class, perm, instance=instance
            )
            setattr(Serializer.Meta, 'fields', fields)
            setattr(Serializer.Meta, 'read_only_fields', read_only_fields)
            setattr(Serializer.Meta, 'extra_kwargs', extra_kwargs)

        return Serializer

    def get_serializer(self, instance=None, data=empty, **kwargs):
        serializer_class = self.get_serializer_class(instance)
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(instance, data=data, **kwargs)
