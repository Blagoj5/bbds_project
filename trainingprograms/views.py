from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Programs, Program
from django.core.paginator import Paginator
from django.http import Http404
from .helperfunction import split_weeks
from itertools import chain
from django.db.models import Q, Max
from .choices import num_weeks, category_type
from django.contrib.auth.models import User


def programsView(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            liked = request.POST['liked']
            program_id = request.POST['program_id']
            program = get_object_or_404(Programs, id = program_id)
            if liked == 'liked':
                program.is_liked = True
                program.users.add(get_object_or_404(User, id = request.user.id))
                program.save()
            else:
                program.is_liked = False
                program.users.remove(get_object_or_404(User, id = request.user.id))
                program.save()

            # # 1 Way
            # if 'to_redirect' in request.POST:
            #     return redirect('dashboard')

            to_redirect = request.POST.get('to_redirect', False)
            print(to_redirect)
            if to_redirect:
                if to_redirect == 'dashboard':
                    return redirect('dashboard')
                elif to_redirect == 'search':
                    return redirect('search')
            
    programs = Programs.objects.order_by('-is_liked', '-list_date').filter(is_published=True)
    paginator = Paginator(programs, 6)

    page = request.GET.get('page')
    programs_paginated = paginator.get_page(page)


    context = {
        'programs': programs_paginated,
        'weeks': num_weeks,
        'category_type': category_type,
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
    
    # These lines are small query for always updating and adding the max week to the duration field of the current program, so the search queries(and search fields) are VALID
    if not program.program_duration == week_max:
        program.program_duration = week_max
        program.save()
    # ------------------------------------------------------------------------------------------------------------------------------

    weeks = split_weeks(weeks, week_max)

    paginator = Paginator(weeks, 7)
    page = request.GET.get('page')
    week = paginator.get_page(page)

    context = {
        'day': day,
        'week': week,
        'program': program,
    }

    return render(request, 'trainingprograms/program.html', context)



def searchView(request):

    queryset_list = Programs.objects.order_by('-is_liked', '-list_date').filter(is_published=True)

    # Filter by all keywords, and use it even for the nav search input
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(Q(description__icontains=keywords) | Q(athlete_name__icontains=keywords) |
            Q(program_name__icontains=keywords) | Q(program_category__icontains=keywords))


    # Filter by athlete
    if 'athlete' in request.GET:
        athlete = request.GET['athlete']
        if athlete:
            queryset_list = queryset_list.filter(athlete_name__icontains=athlete)


    # Filter by program
    if 'program' in request.GET:
        program = request.GET['program']
        if program:
            queryset_list = queryset_list.filter(program_name__icontains=program)
                
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            queryset_list = queryset_list.filter(program_category__iexact=category)

    if 'duration' in request.GET:
        duration = request.GET['duration']
        if duration:
            # Aggregation function and gruoping
            # queryset_list_two = Program.objects.values('program_id').annotate(max_week=Max('week')) # This is query that groups by program_id(ex 1, 2, etc ..) and finds max week of each program (ex. {'program_id': 1, 'max_week': 2} )
                queryset_list = queryset_list.filter(program_duration__lte=duration)

    paginator = Paginator(queryset_list, 6)
    page = request.GET.get('page')
    queryset_list_paginated = paginator.get_page(page)


    context = {
        'weeks': num_weeks,
        'category_type': category_type,
        'programs': queryset_list_paginated,
        'values': request.GET,
    }

    return render(request, 'trainingprograms/search.html', context)