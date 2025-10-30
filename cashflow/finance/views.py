from django.shortcuts import render, get_object_or_404, redirect
from .models import CashFlowRecord, Category, SubCategory, Type, Status
from .forms import CashFlowRecordForm  # создадим Django форму для записи
from django.http import JsonResponse
from django.contrib import messages
from django.forms import modelform_factory
from django.shortcuts import redirect

def records_list(request):
    records = CashFlowRecord.objects.all().order_by('-date')

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        records = records.filter(date__gte=date_from)
    if date_to:
        records = records.filter(date__lte=date_to)
    if status_id:
        records = records.filter(status_id=status_id)
    if type_id:
        records = records.filter(type_id=type_id)
    if category_id:
        records = records.filter(category_id=category_id)
    if subcategory_id:
        records = records.filter(subcategory_id=subcategory_id)

    context = {
        'records': records,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'filters': {
            'date_from': date_from,
            'date_to': date_to,
            'status_id': status_id,
            'type_id': type_id,
            'category_id': category_id,
            'subcategory_id': subcategory_id,
        }
    }
    return render(request, 'finance/index.html', context)


def record_add(request):
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('records_list')
    else:
        form = CashFlowRecordForm()
    return render(request, 'finance/record_form.html', {'form': form, 'title': 'Добавить запись'})


def record_edit(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('records_list')
    else:
        form = CashFlowRecordForm(instance=record)
    return render(request, 'finance/record_form.html', {'form': form, 'title': 'Редактировать запись'})


def record_delete(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запись успешно удалена.')
        return redirect('records_list')
    
    return render(request, 'finance/record_confirm_delete.html', {'record': record})


def get_subcategories(request):
    """Возвращает список подкатегорий по id категории (для AJAX)."""
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def reference_manage(request):
    StatusForm = modelform_factory(Status, fields=('name',))
    TypeForm = modelform_factory(Type, fields=('name',))
    CategoryForm = modelform_factory(Category, fields=('name', 'type'))
    SubCategoryForm = modelform_factory(SubCategory, fields=('name', 'category'))

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'status':
            form = StatusForm(request.POST)
            if form.is_valid(): form.save()
        elif form_type == 'type':
            form = TypeForm(request.POST)
            if form.is_valid(): form.save()
        elif form_type == 'category':
            form = CategoryForm(request.POST)
            if form.is_valid(): form.save()
        elif form_type == 'subcategory':
            form = SubCategoryForm(request.POST)
            if form.is_valid(): form.save()
        return redirect('reference_manage')

    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.select_related('type'),
        'subcategories': SubCategory.objects.select_related('category'),
        'status_form': StatusForm(),
        'type_form': TypeForm(),
        'category_form': CategoryForm(),
        'subcategory_form': SubCategoryForm(),
    }

    return render(request, 'finance/reference_manage.html', context)

def delete_object(request, model, pk, redirect_url_name):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect(redirect_url_name)
    return render(request, 'finance/confirm_delete.html', {'object': obj})

def delete_status(request, pk):
    return delete_object(request, Status, pk, 'records_list')

def delete_type(request, pk):
    return delete_object(request, Type, pk, 'records_list')

def delete_category(request, pk):
    return delete_object(request, Category, pk, 'records_list')

def delete_subcategory(request, pk):
    return delete_object(request, SubCategory, pk, 'records_list')