from rest_framework import serializers
from .models import Status, Type, Category, SubCategory, CashFlowRecord


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(), source="type", write_only=True
    )

    class Meta:
        model = Category
        fields = ["id", "name", "type", "type_id"]


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = SubCategory
        fields = ["id", "name", "category", "category_id"]


class CashFlowRecordSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    type = TypeSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), source="status", write_only=True
    )
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(), source="type", write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source="subcategory", write_only=True
    )

    class Meta:
        model = CashFlowRecord
        fields = [
            "id",
            "date",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
            "status_id",
            "type_id",
            "category_id",
            "subcategory_id",
        ]
