from django.views.decorators import cache
import requests
import datetime

from django.views import View
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import SearchForm

class RegistrationView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect("main:home")

        context={'form':UserCreationForm()}
        
        return render(request,'apps/main/register.html', context=context)

    def post(self, request):

        if request.user.is_authenticated:
            return redirect("main:home")

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:login')

        return render(request, 'apps/main/register.html', {'form':form, 'error':form.errors})

class LoginView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect("main:home")

        context={'form':AuthenticationForm()}
        
        return render(request,'apps/main/login.html', context=context)

    def post(self, request):

        if request.user.is_authenticated:
            return redirect("main:home")

        form = AuthenticationForm(request=request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['last_request'] = 0
                request.session['request_num'] = 0
                print(reverse('main:home')+"?msg=Login%20Success")
                return redirect(reverse('main:home')+"?msg=Login%20Success")
        
        return render(request, 'apps/main/login.html', context={'form':form, 'error':"Invalid credentials."})

class HomeView(View):

    @method_decorator(cache_page(2*60))
    def get(self, request):

        allow = False

        print(request.session.get('last_request'))
        if request.session.get('last_request') == 0:
            request.session['last_request'] = datetime.datetime.timestamp(datetime.datetime.now())
            request.session['request_num'] = 1
            allow = True
        else:
            if ((request.session['last_request'] - datetime.datetime.timestamp(datetime.datetime.now()))/60)>5:
                if request.session['request_num'] <= 100:
                    allow = True

        context = None
        question_filter = None
        params = {}

        if allow:

            if request.GET != {}:

                data = request.GET.dict()

                if not ((request.GET.get('fromdate_day') in ['',None,'unknown',]) or (request.GET.get('fromdate_month') in ['',None,'unknown',]) or (request.GET.get('fromdate_year') in ['',None,'unknown',])):
                    from_epoch = datetime.datetime(
                        int(request.GET.get('fromdate_year')),
                        int(request.GET.get('fromdate_month')),
                        int(request.GET.get('fromdate_day')),
                        0,
                        0
                    ).timestamp()
                    data.update({'fromdate':str(int(from_epoch))})

                if not ((request.GET.get('todate_day') in ['',None,'unknown',]) or (request.GET.get('todate_month') in ['',None,'unknown',]) or (request.GET.get('todate_year') in ['',None,'unknown',])):
                    to_epoch = datetime.datetime(
                        int(request.GET.get('todate_year')),
                        int(request.GET.get('todate_month')),
                        int(request.GET.get('todate_day')),
                        23,
                        59
                    ).timestamp()
                    data.update({'todate':str(int(to_epoch))})

                question_filter = SearchForm(request.GET)
                if question_filter.is_valid():
                    data = question_filter.cleaned_data
                    params.update(data)
                else:
                    question_filter = SearchForm()

            else:
                question_filter = SearchForm()

        else:
            question_filter = SearchForm()

        if request.user.is_authenticated:
            
            field_list = []
            temp = []
            q_field = None
            counter = 0
            for field in question_filter:
                counter += 1
                if counter != 1:
                    if len(temp) < 3:
                        temp.append(field)
                    else:
                        field_list.append(temp)
                        temp = [field,]
                else:
                    q_field = field

            field_list.append(temp)


            if context is None:
                context = {'form': question_filter, 'field_count': field_list, 'q_field': q_field}
            else:
                context.update({'form':question_filter, 'field_count': field_list, 'q_field': q_field})

            if allow:

                url = "https://api.stackexchange.com/2.2/search/advanced"

                if params != {}:

                    params.update({
                        'site':'stackoverflow'
                    })

                    if 'page' in request.GET.keys():
                        params.update({
                            'page':request.GET.get('page')
                        })

                    req = requests.get(url,params=params)
                    items = req.json()

                    items_objs = items['items']
                    # items_temp = []
                    for item in items_objs:
                        if 'creation_date' in item.keys():
                            item['creation_date'] = datetime.datetime.fromtimestamp(item['creation_date'])
                        if 'last_activity_date' in item.keys():
                            item['last_activity_date'] = datetime.datetime.fromtimestamp(item['last_activity_date']).strftime("%c")
                        if 'last_edit_date' in item.keys():
                            item['last_edit_date'] = datetime.datetime.fromtimestamp(item['last_edit_date']).strftime("%c")

                    if items['has_more'] in ['true',True]:
                        next_page = 2
                        if ('page' in request.GET.keys()) and (request.GET.get('page') not in [None,'','unknown','None']):
                            print(request.GET.get('page'), type(request.GET.get('page')))
                            next_page = int(request.GET.get('page')) + 1
                        context.update({'next_page':next_page})

                    if ('page' in request.GET.keys()) and (request.GET.get('page') not in [None,'','unknown','None']):
                        if int(request.GET.get('page')) > 1:
                            context.update({'previous_page':int(request.GET.get('page')) - 1})

                    context.update({'items':items['items']})

            else:
                context.update({'info_msg':"Requests limited to 1 per 5 mins and 100 per session."})

        return render(request, 'apps/main/home.html', context=context)
