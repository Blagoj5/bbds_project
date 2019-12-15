def split_weeks(weeks, week_max):
    """ 
    Method for defining which one is rest day and which one is working day,
    can be done also in the template ---> ex. in program_forloop.html, but also this way
    
    od, from where to start only value is 1, which means day 1
    do, where to finish, it represents the number of weeks, for example if we have 2 weeks it ranges range(1,15) so we include all 14 days

    counter, variable that represents the FIRST number for checking which WEEK it is for example 11, 13, 15, 27 (means WEEK 1 day 1, WEEK 1 day 3, WEEK 2 day 7, etc...)
    counter_two, variable that represents SECOND number for checking which DAY it is for example 11, 13, 15, 27 (means week 1 DAY 1, week 1 DAY 3, week 2 DAY 7, etc...)
    
    Returns a list (of all days in the weeks, deciding which one is rest day and which one is training day)
    """    

    od = 1
    do = (week_max*7) + 1 

    day_in_week = []
    program_in_week = {}
    counter = 1  
    counter_two = 1 
    week_increment = 8
    for i in range(od,do):
        if i == 1:
            for singe_day in weeks:
                    program_in_week[int(str(singe_day.week) + str(singe_day.for_day))] = singe_day

        if i == week_increment:
            week_increment += 7
            counter +=1
            counter_two = 1

        num = int(str(counter) + str(counter_two))
        if num in program_in_week.keys():
            day_in_week.append(program_in_week[num])
        else:
            day_in_week.append('rest')

        counter_two += 1

    return day_in_week


#FUNCTION FOR OLD VERSION

# This function devides the week, for example if you have 4 weeks and the last week are all rest days
# so 7 rest days, it deletes the whole week
def slice_weeks(slice_list, od, do, default_word = None):
    default_word = 'rest'
    counter = 0
    print(od)
    for word in slice_list[od:do]:
        if word == default_word:
            counter += 1

    print(default_word)
    if counter >= 7:
        for i in range(1, 8):
            del slice_list[len(slice_list)-1]

    return slice_list