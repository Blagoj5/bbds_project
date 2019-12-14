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