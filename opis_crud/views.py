# views.py
from django.shortcuts import render, redirect, get_object_or_404
from hr_helper.models import Opis
from .forms import OpisForm

# Listowanie opisów
def opis_list(request):
    opisy = Opis.objects.filter(user=request.user)
    print(opisy)
    return render(request, 'opis_list.html', {'opisy': opisy})

# Strona szczegółów opisu
def opis_detail(request, opis_id):
    opis = get_object_or_404(Opis, id=opis_id, user=request.user)
    return render(request, 'opis_detail.html', {'opis': opis})

# Edycja istniejącego opisu
def opis_update(request, opis_id):
    opis = get_object_or_404(Opis, id=opis_id, user=request.user)
    if request.method == 'POST':
        form = OpisForm(request.POST, instance=opis)
        if form.is_valid():
            form.save()
            return redirect('opis_detail', opis_id=opis.id)
    else:
        form = OpisForm(instance=opis)
    return render(request, 'opis_form.html', {'form': form})
