# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action

class TaskListView(APIView):
    
    # Handle GET requests — return all tasks
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    # Handle POST requests — create a new task
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailView(APIView):

    # A helper method to fetch the task or return 404
    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    # GET a single task
    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    # PUT — fully update a task
    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH — partially update a task (e.g. just mark as completed)
    def patch(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE a task
    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    # Let's Rewrite Our Task API Using ViewSets

    class TaskViewSet(viewsets.ModelViewSet):
        queryset = Task.objects.all()
        serializer_class = TaskSerializer

        @action(detail=False, methods=['post'])

        def mark_all_complete(self, request):
            Task.objects.update(completed=True)
            return Response({'status': 'all tasks marked complete'})

        