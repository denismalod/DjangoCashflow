from django.shortcuts import render, get_object_or_404, redirect
from .models import CashFlowRecord, Category, SubCategory, Type, Status
from .forms import CashFlowRecordForm  # создадим Django форму для записи

def records_list(request):
    records = CashFlowRecord.objects.all().order_by('-date')
    return render(request, 'finance/index.html', {'records': records})

def record_form(request, pk=None):
    if pk:
        record = get_object_or_404(CashFlowRecord, pk=pk)
    else:
        record = None

    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('records_list')
    else:
        form = CashFlowRecordForm(instance=record)

    return render(request, 'finance/record_form.html', {'form': form})
