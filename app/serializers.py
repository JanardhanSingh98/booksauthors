import re

from .models import *
from rest_framework import serializers


class AuthorSerializers(serializers.ModelSerializer):
    au_id = serializers.IntegerField(source='author_uuid', required=False, read_only=True)
    f_n = serializers.CharField(source='first_name')
    l_n = serializers.CharField(source='last_name')
    nt = serializers.CharField(source='notes', required=False)
    cr_at = serializers.ReadOnlyField(source='created_at', required=False)
    up_at= serializers.ReadOnlyField(source='updated_at', required=False)

    class Meta:
        model = Author
        fields = ['id', 'au_id', 'f_n', 'l_n', 'email', 'nt', 'cr_at', 'up_at']


class BookSerializers(serializers.ModelSerializer):
    bo_id = serializers.IntegerField(source='book_uuid', required=False, read_only=True)
    ti = serializers.CharField(source='title')
    desc = serializers.CharField(source='description')
    au_id = serializers.PrimaryKeyRelatedField(source='author', read_only=False, queryset=Author.objects.all())
    cr_at = serializers.ReadOnlyField(source='created_at', required=False)
    up_at= serializers.ReadOnlyField(source='updated_at', required=False)

    class Meta:
        model = Book
        fields = ['bo_id', 'ti', 'desc', 'au_id', 'cr_at', 'up_at']
