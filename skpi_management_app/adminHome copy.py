import os
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .forms import CreateCplForm, CreateGelarfForm, CreatePelatihanForm, CreateUserForm,CreateOrganisasiForm, CreatePerguruanTinggiForm, CreateStaffForm, CreateSubCplForm, CreatemahasiswaForm, UpdateCplForm, UpdateGelarfForm, UpdatePerguruanTinggiForm,CreateFakultasForm,UpdateFakultasForm,CreateProgramStudiForm,UpdateProgramStudiForm, UpdateSubCplForm

from .models import Cpl, CustomUser, Fakultas, Gelar, Organisasi, Pelatihan, PerguruanTinggi, ProgramStudi,Staff,Mahasiswa, SubAspekCpl

def admin_home(request):
    all_mahasiswa_count = Mahasiswa.objects.all().count()
    all_staff_count = Staff.objects.all().count()
    all_programstudi_count = ProgramStudi.objects.all().count()
    all_perguruantinggi_count = PerguruanTinggi.objects.all().count

    context={
        'all_mahasiswa_count':all_mahasiswa_count,
        'all_staff_count':all_staff_count,
        'all_programstudi_count':all_programstudi_count,
        'all_perguruantinggi_count':all_perguruantinggi_count,
    }
    return render(request,'hod_template/home_content.html',context)

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        'user':user,
    }
    return render(request,'hod_template/admin_profile.html',context)

#perguruan tinggi
def manage_perguruantinggi(request):
    perguruantinggi = PerguruanTinggi.objects.all()

    if request.method == 'POST':
        form = CreatePerguruanTinggiForm(request.POST,request.FILES)

        if form.is_valid():
            namapt = form.cleaned_data['nama']
            nomorsk = form.cleaned_data['nosk']
            logopt = form.cleaned_data['logo']

            try:
                perguruantinggi = PerguruanTinggi(nama=namapt,nosk=nomorsk,logo=logopt)
                perguruantinggi.save()
                messages.success(request,'Data Perguruan Tinggi Ditambah! ')
                return redirect('manage_perguruan_tinggi')
            except:
                messages.error(request,'Gagal Tambah Data!!!')
                return redirect('manage_perguruan_tinggi')
    else:
        form = CreatePerguruanTinggiForm()
    context={
        'perguruantinggi':perguruantinggi,
        'form':form,
    }
    return render(request,'hod_template/manage_perguruantinggi_template.html',context)

def hapus_perguruantinggi(request,perguruantinggi_id):
    perguruantinggi = PerguruanTinggi.objects.get(id=perguruantinggi_id)
    if len(perguruantinggi.logo) > 0:
        os.remove(perguruantinggi.logo.path)
        perguruantinggi.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('manage_perguruan_tinggi')
        

def edit_perguruantinggi(request,perguruantinggi_id):
    perguruantinggi = PerguruanTinggi.objects.get(id=perguruantinggi_id)

    if request.method == 'POST':
        form = UpdatePerguruanTinggiForm(request.POST,request.FILES,instance=perguruantinggi)
        if len(request.FILES) !=0:
            if len(perguruantinggi.logo) > 0:
                os.remove(perguruantinggi.logo.path)
                if form.is_valid():
                    # perguruantinggi = PerguruanTinggi(nama=namapt,nosk=nomorsk,logo=logo)
                    form.save()
                    messages.success(request,'Data Perguruan Tinggi Ditambah! ')
                    return redirect('manage_perguruan_tinggi')
                else:
                    messages.error(request,'Gagal Tambah Data!!!')
                    return redirect('manage_perguruan_tinggi')
    else:
        form = UpdatePerguruanTinggiForm(instance=perguruantinggi)
    context={
        'form':form,
    }
    return render(request,'hod_template/edit_perguruantinggi_template.html',context)

#fakultas 
def manage_fakultas(request):
    fakultas = Fakultas.objects.all()

    if request.method == 'POST':
        if request.method == "POST":
            form = CreateFakultasForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Data Fakultas Disimpan!')
                return redirect('manage_fakultas')
    else:
        form = CreateFakultasForm()

    context = {
        'fakultas':fakultas,
        'form':form,
    }
    return render(request,'hod_template/manage_fakultas_template.html',context)

