import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import ToDoTask


class ToDo2Serializer(serializers.Serializer):
    NEW = 'NEW'
    WORKING = 'WORKING'
    DONE = 'DONE'
    STATUS_CHOICES = (
        (NEW, 'NEW'),
        (WORKING, 'WORKING'),
        (DONE, 'DONE'),
    )

    task_name = serializers.CharField(required=True, max_length=50)
    description = serializers.CharField(max_length=300)
    modified_date = serializers.DateField(default=datetime.date.today())
    modify_by = serializers.CharField(required=True, max_length=50)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default=NEW)


class ToDoSerializer(ModelSerializer):
    class Meta:
        model = ToDoTask
        fields = ['ids', 'task_name', 'description', 'modified_date', 'modify_by', 'status']


class ToDoUpdateSerializer(ModelSerializer):
    class Meta:
        model = ToDoTask
        fields = ['description', 'status']


class ToDoCreateSerializer(ModelSerializer):
    class Meta:
        model = ToDoTask
        fields = ['task_name', 'description', 'modify_by']