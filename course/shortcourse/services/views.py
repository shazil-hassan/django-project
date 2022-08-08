from django.http import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site  
import datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, profileUpdateForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .token import account_activation_token 
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_text  

# from .forms import  Userform

def index(request):

    sections = Section.objects.filter(~Q(section_status='CLOSED'))
    today_date = datetime.date.today()
    services = Service.objects.all()
    projects = Project.objects.all()

    data = {
        'sections': sections,
        'today_date': today_date,
        'services': services,
        'projects': projects,
        'meta_title': "HiveSol Technology | Home",
        'meta_description': "HiveSol Focuses on advance Ideas and Learning systems from Consultancy to Development. We offer thousands of technical courses with modern practices",
        'meta_keywords': "HiveSol, Technology, Software Development, E-learning, Softwares"
    }

    return render(request, 'index.html', data)


def description(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.enrollment_set.exists():
                comment = request.POST.get('comment')
                a = Review(comment=comment, user=request.user,
                       course=course)
                a.save()
            else:
                messages.error(request, "You must have to Enroll for Comment")
                return redirect("index")
        else:
            request.session["course"] = slug
            messages.info(request, "Please login to comment")
            return redirect("login")

    data = {
        'course': course,
        'meta_title': course.seo_title,
        'meta_description': course.seo_description,
        'meta_keywords': course.seo_keywords,
    }

    return render(request, 'description.html', data)


@login_required
def loginSuccess(request):
    if 'section' in request.session and request.session['section'] is not None:
        section_slug = request.session['section']
        request.session['section'] = None
        return redirect("course-apply", sid=section_slug)
    elif 'course' in request.session and request.session["course"] is not None:
        course_slug = request.session["course"]
        request.session["course"] = None
        return redirect("description", slug=course_slug)
    else:
        return redirect("/")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'Account activation Link has been sent to your Email Please confirm your email address to continue !')
            current_site = get_current_site(request)  
            mail_subject = 'Account Activation Link'  
            message = render_to_string('active_email.html', {  
                'user': user,  
                'section_slug': request.session['section'] if 'section' in request.session  else None ,
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })   
            email = EmailMessage(  
                        mail_subject, message, to=[user.email]  
            )  
            email.send()  
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form, 'meta_title': "Sign Up", 'meta_description': 'Sign up to learn World best courses and Instructors Guide'})


def activate(request, uidb64, token, section_slug):  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save() 
        login(request, user)
        messages.success(request,  'Thank you for your email confirmation. You are now login.')
        if section_slug != "None":
            return redirect('course-apply', sid = section_slug)
        else:
            return redirect('/')
    else:  
        return HttpResponse('Activation link is invalid!')  

def apply(request, sid):
    section = Section.objects.get(slug=sid)
    if request.method == "POST":
        if section.enrollment_end_date < datetime.date.today():
            messages.error(
                request, "We cant Proceed with your request as Enrollment has been Ended")
        elif section.enrollment_start_date > datetime.date.today():
            messages.error(
                request, "We cant Proceed with your request as Enrollment is not started yet")
        elif Enrollment.objects.filter(user=request.user, section=section).exists():
            messages.error(request, "You already Applied for this course")
        else:
            en = Enrollment(user=request.user, section=section)
            en.save()
            messages.success(
                request, "Your Request for Enrollment is successfully submitted")
            return redirect('enrollments')    
        return redirect('/')
    
    if request.user.is_authenticated is False:
        request.session["section"] = sid
        return redirect('login')

    return render(request, 'applyform.html', {"course_title": section.course.course_name, 'meta_title': section.section_title + " | " + section.course.course_name})


@login_required
def show_enrollment_detail(request):
    obj = Enrollment.objects.filter(user=request.user)
    return render(request, 'show_enrollments.html', {'data': obj, 'meta_title': 'Enrollments'})


@login_required
def profile(request):
    if request.method == 'POST':
        form = profileUpdateForm(request.POST, instance=request.user, files = request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been Updated Successfully !')
            return redirect("profile")

    form = profileUpdateForm(instance = request.user)
    return render(request, 'profile.html', {'form': form, 'meta_title': 'Profile'})


def about(request):
   return render(request, 'about.html', {'meta_title': "HiveSol Technologies | About", 'meta_description': 'Our other goal is to create online learning platforms that are engaging and easy to use for individuals. Let’s empower the learners with an exceptional eLearning experience!'})

def contact(request):
   return render(request, 'contact.html', {'meta_title': "HiveSol Technologies | Contact Us", 'meta_description': 'Our other goal is to create online learning platforms that are engaging and easy to use for individuals. Let’s empower the learners with an exceptional eLearning experience!'})

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

