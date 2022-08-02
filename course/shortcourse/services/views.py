from django.http import *
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.list import ListView
from .form import Userform
import datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm,update_profile_form
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# from .forms import  Userform


def about(request):
    return render(request, 'about.html')


def index(request):

    sections = Section.objects.filter(~Q(section_status = 'CLOSED'))
    today_date = datetime.date.today()
    services = Service.objects.all()

    data = {
        'sections': sections,
        'today_date': today_date,
        'services': services,
    }

    return render(request, 'index.html', data)


def description(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment = request.POST.get('comment')
            a = Review(comment=comment, user=request.user,
                   course=course)
            a.save()
        else:
            request.session["course"] = slug
            messages.info(request, "Please login to comment")
            return redirect("login")

    data = {
        'course': course,
        'latestSection': course.sections.last(),
        'reviews': course.reviews.all(),
        'instructors': course.instructors.all(),
        'faqs': course.FAQ.all(),
    }

    return render(request, 'description.html', data)

@login_required
def loginSuccess(request):
    if  'section' in request.session and request.session['section'] is not None:
        section_id = request.session['section']
        request.session['section'] = None
        return redirect("course-apply", sid=section_id)
    elif 'course' in request.session and request.session["course"] is not None:
        course_slug = request.session["course"] 
        request.session["course"]  = None
        return redirect("description", slug= course_slug)
    else:
        return redirect("/")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, 'Registered Successfully !')
            if request.session["section"] is not None:
                section_id = request.session['section']
                request.session['section'] = None
                return redirect("course-apply", sid=section_id)
            else:
                redirect("/")
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def apply(request, sid):
    section = Section.objects.get(id = sid)
    if request.method == "POST": 
            if section.enrollment_end_date < datetime.date.today():
                 messages.error(request, "We cant Proceed with your request as Enrollment has been Ended")
            elif Enrollment.objects.filter(user = request.user , section = section).exists():
                messages.error(request, "You already Applied for this course")
            else:
                en = Enrollment.objects.create(user=request.user, section_id=sid, status='inactive')
                en.save()
                messages.success(request, "Your Request for Enrollment successfully submitted")
            return redirect('/')
    else:
        if request.user.is_authenticated is False:
            request.session["section"] = sid
            return redirect('login')

    return render(request, 'applyform.html', {"course_title": section.course.course_name})


@csrf_exempt
def like(request):

    if request.method == "POST":
        id = request.POST.get('id')
        response = request.POST.get('value')

        r = Review.objects.get(id=id)

        if response == "1":
            r.likes = r.likes+1
        else:
            r.dislikes = r.dislikes+1
        r.save()
        data = response

    return HttpResponse(data)
    # return JsonResponse(data)


def show_enrollment_detail(request):

    obj = Enrollment.objects.filter(user=request.user)
    
    return render(request,'show_enrollments.html',{'data':obj})

def update_profile(request):
    if request.user.is_authenticated:
        data = User.objects.get(id=request.user.id)
        
        if request.method == "POST":
            form = update_profile_form(request.POST, instance = request.user)

            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            educational_background = request.POST["educational_background"]
            
            if form.is_valid():
                User.objects.filter(id=request.user.id).update(first_name=first_name,last_name=last_name,email=email,educational_background=educational_background)
                form.save()
                return redirect('update-profile')

        form = update_profile_form(instance = request.user)
    return render(request,'update_profile.html', {'data': data,'form':form}) 
    

class StudentList(ListView):

    # specify the model for list view
    model = Section
    template_name = "course_list.html"
