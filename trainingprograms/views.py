from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Programs, Program, Program_User
from django.core.paginator import Paginator
from django.http import Http404
from .helperfunction import split_weeks
from itertools import chain
from django.db.models import Q, Max
from .choices import num_weeks, category_type
from django.contrib.auth.models import User


def programsView(request):
    programs_for_user = []
    if request.user.is_authenticated:
        if request.method == 'POST':
            liked = request.POST['liked']
            program_id = request.POST['program_id']
            program = get_object_or_404(Programs, id = program_id)
            user = get_object_or_404(User, id = request.user.id)
            if liked == 'unliked':
                if not Program_User.objects.filter(user=user.id, program=program.id, is_liked=True).exists():
                    program_user = Program_User.objects.create(user=user, program=program, is_liked=True)
            else:
                # Deleting object in order for the table to have less tuples(rows) in the database, only add programs in the db
                # that the user has liked, else if they are not liked=delete them from the db
                if Program_User.objects.filter(user=user.id, program=program.id, is_liked=True).exists():
                    program_user = Program_User.objects.get(user=user.id, program=program.id, is_liked=True)
                    program_user.delete()



            # # 1 Way
            # if 'to_redirect' in request.POST:
            #     return redirect('dashboard')

            to_redirect = request.POST.get('to_redirect', False)
            if to_redirect:
                if to_redirect == 'dashboard':
                    return redirect('dashboard')
                elif to_redirect == 'search':
                    return redirect('search')


            if Program_User.objects.filter(user=request.user.id , is_liked=True).exists():
                programs_for_user = Program_User.objects.filter(
                    user=request.user.id, 
                    is_liked=True, 
                    program__is_published=True
                )
        
        elif request.method == 'GET':
            # Treba da se dodade is_published isto taka
            if Program_User.objects.filter(user=request.user.id , is_liked=True).exists():
                programs_for_user = Program_User.objects.filter(
                    user=request.user.id, 
                    is_liked=True, 
                    program__is_published=True
                )


    programs = Programs.objects.order_by('-list_date').filter(is_published=True)


    # method for adding the liked programs (objects) for a certain user to a new list
    liked_programs = []
    for program in programs_for_user:
        liked_programs.append(program.program)

    # #fix ordering (tried with order_by but also orders for other users, problem is that i only put info in db for when a program is liked!)
    # # quick fix --->
    # ordered_programs = []
    # unliked_programs = ['line']
    # for program in programs:
    #     if program not in liked_programs:
    #         unliked_programs.append(program)

   
    # ordered_programs = liked_programs + unliked_programs

    paginator = Paginator(programs, 6)


    page = request.GET.get('page')

    # Solution num 1: Add another field in the  Post form, and get the page.number so you display that again
    # if page is None:
    #     if 'page' in request.POST:
    #         page = request.POST.get('page')
    
    #Solution num 2: Store it in previous session, and get it in the needed session where there will be a post field named 'change_page' in order to notify
    # if 'change_page' in request.POST:
    #     page = request.session.get('page', None)
    #     request.session['page'] = request.GET.get('page') # This will be set to None, because  there will be no pages;
    # else:
    #     request.session['page'] = request.GET.get('page')

    if page is None:
        if 'page' in request.POST:
            page = request.POST.get('page')
            request.GET._mutable = True
            request.GET['page'] = page
            request.GET._mutable = False
            print(request.GET._mutable)


    programs_paginated = paginator.get_page(page)

    print(request.GET)
    print(request.POST)
    # print(request.session.get('page', None))

   
    context = {
        'programs': programs_paginated,
        'liked_programs': liked_programs,
        'weeks': num_weeks,
        'category_type': category_type,
        'page': request.GET.get('page'),
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

    queryset_list = Programs.objects.order_by('-list_date').filter(is_published=True)

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