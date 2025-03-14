from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Module, Professor, User, ModuleInstance, Rating
import json

# Create your views here.

def HandleRegisterRequest(request):
    return HttpResponse('Not yet implemented')


@csrf_exempt
def Register(request):
    if request.method == 'POST':
        u1 = User(
            username = request.POST.get('username'),
            email    = request.POST.get('email'),
            password = request.POST.get('password')
        )
        u1.save()
        return HttpResponse('Registration successful')


@csrf_exempt
def Login(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            u1 = User.objects.get(username=username)
        except:
            return HttpResponse('2')
        if u1.password == password:
            return HttpResponse('0')
        else:
            return HttpResponse('1')


@csrf_exempt
def List(request):
    if request.method == 'GET':
        MODULEINSTANCES = {'moduleinstances': []}
        for i in ModuleInstance.objects.all():
            MODULEINSTANCE = {
                'module_code': Module.objects.get(id=i.module.id).code,
                'module_name': Module.objects.get(id=i.module.id).name,
                'year': i.year,
                'semester': i.semester,
                'professors': []
            }

            for j in i.professors.all():
                PROFESSOR = {
                    'professor_code': Professor.objects.get(id=j.id).code,
                    'professor_name': Professor.objects.get(id=j.id).firstname[0]
                                      + '. '
                                      + Professor.objects.get(id=j.id).surname
                }
                MODULEINSTANCE['professors'].append(PROFESSOR)

            print(MODULEINSTANCE['professors'])
            MODULEINSTANCES['moduleinstances'].append(MODULEINSTANCE)
        return HttpResponse(json.dumps(MODULEINSTANCES), content_type='application/json')


@csrf_exempt
def View(request):
    if request.method == 'GET':
        PROFESSORS = {'professors': []}
        for i in Professor.objects.all():
            sum = 0
            count = 0
            for j in Rating.objects.all():
                if i.id == j.professor.id:
                    sum += j.score
                    count += 1
            if count:
                PROFESSOR = {
                    'name': 'Professor ' + i.firstname[0] + '. ' + i.surname,
                    'rating': sum / count
                }
                PROFESSORS['professors'].append(PROFESSOR)
        return HttpResponse(json.dumps(PROFESSORS), content_type='application/json')


@csrf_exempt
def Average(request):
    if request.method == 'POST':
        professor = Professor.objects.get(code=request.POST.get('professor_code')).id
        module    = Module.objects.get(code=request.POST.get('module_code')).id
        professor_id = professor.id
        module_id = module.id

        sum = 0
        count = 0
        for i in Rating.objects.all():
            if i.professor.id == professor_id and i.moduleinstance.module.id == module_id:
                sum += i.score
                count += 1
                print('i')
        if not count:
            average = 0
        else:
            average = sum / count

        JSON = {
            'professor_name': 'Professor ' + professor.firstname[0] + '. ' + professor.surname + ' ({})'.format(professor.code),
            'module_name': module.name + ' ({})'.format(module.code),
            'rating': average
        }
        return HttpResponse(json.dumps(JSON), content_type='application/json')



@csrf_exempt
def Rate(request):
    if request.method == 'POST':
        try:
            professor = Professor.objects.get(code=request.POST.get('professor_code'))
            module = Module.objects.get(code=request.POST.get('module_code'))
            year = request.POST.get('year')
            semester = request.POST.get('semester')
        except:
            return HttpResponse('Module instance does not exist')

        moduleinstance = None
        for i in ModuleInstance.objects.filter(module=module, year=year, semester=semester):
            if professor in i.professors.all():
                moduleinstance = i
        if moduleinstance == None:
            return HttpResponse('Module instance does not exist')

        score = request.POST.get('rating')
        r1 = Rating(
            professor = professor,
            moduleinstance = moduleinstance,
            score = score
        )
        r1.save()

        return HttpResponse('Rating successful')