def hapus_fakultas(request,fakultas_id):
    fakultas = Fakultas.objects.get(id=fakultas_id)
    fakultas.delete()
    messages.success(request,'Data Dihapus!')
    return redirect('manage_fakultas')    

def update_fakultas(request,fakultas_id):
    fakultas = Fakultas.objects.get(id=fakultas_id)

    if request.method == "POST":
        form = UpdateFakultasForm(request.POST,instance=fakultas)
        if form.is_valid():
            form.save()
            messages.success(request,'Data Diupdate!')
            return redirect('manage_fakultas')
    else:
        form = UpdateFakultasForm(instance=fakultas)
    context={
        'form':form,
    }
    return render(request,'hod_template/edit_fakultas_template.html',context)

#program studi

def manage_programstudi(request):
    programstudi = ProgramStudi.objects.all()

    if request.method == "POST":
        form = CreateProgramStudiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Data Disimpan!')
            return redirect('manage_programstudi')
    else:
         form = CreateProgramStudiForm()
    context={
        'form':form,
        'programstudi':programstudi,
    }
    return render(request,'hod_template/manage_programstudi_template.html',context)

def update_programstudi(request,programstudi_id):
    programstudi = ProgramStudi.objects.get(id=programstudi_id)

    if request.method == "POST":
        form = UpdateProgramStudiForm(request.POST,request.FILES,instance=programstudi)
        if len(request.FILES) != 0:
            if len(programstudi.images) > 0:
                os.remove(programstudi.images.path)
                if form.is_valid():
                    form.save()
                    messages.success(request,'Data Diupdate!')
                    return redirect('manage_programstudi')
                else:
                    messages.success(request,'Gagal Update!')
                    return redirect('manage_programstudi')
    else:
        form = UpdateProgramStudiForm(instance=programstudi)

    context={
        'form':form,
        'programstudi':programstudi,
    }
    return render(request,'hod_template/edit_programstudi_template.html',context)

def view_programstudi_detail(request,programstudi_id):
    programstudi = ProgramStudi.objects.get(id=programstudi_id)
    context={
        'programstudi':programstudi,
    }
    return render(request,'hod_template/view_detail_programstudi_template.html',context)


#Staff
def manage_staff(request):
    staff = Staff.objects.all()
    
    context = {
        'staff':staff,
    }
    return render(request,'hod_template/manage_staff_template.html',context)

def add_staff(request):
    programstudi = ProgramStudi.objects.all()
    form = CreateUserForm()
    form_mahasiswa = CreatemahasiswaForm()
    return render(request,'hod_template/add_staff_template.html',{'prodi':programstudi,'form':form,'form_mahasiswa':form_mahasiswa})

def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    
    else:
        #first_name = request.POST.get('first_name')
        #last_name = request.POST.get('last_name')
        #username = request.POST.get('username')
        #email = request.POST.get('email')
        #password = request.POST.get('password')
        #address = request.POST.get('address')
        #programstudi = ProgramStudi.objects.get(id=request.POST.get('programstudi'))
        form_user = CreateUserForm(request.POST)
        form_mahasiswa=CreatemahasiswaForm(request.POST)
        try:

           # user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
           # user.staff.address=address
           # user.staff.programstudi=programstudi
            #user.save()
            if form_user.is_valid() and form_mahasiswa.is_valid():
                messages.success(request, "Data Staff Di Tambah!")
                return redirect('add_staff')
            else:
                messages.error(request, "Data Staff gagal Di Tambah!")
                return redirect('add_staff')
        except:
            messages.error(request, "Data Staff gagal Di Tambah!")
            return redirect('add_staff')

def edit_staff(request,staff_id):
    staff = Staff.objects.get(admin=staff_id)
    prodi = ProgramStudi.objects.all()
    context={
        'staff':staff,
        'id':staff_id,
        'prodi':prodi,
    }
    return render(request,'hod_template/edit_staff_template.html',context)

def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        programstudi = ProgramStudi.objects.get(id=request.POST.get('programstudi'))

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Staff Model
            staff_model = Staff.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.programstudi = programstudi
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('manage_staff')

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)



def hapus_staff(request,staff_id):
    staff = Staff.objects.get(admin=staff_id)
    user = CustomUser.objects.get(id=staff_id)
    try:
        staff.delete()
        user.delete()
        messages.success(request, "Data Staff Dihapus")
        return redirect('manage_staff')
    except:
        messages.error(request, "Data Staff gagal di hapus!")
        return redirect('manage_staff')

