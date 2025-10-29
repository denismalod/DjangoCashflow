from django.db import models
from django.core.exceptions import ValidationError


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ("name", "type")

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ("name", "category")

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlowRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="records")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="records")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="records"
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, related_name="records"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} | {self.type.name} | {self.amount} ₽"

    def clean(self):

        if self.category.type != self.type:
            raise ValidationError("Выбранная категория не относится к указанному типу.")
        if self.subcategory.category != self.category:
            raise ValidationError(
                "Выбранная подкатегория не связана с выбранной категорией."
            )
        if self.amount <= 0:
            raise ValidationError("Сумма должна быть положительной.")
