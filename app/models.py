import random
from django.db import models
from django.utils import timezone


class Author(models.Model):
    author_uuid = models.IntegerField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, unique=True)
    notes = models.TextField(null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    created_by = models.CharField(default='', max_length=255)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(default='', max_length=255)

    def __str__(self):
        return str(self.author_uuid)

    def save(self, *args, **kwargs):
        # On save, update timestamps #
        if not self.id:
            self.created_at = timezone.now()
            self.is_active = True
            self.author_uuid = random.randrange(1000000, 9999999)
            self.created_by = 'admin'
            self.updated_by = 'admin'
        self.updated_at = timezone.now()
        return super(Author, self).save(*args, **kwargs)


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_uuid = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    created_by = models.CharField(default='', max_length=255)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(default='', max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # On save, update timestamps #
        if not self.id:
            self.created_at = timezone.now()
            self.is_active = True
            self.book_uuid = random.randrange(1000000, 9999999)
            self.created_by = 'admin'
            self.updated_by = 'admin'
        self.updated_at = timezone.now()
        return super(Book, self).save(*args, **kwargs)
