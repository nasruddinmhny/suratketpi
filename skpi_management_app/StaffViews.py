
import os
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import CustomUser, Staff
from .forms import CreateCustomUserForm,UpdateMAhasiswaForm,CreateKonfirmasiData

from .models import Mahasiswa, ProgramStudi,KonfirmasiData


def staff_home(request):
    loginuserprodi = Staff.objects.get(admin=request.user.id)
    mahasiswa_count = Mahasiswa.objects.filter(programstudi=loginuserprodi.programstudi).count()
    staff = Staff.objects.get(admin=request.user.id)
    print(loginuserprodi.programstudi)

    context={
        'mahasiswa_count':mahasiswa_count,
        'staff':staff,
        'loginuserprodi':loginuserprodi,


    }
    return render(request,'staff_template/home_content.html',context)

def manage_mahasiswa(request):
    mahasiswa = Mahasiswa.objects.all()
    return render(request,'staff_template/staff_manage_mahasiswa_template.html',{'mahasiswa':mahasiswa})

def add_mahasiswa(request):
    form_mahasiswa = CreateCustomUserForm()
    context={
        'form_mahasiswa':form_mahasiswa,
    }
    return render(request,'staff_template/add_mahasiswa_template.html',context)

def add_mahasiswa_save(request):
    if request.method == 'POST':
        form_mahasiswa = CreateCustomUserForm(request.POST)  
        if form_mahasiswa.is_valid():
            userForm = form_mahasiswa.save(commit=False)
            userForm.user_type = 3 
            #userForm.programstudi_id = ProgramStudi.objects.get(id=1)
            userForm.save()
            messages.success(request,'Data User Disimpan')  
            return redirect('staff_add_mahasiswa')
    else:
        form_mahasiswa= CreateCustomUserForm()
        
    context = {
        'form_mahasiswa':form_mahasiswa,
        
    }
    return render(request,'staff_template/add_mahasiswa_template.html',context)
    '''
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        
      
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        nim = request.POST.get('nim')
        tempatlahir = request.POST.get('tempatlahir')
        tgllahir = request.POST.get('tgllahir')
        #programstudi = ProgramStudi.objects.get(id=request.POST.get('programstudi'))
        
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.mahasiswa(address=address,nim=nim,tempatlahir=tempatlahir,tgllahir=tgllahir,prodi=programstudi)
            user.save()
            messages.success(request, "Data Mahasiswa Di Tambah!")
            return redirect('add_mahasiswa')
        except:
            messages.error(request, "Data Mahasiswa gagal Di Tambah!")
            return redirect('add_mahasiswa')
        '''

def hapus_mahasiswa(request,mahasiswa_id):
    mahasiswa = Mahasiswa.objects.get(admin=mahasiswa_id)
    user = CustomUser.objects.get(id=mahasiswa_id)
    try:
        mahasiswa.delete()
        user.delete()
        messages.success(request, "Data Mahasiswa Dihapus")
        return redirect('staff_manage_mahasiswa')
    except:
        messages.error(request, "Data mahasiswa gagal di hapus!")
        return redirect('staff_manage_mahasiswa')

def update_mahasiswa(request,user_id):
    mahasiswa= Mahasiswa.objects.get(admin=user_id)
   
    if request.method == 'POST':
        form_mahasiswa = UpdateMAhasiswaForm(request.POST,instance=mahasiswa)
        if form_mahasiswa.save():
            messages.success(request, "Data Di update")
            return redirect('staff_manage_mahasiswa')
        #else:
            #messages.error(request, "Data gagal update")
            #return redirect('update_mahasiswa',mahasiswa.admin.id)
    else:
        
        form_mahasiswa = UpdateMAhasiswaForm(instance=mahasiswa)


    context={
        'form_mahasiswa':form_mahasiswa,
    }
    return render(request,'hod_template/edit_mahasiswa_template.html',context)

def view_mahasiswa_skpi(request,user_id):
    mhs = Mahasiswa.objects.get(admin=user_id)
    konfir = KonfirmasiData.objects.filter(mahasiswa=mhs.id)

    if request.method == 'POST':
        form = CreateKonfirmasiData(request.POST)
        print(form)
        if form.is_valid():
            konfirmData = form.save(commit=False)
            konfirmData.mahasiswa_id = mhs.id
            konfirmData.save()
            return redirect('manage_mahasiswa')
    else:
        form = CreateKonfirmasiData()
    

    #customuser = CustomUser.objects.get(id=user_id)
    #prodi = ProgramStudi.objects.get(id=mahasiswa.programstudi_id)
    
    #mahasiswa = Mahasiswa.objects.select_related('pelatihan','organisasi').get(admin=user_id)
    #pelatihan = Pelatihan.objects.get(mahasiswa=user_id)
    context={
        
        'mahasiswa':mhs,
        'konfirmasi':konfir,     
        'form':form,
        #'customuser':customuser, 
        #'prodi':prodi,
    }
    return render(request,'staff_template/view_skpi_template.html',context)



@csrf_exempt
def staff_check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def staff_check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)