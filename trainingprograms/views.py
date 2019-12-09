from django.shortcuts import render

def programsView(request):
    return render(request, 'trainingprograms/programs.html')

def programView(request, program_name):
    return render(request, 'trainingprograms/program.html')
