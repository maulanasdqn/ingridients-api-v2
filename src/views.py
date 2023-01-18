import math
from django.shortcuts import render
from .models import Ingridients, Category
from .serializers import IngridientSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


class IngridientView(generics.GenericAPIView):
    serializer_class = IngridientSerializer
    queryset = Ingridients.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        item = Ingridients.objects.all()
        total_item = item.count()
        if search_param:
            items = item.filter(title__icontains=search_param)
        serializer = self.serializer_class(item[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_item,
            "page": page_num,
            "last_page": math.ceil(total_item / limit_num),
            "items": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "item": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class IngridientDetail(generics.GenericAPIView):
    queryset = Ingridients.objects.all()
    serializer_class =IngridientSerializer
    permission_classes = [IsAuthenticated]

    def get_ingridient(self, pk):
        try:
            return Ingridients.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        item = self.get_ingridient(pk=pk)
        if item == None:
            return Response({"status": "fail", "message": f"Ingridient with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(item)
        return Response({"status": "success", "item": serializer.data})

    def patch(self, request, pk):
        item = self.get_ingridient(pk)
        if item == None:
            return Response({"status": "fail", "message": f"Ingridient with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updated_at'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "item": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_ingridient(pk)
        if item == None:
            return Response({"status": "fail", "message": f"Ingridient with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


