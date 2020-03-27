from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Hybrid, Vest, Photo
from .forms import AppointmentForm
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'hybridex'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def hybrids_index(request):
    hybrids = Hybrid.objects.filter(user=request.user)
    return render(request, 'hybrids/index.html', {'hybrids': hybrids})

@login_required
def hybrids_index_all(request):
    hybrids = Hybrid.objects.all()
    return render(request, 'hybrids/index_all.html', {'hybrids': hybrids})

@login_required
def hybrids_detail(request, hybrid_id):
    hybrid= Hybrid.objects.get(id=hybrid_id)
    vests_not_owned = Vest.objects.exclude(id__in = hybrid.vests.all().values_list('id'))
    appointment_form = AppointmentForm()
    return render(request, 'hybrids/detail.html', {
        'hybrid': hybrid,
        'appointment_form': appointment_form,
        'vests': vests_not_owned
    })

@login_required
def add_appointment(request, hybrid_id):
    form = AppointmentForm(request.POST)
    if form.is_valid():
        new_appointment = form.save(commit=False)
        new_appointment.hybrid_id = hybrid_id
        new_appointment.save()
    return redirect('detail', hybrid_id=hybrid_id)

@login_required
def assoc_vest(request, hybrid_id, vest_id):
    Hybrid.objects.get(id=hybrid_id).vests.add(vest_id)
    return redirect('detail', hybrid_id=hybrid_id)

@login_required
def unassoc_vest(request, hybrid_id, vest_id):
    Hybrid.objects.get(id=hybrid_id).vests.remove(vest_id)
    return redirect('detail', hybrid_id=hybrid_id)

@login_required
def add_photo(request, hybrid_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, hybrid_id=hybrid_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', hybrid_id=hybrid_id)

def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class HybridCreate(LoginRequiredMixin, CreateView):
    model = Hybrid
    fields = ['name', 'animal', 'produce', 'num_legs']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HybridUpdate(LoginRequiredMixin, UpdateView):
    model = Hybrid
    fields = ['animal', 'produce', 'num_legs']

class HybridDelete(LoginRequiredMixin, DeleteView):
    model = Hybrid
    success_url = '/hybrids/'

class VestList(LoginRequiredMixin, ListView):
    model = Vest

class VestDetail(LoginRequiredMixin, DetailView):
    model = Vest

class VestCreate(LoginRequiredMixin, CreateView):
    model = Vest
    fields = '__all__'
    
class VestUpdate(LoginRequiredMixin, UpdateView):
    model = Vest
    fields = ['vest_type', 'color']
    
class VestDelete(LoginRequiredMixin, DeleteView):
    model = Vest
    success_url = '/vests/'