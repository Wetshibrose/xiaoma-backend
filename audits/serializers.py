from rest_framework import serializers

from django.contrib.admin.models import LogEntry


class AuditsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = "__all__"
