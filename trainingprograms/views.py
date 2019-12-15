from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Programs, Program
from django.core.paginator import Paginator
from django.http import Http404
from .helperfunction import split_weeks
from itertools import chain


def programsView(request):
    programs = Programs.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(programs, 6)

    page = request.GET.get('page')
    programs_paginated = paginator.get_page(page)

    context = {
        'programs': programs_paginated
    }
    return render(request, 'trainingprograms/programs.html', context)


def programView(request, slug_field):

    program = get_object_or_404(Programs ,slug=slug_field)
    
    weeks = []
    week_max = 0
    try :
        for week_number in range(1, 10):
            if Program.objects.order_by('week', 'for_day').filter(program_id=program.id, week=week_number).exists():
                weeks = list(chain(weeks, Program.objects.order_by('week', 'for_day').filter(program_id=program.id, week=week_number)))
                week_max = week_number
            else:
                break

        day = Program.objects.filter(program_id=program.id)[0]
    except IndexError:
        raise Http404("Program does not exist")
    

    weeks = split_weeks(weeks, week_max)

    paginator = Paginator(weeks, 7)
    page = request.GET.get('page')
    week = paginator.get_page(page)

    context = {
        'day': day,
        'week': week,
    }

    return render(request, 'trainingprograms/program.html', context)

def searchView(request):
    return render(request, 'trainingprograms/search.html')