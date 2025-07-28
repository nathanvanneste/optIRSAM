from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from .models import Enfant, Groupe
from .forms import EnfantForm, GroupeForm

class EnfantList(ListView):
    model = Enfant
    paginate_by = 20
    template_name = 'user/enfant_list.html'

class EnfantCreate(CreateView):
    model = Enfant
    form_class = EnfantForm
    success_url = reverse_lazy('enfant_list')
    template_name = 'user/enfant_form.html'

class EnfantUpdate(UpdateView):
    model = Enfant
    form_class  = EnfantForm
    success_url = reverse_lazy('enfant_list')
    template_name = 'user/enfant_form.html'

class EnfantDelete(DeleteView):
    model = Enfant
    success_url = reverse_lazy('enfant_list')
    template_name = 'user/enfant_delete.html'

class GroupeList(ListView):
    model = Groupe
    template_name = 'user/groupe_list.html'

class GroupeCreate(CreateView):
    model = Groupe
    form_class = GroupeForm
    success_url = reverse_lazy('groupe_list')
    template_name = 'user/groupe_list.html'

class GroupeUpdate(UpdateView):
    model = Groupe
    success_url = reverse_lazy('groupe_list')
    template_name = 'user/groupe_list.html'

class GroupeDelete(DeleteView):
    model = Groupe
    success_url = reverse_lazy('groupe_list')
    template_name = 'user/groupe_confirm_delete.html'