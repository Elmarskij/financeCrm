from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

#This link will help you https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340



class SoftDeleteQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    date_deleted, effectively soft-deleting the object.
    """
    def delete(self):
        return super(SoftDeleteQuerySet, self).update(deleted_on=timezone.now())

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()

    def undelete(self):
        return self.filter(deleted_on=None)


class SoftDeleteManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model).filter(deleted_on=None)
        return SoftDeleteQuerySet(self.model)

    def get_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_on__isnull=False)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeleteModel(models.Model):

    class Meta:
        abstract = True

    deleted_on = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteManager()
    original_objects = models.Manager()
    all_objects = SoftDeleteManager(alive_only=False)

    def delete(self):
        self.deleted_on=timezone.now()
        self.save()

    def undelete(self):
        self.deleted_on=None
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()
