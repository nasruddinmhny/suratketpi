
import os
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Count,Sum,Q
import json
from .forms import CreateCplForm, CreateCustomUserForm, CreateGelarfForm, CreateKonfirmasiData, CreateOrganisasiForm, CreatePelatihanForm, CreatePerguruanTinggiForm, CreatePrestasiForm, CreateStaffForm, CreateSubCplForm, UpdateCplForm, UpdateCustomeuseForm, UpdateGelarfForm, UpdateMAhasiswaForm, UpdatePelatihanForm, UpdatePerguruanTinggiForm,CreateFakultasForm,UpdateFakultasForm,CreateProgramStudiForm, UpdatePrestasiForm,UpdateProgramStudiForm, UpdateStaffForm, UpdateSubCplForm
from .models import Cpl, CustomUser, Fakultas, Gelar, KonfirmasiData, Organisasi, Pelatihan, PerguruanTinggi, Prestasi, ProgramStudi,Staff,Mahasiswa, SubAspekCpl


def admin_home(request):
    all_mahasiswa_count = Mahasiswa.objects.all().count()
    prodi_count = ProgramStudi.objects.all().count()
    prodi = ProgramStudi.objects.all()
    valid_count_data = KonfirmasiData.objects.values('setuju').annotate(count_data=Count('setuju'))
    invalid_count_data = 0
    all_perguruantinggi_count = PerguruanTinggi.objects.all().count()
    mahasiswa_count_prodi = Mahasiswa.objects.values('programstudi','programstudi__nama').annotate(count=Count('programstudi'))
    print(valid_count_data)

    context={
        'all_mahasiswa_count':all_mahasiswa_count,
        'all_perguruantinggi_count':all_perguruantinggi_count,
        'mahasiswa_count_prodi':mahasiswa_count_prodi,
        'prodi':prodi,
        'prodi_count':prodi_count,
        'valid_count_data':valid_count_data,
        'invalid_count_data':invalid_count_data,


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
    form_user = CreateCustomUserForm()
    
    return render(request,'hod_template/add_staff_template.html',{'prodi':programstudi,'form_user':form_user,})

def add_staff_save(request):
  
    if request.method == 'POST':
        form_user = CreateCustomUserForm(request.POST)  
        if form_user.is_valid():
            userForm = form_user.save(commit=False)
            userForm.user_type = 2
            userForm.save()
            messages.success(request,'Data Disimpan')  
            return redirect('add_staff')
    else:
        form_user = CreateCustomUserForm()
        
    context = {
        'form_user':form_user,
        
    }
    return render(request,'hod_template/add_staff_template.html',context)
        

def edit_staff(request,staff_id):
    staff = Staff.objects.get(id=staff_id)
    print(staff)
    if request.method == 'POST':
        form = UpdateStaffForm(request.POST,instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Staff Diupdate")
            return redirect('manage_staff')
    else:
        form = UpdateStaffForm(instance=staff)
    context={
    
        'form':form,
    }
    return render(request,'hod_template/edit_staff_template.html',context)


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
    form_mahasiswa = CreateCustomUserForm()
    context={
        'form_mahasiswa':form_mahasiswa,
        
    }
    return render(request,'hod_template/add_mahasiswa_template.html',context)

def add_mahasiswa_save(request):
    if request.method == 'POST':
        form_mahasiswa = CreateCustomUserForm(request.POST)  
        if form_mahasiswa.is_valid():
            userForm = form_mahasiswa.save(commit=False)
            userForm.user_type = 3 
            #userForm.programstudi_id = ProgramStudi.objects.get(id=1)
            userForm.save()
            messages.success(request,'Data User Disimpan')  
            return redirect('add_mahasiswa')
    else:
        form_mahasiswa = CreateCustomUserForm() 
        
    context = {
        'form_mahasiswa':form_mahasiswa,
        
    }
    return render(request,'hod_template/add_mahasiswa_template.html',context)
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
def update_mahasiswa(request,user_id):
    mahasiswa= Mahasiswa.objects.get(admin=user_id)
   
    if request.method == 'POST':
        form_mahasiswa = UpdateMAhasiswaForm(request.POST,instance=mahasiswa)
        if form_mahasiswa.save():
            messages.success(request, "Data Di update")
            return redirect('manage_mahasiswa')
        #else:
            #messages.error(request, "Data gagal update")
            #return redirect('update_mahasiswa',mahasiswa.admin.id)
    else:
        
        form_mahasiswa = UpdateMAhasiswaForm(instance=mahasiswa)


    context={
        'form_mahasiswa':form_mahasiswa,
    }
    return render(request,'hod_template/edit_mahasiswa_template.html',context)

def manage_user_mahasiswa(request):
    mahasiswa = Mahasiswa.objects.all()
    return render(request,'hod_template/manage_user_mahasiswa_template.html',{'mahasiswa':mahasiswa})


def hapus_mahasiswa(request,mahasiswa_id):
    mahasiswa = Mahasiswa.objects.get(admin=mahasiswa_id)
    user = CustomUser.objects.get(id=mahasiswa_id)
    try:
        mahasiswa.delete()
        user.delete()
        messages.success(request, "Data Mahasiswa Dihapus")
        return redirect('manage_mahasiswa')
    except:
        messages.error(request, "Data mahasiswa gagal di hapus!")
        return redirect('manage_mahasiswa')


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

#update data user
def update_user(request,user_id):
    customuser = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        form = UpdateCustomeuseForm(request.POST,instance=customuser)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Data Di Hapus")
            return redirect('admin_home')


def view_user_staff(request,user_id):
    customuser = CustomUser.objects.get(id=user_id)
    staff = Staff.objects.get(admin=user_id)

    if request.method == 'POST':
        form = UpdateCustomeuseForm(request.POST,instance=customuser)
        form_staff = UpdateStaffForm(request.POST,instance=staff)
        if form.is_valid() and form_staff.is_valid():
            form.save()
            form_staff.save()
            messages.success(request, "Data Di update")
            return redirect('view_user',customuser.id)
        else:
            messages.error(request, "Data gagal update")
            return redirect('view_user',customuser.id)
    else:
        form = UpdateCustomeuseForm(instance=customuser)
        form_staff = UpdateStaffForm(instance=staff)


    context={
        'customuser':customuser,
        'form':form,
        'form_staff':form_staff,
    }
    return render(request,'hod_template/view_user_template.html',context)

def view_user_mahasiswa(request,user_id):
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
    return render(request,'hod_template/view_mahasiswa_template.html',context)

def manage_pelatihan(request):
    pelatihan = Pelatihan.objects.all()
    pel = Pelatihan.objects.select_related('mahasiswa').all()
    

    context = {
        'pelatihan':pelatihan,
    }
    return render(request,'hod_template/manage_pelatihan_template.html',context)

def add_pelatihan(request):
    form_pelatihan = CreatePelatihanForm()  
    print(form_pelatihan)  
    context = {
        'form_pelatihan':form_pelatihan,
    }
    return render(request,'hod_template/add_pelatihan_template.html',context)

def add_pelatihan_save(request):
    if request.method == 'POST':
        form_pelatihan = CreatePelatihanForm(request.POST,request.FILES)
        if form_pelatihan.is_valid():
            form_pelatihan.save()
            messages.success(request, "Data Disimpan!")
            return redirect('manage_pelatihan')
    else:
        form_pelatihan = CreatePelatihanForm(request.FILES)
    context = {
        'form_pelatihan':form_pelatihan,
    }
    return render(request,'hod_template/add_pelatihan_template.html',context)

def hapus_pelatihan(request,pelatihan_id):
    pelatihan = Pelatihan.objects.get(id=pelatihan_id)

    if len(pelatihan.image) > 0:
        os.remove(pelatihan.image.path)
        pelatihan.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('manage_pelatihan')
    else:
        pelatihan.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('manage_pelatihan')

def update_pelatihan(request,pelatihan_id):

    pelatihan = Pelatihan.objects.get(id=pelatihan_id)

    if request.method == 'POST':
        form_pelatihan = UpdatePelatihanForm(request.POST,request.FILES,instance=pelatihan)
        if len(request.FILES) !=0 :
            if len(pelatihan.image) > 0:
                os.remove(pelatihan.image.path)
                if form_pelatihan.is_valid():
                    form_pelatihan.save()
                    messages.success(request, 'Data Diupdate.')
                    return redirect('update_pelatihan',pelatihan.id)
            
    else:
        form_pelatihan = UpdatePelatihanForm(instance=pelatihan)
    context={
        'form_pelatihan':form_pelatihan,
    }
    return render(request,'hod_template/edit_pelatihan_template.html',context)


def manage_prestasi(request):
    prestasi = Prestasi.objects.all()

    if request.method == 'POST':
        form = CreatePrestasiForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Disimpan.')
            return redirect('manage_prestasi')
    else:
        form = CreatePrestasiForm()

    context={
        'form':form,
        'prestasi':prestasi,
    }
    return render(request,'hod_template/manage_prestasi_template.html', context)

def add_prestasi(request):
    form = CreatePrestasiForm()    
    context = {
        'form':form,
    }
    return render(request,'hod_template/add_prestasi_template.html',context)

def add_prestasi_save(request):
    if request.method == 'POST':
        form_prestasi = CreatePrestasiForm(request.POST,request.FILES)
        if form_prestasi.is_valid():
            form_prestasi.save()
            messages.success(request, "Data Disimpan!")
            return redirect('add_prestasi')

    else:
        form_prestasi = CreatePrestasiForm(request.FILES)
    context = {
        'form_prestasi':form_prestasi,
    }
    return render(request,'hod_template/add_prestasi_template.html',context)

def hapus_prestasi(request,prestasi_id):
    prestasi = Prestasi.objects.get(id=prestasi_id)

    if len(prestasi.images) > 0:
        os.remove(prestasi.images.path)
        prestasi.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('manage_prestasi')
    else:
        prestasi.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('manage_prestasi')

def update_prestasi(request,prestasi_id):
    
    prestasi = Prestasi.objects.get(id=prestasi_id)

    if request.method == 'POST':
        form_prestasi = UpdatePrestasiForm(request.POST,request.FILES,instance=prestasi)
        if len(request.FILES) !=0 :
            if len(prestasi.images) > 0:
                os.remove(prestasi.images.path)
                if form_prestasi.is_valid():
                    form_prestasi.save()
                    messages.success(request, 'Data Diupdate.')
                    return redirect('update_prestasi',prestasi.id)
            
    else:
        form_prestasi = UpdatePrestasiForm(instance=prestasi)
    context={
        'form_prestasi':form_prestasi,
    }
    return render(request,'hod_template/edit_prestasi_template.html',context)

def manage_organisasi(request):
    organisasi = Organisasi.objects.all()

    context = {
        'organisasi':organisasi,
    }
    return render(request,'hod_template/manage_organisasi_template.html',context)

def viewdataskpi(request,admin_id):
    mahasiswa = Mahasiswa.objects.select_related('admin').get(admin=admin_id)

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

