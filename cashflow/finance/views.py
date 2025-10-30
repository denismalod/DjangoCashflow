from django.shortcuts import render, get_object_or_404, redirect
from .models import CashFlowRecord, Category, SubCategory, Type, Status
from .forms import CashFlowRecordForm  # создадим Django форму для записи

def records_list(request):
    records = CashFlowRecord.objects.all().order_by('-date')

    # получаем фильтры из GET-параметров
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


from django.http import JsonResponse
from .models import SubCategory

def get_subcategories(request):
    """Возвращает список подкатегорий по id категории (для AJAX)."""
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)
