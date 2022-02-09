from django.shortcuts import render
from .forms import MatchingForm
from .helper import get_input
from .helper import get_random_preferance
from .helper import plotgraph
from .helper import init_free_men

tentative_engagements = []
free_men = []
men_list = []
women_list = []
preferred_rankings_men=[]
preferred_rankings_women =[]

def index(request):
    my_form = MatchingForm(request.POST or None)
    global free_men, tentative_engagements, men_list, women_list,preferred_rankings_women,preferred_rankings_men
    tentative_engagements = []
    free_men = []
    men_list = []
    women_list = []
    preferred_rankings_men =[]
    preferred_rankings_women =[]

    n = request.GET.get('input_num')
    if(n == None):
        n = '1'
    men_list = get_input(n,'male')
    women_list = get_input(n,'female')
    preferred_rankings_men = get_random_preferance(men_list,women_list)
    preferred_rankings_women = get_random_preferance(women_list,men_list)

    init_free_men(preferred_rankings_men, free_men)

    while(len(free_men) > 0):
        for man in free_men:
            begin_matching(man)

    image_bytes = plotgraph(tentative_engagements,preferred_rankings_men,preferred_rankings_women)
    context = {
        "form" : my_form,
        "data" : tentative_engagements,
        "input_data_men" : preferred_rankings_men,
        "input_data_women" : preferred_rankings_women,
        "chart" : image_bytes,
        "number" : n
    }

    return render(request, 'index.html',context)



def begin_matching(man):
    for woman in preferred_rankings_men[man]:
        taken_match = [couple for couple in tentative_engagements if woman in couple]
        if (len(taken_match) == 0):
            tentative_engagements.append([man, woman])
            free_men.remove(man)
            break
        elif (len(taken_match) > 0):
            current_guy = preferred_rankings_women[woman].index(taken_match[0][0])
            potential_guy = preferred_rankings_women[woman].index(man)
            if (current_guy < potential_guy):
                pass
            else:
                free_men.remove(man)
                free_men.append(taken_match[0][0])
                taken_match[0][0] = man
                break
    print(len(free_men))  
    
