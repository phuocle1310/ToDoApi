import datetime
import json

import redis
import view as view
from django.conf import settings
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ToDoTask
from .serializers import ToDoSerializer, ToDoCreateSerializer, ToDoUpdateSerializer

# Connect to our Redis instance
# THIS IS A CONNECTION STRING TO REDIS DB, THIS CAN DEFINE IN setting.py
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class ToDoView(viewsets.ViewSet):
    serializer_class = ToDoSerializer
    NEW = 'NEW'
    WORKING = 'WORKING'
    DONE = 'DONE'
    STASTUS_CHOICES = [NEW, WORKING, DONE]
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ToDoSerializer
        if self.action in ['create']:
            return ToDoCreateSerializer
        if self.action in ['update']:
            return ToDoUpdateSerializer

    def list(self, request):
        items = []
        count = 0
        '''
            +   Get and push data to array
        '''
        for key in redis_instance.keys("*"):
            items.append(json.loads(redis_instance.get(key)))
            count += 1

        # SORT DATA ARRAY ACCORRDING FIELD MODIFIED_DATE DESC
        items = sorted(items, key=lambda k: k['ids'], reverse=True)
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, **kwargs):
        object = redis_instance.get(pk)

        if not object:
            return Response("This todo doesn't exist", status=status.HTTP_404_NOT_FOUND)
        else:
            response = {
                'msg': f"Successfully",
                'items': json.loads(object)
            }
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        serializer = ToDoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = request.data
        '''
            + CREATE A NEW TODO TASK BASE ON REQUEST DATA
        '''
        object = ToDoTask()
        object.task_name = item.get('task_name')
        object.modify_by = item.get('modify_by')
        object.description = item.get('description')
        object.modified_date = str(datetime.datetime.now())
        object.status = ToDoView.NEW    # ALWAYS STATUS IS NEW WHEN CREATE A NEW TASK

        # CREATE AN UNIQUE ID FOR OBJECT. B/C REDIS IS A KEY/VALUE STORE
        object.ids = str(object.modified_date).replace(' ', '').replace('.', '').replace('-', '').replace(':', '')

        # ADD DATA TO DB. B/C DATA MUST BE A STRING THEN CONVERT OBJECT TO STRING
        redis_instance.set(object.ids, json.dumps(ToDoSerializer(object, many=False).data))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, **kwargs):
        serializer = ToDoUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        object = redis_instance.get(pk)
        if not object:
            return Response("This todo doesn't exist", status=status.HTTP_404_NOT_FOUND)

        # GET AND UPDATE DATA BASE ON REQUEST DATA
        object = json.loads(object)
        object['description'] = serializer.data.get('description')
        object['status'] = serializer.data.get('status')

        # WITH THE SAME KEY, REDIS JUST UPDATE DATA WITH KEY, NOT ADD MORE
        redis_instance.set(pk, json.dumps(object))
        return Response(object, status=status.HTTP_200_OK)

    def destroy(self, request, pk, **kwargs):
        object = redis_instance.get(pk)
        if not object:
            return Response("This todo doesn't exist", status=status.HTTP_404_NOT_FOUND)
        else:
            redis_instance.delete(pk)
            response = {
                'msg': f"Delete Successfully",
            }
        return Response(response, status=status.HTTP_200_OK)