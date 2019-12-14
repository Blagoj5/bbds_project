from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Programs, Program
from django.core.paginator import Paginator
from django.http import Http404
from .helperfunction import slice_weeks
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
    
    try :
        days = Program.objects.order_by('for_day').filter(program_id=program.id)
        day = Program.objects.order_by('for_day').filter(program_id=program.id)[0]
    except IndexError:
        raise Http404("Program does not exist")
    
    # Method for defining which one is rest day and which one is working day,
    # can be done also in the template ---> ex. in program_forloop.html, but also this way
    day_in_week = []
    program_in_week = {} 
    for i in range(1,29):
        if i == 1:
            for d in days:
                    program_in_week[d.for_day] = d

        if i in program_in_week.keys():
            day_in_week.append(program_in_week[i])
        else:
            day_in_week.append('rest')

    slice_weeks(day_in_week, 21, 28)
    slice_weeks(day_in_week, 14, 21)
    

    print(day_in_week)
    paginator = Paginator(day_in_week, 7)

    page = request.GET.get('page')
    week = paginator.get_page(page)

    context = {
        'days': days,
        'day': day,
        'week': week,
    }
    return render(request, 'trainingprograms/program.html', context)
