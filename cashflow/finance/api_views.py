from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Status, Type, Category, SubCategory, CashFlowRecord
from .serializers import (
    StatusSerializer, TypeSerializer, CategorySerializer,
    SubCategorySerializer, CashFlowRecordSerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related('type').all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class CashFlowRecordViewSet(viewsets.ModelViewSet):
    queryset = CashFlowRecord.objects.select_related(
        'status', 'type', 'category', 'subcategory'
    ).all()
    serializer_class = CashFlowRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'status', 'type', 'category', 'subcategory']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        """Поддержка фильтрации по диапазону дат"""
        queryset = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset
