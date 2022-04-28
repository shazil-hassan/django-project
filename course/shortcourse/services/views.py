import email
from sqlite3 import Date
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .form import Userform
import datetime
from .models import *
# from .forms import  Userform



def about(request):
    return render(request, 'about.html')

def base(request,aid):
    img = Section.objects.get(id=aid)
    
    data ={
        'img':img

        }

 
    return render(request, 'base.html', data)

def index(request):
    
    img= Section.objects.all()
    today_date = datetime.date.today()

    data ={
        'img':img,
        'today_date': today_date
        }

    return render(request,'index.html',data)

def description(request,aid):
    img = Section.objects.get(id=aid)
    data ={
        'img':img
        }

    return render(request, 'description.html', data)


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

  