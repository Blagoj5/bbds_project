from django.shortcuts import render
from .models import Programs

def programsView(request):
    return render(request, 'trainingprograms/programs.html')

def programView(request, program_name):
    return render(request, 'trainingprograms/program.html')
