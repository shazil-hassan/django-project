import email
from re import L
from sqlite3 import Date
from django.http import *
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .form import Userform
import datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt


# from .forms import  Userform



def about(request):
    return render(request, 'about.html')



def index(request):
    
    sections= Section.objects.all()
    today_date = datetime.date.today()

    data ={
        'sections':sections,
        'today_date': today_date
        }

    return render(request,'index.html',data)

def description(request,aid):
    course=Section.objects.get(id=aid).course_id
    if request.method =="POST":
        comment=request.POST.get('comment')
        name=request.POST.get('name')
        reply_id=request.POST.get('review_id')
        if name == "":
            name = "Anonymous"
        
        a=Review(comment=comment,name=name,course_id=course,parent_id=reply_id)
        a.save()

        
    massage= Review.objects.filter(course_id=course, parent=None)
    
    section = Section.objects.get(id=aid)
    data ={
        'section':section,
        'massage':massage,
        
        }

    return render(request,'description.html', data)

@csrf_exempt
def like(request):
 
    if request.method=="POST":
        id=request.POST.get('id')
        response=request.POST.get('value')

        r=Review.objects.get(id=id)

        if response == "1":
            r.likes= r.likes+1            
        else:
            r.dislikes = r.dislikes+1        
        r.save()
        data=response
       
        
    return HttpResponse(data)
    # return JsonResponse(data)

 

def applyform(request,aid):

        img = Section.objects.get(id=aid)

        if request.method =="POST":
            formdata =Userform(request.POST)
            if formdata.is_valid():
        
                fname= formdata.cleaned_data['first_name']
                lname= formdata.cleaned_data['last_name']
                email= formdata.cleaned_data['email']
                cnic= formdata.cleaned_data['cnic']
                contact= formdata.cleaned_data['contact']
                educational_background= formdata.cleaned_data['educational_background']
            
                myuser= User(first_name=fname,last_name=lname,email=email,cnic=cnic,contact=contact,educational_background=educational_background)
                user=formdata.save()

                en= Enrollment.objects.create(user=user,section_id=aid,apply_date=datetime.datetime.now(),activation_Date=datetime.datetime.now(),activate='True')
                en.save()
                return redirect('/')
        else:
            formdata=Userform()

           
           

        return render(request,'applyform.html',{'form':formdata })

    # if request.method == 'POST':

    #     first_name=request.POST['first_name']
    #     last_name=request.POST['last_name']
    #     email=request.POST['email']
    #     cnic=request.POST['cnic']
    #     contact=request.POST['contact']
    #     educational_background=request.POST['educational_background']
        

    #     myuser = User.objects.create(first_name=first_name,last_name=last_name,email=email,cnic=cnic,contact=contact,educational_background=educational_background)
    #     User.save(myuser)

    #     return redirect('/')
  
    # return render(request, 'applyform.html')



class StudentList(ListView):
 
    # specify the model for list view
    model = Section
    template_name = "course_list.html" 




# class StudentCreate(CreateView):
  
#     # specify the model for create view
#     model = User
  
#     # specify the fields to be displayed
  
#     fields = ['name', 'email','password']
#     template_name = "create.html"
#     # success_url = reverse_lazy("home")

  