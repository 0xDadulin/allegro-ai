# views.py
from django.shortcuts import render, redirect, get_object_or_404
from hr_helper.models import UlepszonyTekst
from .forms import UlepszonyTekstForm

# Listowanie ulepszonych tekstów
def ulepszony_tekst_list(request):
    ulepszone_teksty = UlepszonyTekst.objects.filter(uzytkownik=request.user)
    print('chuj')
    return render(request, 'ulepszony_tekst_list.html', {'ulepszone_teksty': ulepszone_teksty})

# Strona szczegółów ulepszonych tekstów
def ulepszony_tekst_detail(request, tekst_id):
    ulepszony_tekst = get_object_or_404(UlepszonyTekst, id=tekst_id, uzytkownik=request.user)
    return render(request, 'ulepszony_tekst.html', {'ulepszony_tekst': ulepszony_tekst})

# Edycja istniejącego ulepszonych tekstów
def ulepszony_tekst_update(request, tekst_id):
    ulepszony_tekst = get_object_or_404(UlepszonyTekst, id=tekst_id, uzytkownik=request.user)
    if request.method == 'POST':
        form = UlepszonyTekstForm(request.POST, instance=ulepszony_tekst)
        if form.is_valid():
            form.save()
            return redirect('ulepszony_tekst_detail', tekst_id=ulepszony_tekst.id)
    else:
        form = UlepszonyTekstForm(instance=ulepszony_tekst)
    return render(request, 'ulepszony_tekst_form.html', {'form': form,'ulepszony_tekst':ulepszony_tekst})