def manage_mahasiswa(request):
    mahasiswa = Mahasiswa.objects.all()
    return render(request,'hod_template/manage_mahasiswa_template.html',{'mahasiswa':mahasiswa})

def add_mahasiswa(request):
    prodi = ProgramStudi.objects.all()
    return render(request,'hod_template/add_mahasiswa_template.html',{'prodi':prodi})

def add_mahasiswa_save(request):
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
        programstudi = ProgramStudi.objects.get(id=request.POST.get('programstudi'))

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.mahasiswa(address=address,nim=nim,tempatlahir=tempatlahir,tgllahir=tgllahir,prodi=programstudi)
            user.save()
            messages.success(request, "Data Mahasiswa Di Tambah!")
            return redirect('add_mahasiswa')
        except:
            messages.error(request, "Data Mahasiswa gagal Di Tambah!")
            return redirect('add_mahasiswa')




def manage_gelar(request):
    gelar = Gelar.objects.all()

    if request.method == 'POST':
        form = CreateGelarfForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Di Tambah!")
            return redirect('manage_gelar')
    else:
        form = CreateGelarfForm()
    
    context={
        'gelar':gelar,
        'form':form,
    }

    return render(request,'hod_template/manage_gelar_template.html',context)

def update_gelar(request,gelar_id):
    gelar = Gelar.objects.get(id=gelar_id)
    if request.method == 'POST':
        form = UpdateGelarfForm(request.POST,instance=gelar)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Di Update!")
            return redirect('manage_gelar')
    else:
        form = UpdateGelarfForm(instance=gelar)
    context={
        'form':form,
    }
    return render(request,'hod_template/update_gelar_template.html',context)

def manage_cpl(request):    
    cpl = Cpl.objects.all()

    if request.method == 'POST':
        form = CreateCplForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Di Simpan!")
            return redirect('manage_cpl')
    else:
        form = CreateCplForm()
 
    context={
        'form':form,
        'cpl':cpl,
    }

    return render (request,'hod_template/manage_cpl_template.html',context)

def update_cpl(request,cpl_id):
    cpl = Cpl.objects.get(id=cpl_id)

    if request.method == 'POST':
        form = UpdateCplForm(request.POST,instance=cpl)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Di Update!")
            return redirect('manage_cpl')
    else:
        form = UpdateCplForm(instance=cpl)

    context={
        'form':form,
    }
    return render(request,'hod_template/edit_cpl_template.html',context)

def hapus_cpl(request,cpl_id):
    cpl = Cpl.objects.get(id=cpl_id)
    cpl.delete()
    messages.success(request, "Data Di Hapus")
    return redirect('manage_cpl')


def manage_subcpl(request):    
    subcpl = SubAspekCpl.objects.all()

    if request.method == 'POST':
        form = CreateSubCplForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Di Simpan!")
            return redirect('manage_subcpl')
    else:
        form = CreateSubCplForm()

    context={
        'form':form,
        'subcpl':subcpl,
    }

    return render (request,'hod_template/manage_subcpl_template.html',context)

def update_subcpl(request,subcpl_id):
    subcpl = SubAspekCpl.objects.get(id=subcpl_id)

    if request.method == 'POST':
        form = UpdateSubCplForm(request.POST,instance=subcpl)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Di Update!")
            return redirect('manage_subcpl')
    else:
        form = UpdateSubCplForm(instance=subcpl)

    context={
        'form':form,
        'subcpl':subcpl,
    }
    return render(request,'hod_template/edit_subcpl_template.html',context)

def hapus_subcpl(request,subcpl_id):
    subcpl = SubAspekCpl.objects.get(id=subcpl_id)
    subcpl.delete()
    messages.success(request, "Data Di Hapus")
    return redirect('manage_subcpl')


#organisasi
def manage_organisasi(request):
    organisasi = Organisasi.objects.all()

    if request.method == 'POST':
        form = CreateOrganisasiForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Data Disimpan.')
            return redirect('organisasi-index')
    else:
        form = CreateOrganisasiForm(request.FILES)

    context = {
        'form':form,
        'organisasi':organisasi,
    }
    return render(request,'skpi/organisasi/index.html',context)






@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

