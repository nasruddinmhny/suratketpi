import os
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse

from skpi_management_app.forms import CreatePelatihanMhsForm, CreatePrestasiMhsForm, UpdateMAhasiswaForm, UpdatePelatihanMhsForm, UpdatePrestasiMhsForm
from .models import CustomUser, Mahasiswa, Pelatihan, Prestasi




def student_home(request):
    mhs_id = get_object_or_404(Mahasiswa,admin=request.user.id)
    #mahasiswa = get_object_or_404(Mahasiswa,admin=request.user.id)
    mahasiswa = Mahasiswa.objects.get(admin=request.user.id)
    pelatihan = Pelatihan.objects.select_related('mahasiswa').filter(mahasiswa_id=mahasiswa)
    prestasi = Prestasi.objects.select_related('mahasiswa').filter(mahasiswa_id = mahasiswa)

   #Sessions.objects.filter(affiliation_session__ip_id=X)
    customuser = get_object_or_404(CustomUser,id=request.user.id)
   # pelatihan = get_object_or_404(Pelatihan,mahasiswa=mhs_id)

    context={
        'mahasiswa':mahasiswa,
        'customuser':customuser,
        'pelatihan':pelatihan,
        'prestasi':prestasi,
    }
    return render(request,'mahasiswa_template/home_content.html',context)

def view_mahasiswa(request):
    mahasiswa =  mahasiswa = get_object_or_404(Mahasiswa,admin=request.user.id)
    if request.method == 'POST':
        form = UpdateMAhasiswaForm(request.POST,instance=mahasiswa)
        if form.is_valid():
            form.save()
            messages.success(request,'Data Diupdate!')
    
    else:
         form = UpdateMAhasiswaForm(instance=mahasiswa)
    context = {
        'mahasiswa':mahasiswa,
        'form':form,
    } 
    return render(request,'mahasiswa_template/view_mahasiswa_template.html',context)

def mahasiswa_manage_pelatihan(request):
    mahasiswa = Mahasiswa.objects.get(admin=request.user.id)
    pelatihan = Pelatihan.objects.select_related('mahasiswa').filter(mahasiswa_id=mahasiswa)
    print(pelatihan)

    context={
        'pelatihan':pelatihan,
    }
    return render(request,'mahasiswa_template/manage_pelatihan_template.html',context)

def mahasiswa_add_pelatihan(request):
    form_pelatihan = CreatePelatihanMhsForm()
    context={
        'form_pelatihan':form_pelatihan,
    }
    return render(request,'mahasiswa_template/add_pelatihan_template.html',context)

def mahasiswa_add_pelatihan_save(request):
    mhs = Mahasiswa.objects.get(admin_id=request.user.id)
    print(mhs)
    if request.method == 'POST':
        form_pelatihan = CreatePelatihanMhsForm(request.POST, request.FILES)
        if form_pelatihan.is_valid():
            pelatihanForm = form_pelatihan.save(commit=False)
            pelatihanForm.mahasiswa_id = mhs.id
            pelatihanForm.save()
            messages.success(request,'Data Pelatihan Disimpan!')
            return redirect('mahasiswa_add_pelatihan')
        else:
            messages.error(request,'Data Pelatihan Disimpan!')
            return redirect('mahasiswa_add_pelatihan')
    else:
        return redirect('mahasiswa_manage_pelatihan')

def mahasiswa_hapus_pelatihan(request,pelatihan_id):
    pelatihan = Pelatihan.objects.get(id=pelatihan_id)

    if len(pelatihan.image) > 0:
        os.remove(pelatihan.image.path)
        pelatihan.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('mahasiswa_manage_pelatihan')
    else:
        pelatihan.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('mahasiswa_manage_pelatihan')

def mahasiswa_update_pelatihan(request,pelatihan_id):
    
    pelatihan = Pelatihan.objects.get(id=pelatihan_id)

    if request.method == 'POST':
        form_pelatihan = UpdatePelatihanMhsForm(request.POST,request.FILES,instance=pelatihan)
        if len(request.FILES) !=0 :
            if len(pelatihan.image) > 0:
                os.remove(pelatihan.image.path)
                if form_pelatihan.is_valid():
                    form_pelatihan.save()
                    messages.success(request, 'Data Diupdate.')
                    return redirect('mahasiswa_update_pelatihan',pelatihan.id)
            
    else:
        form_pelatihan = UpdatePelatihanMhsForm(instance=pelatihan)
    context={
        'form_pelatihan':form_pelatihan,
    }
    return render(request,'mahasiswa_template/edit_pelatihan_template.html',context)

def mahasiswa_view_pelatihan(request) :
    pass
    
def mahasiswa_manage_prestasi(request):
    mahasiswa = Mahasiswa.objects.get(admin=request.user.id)
    prestasi = Prestasi.objects.select_related('mahasiswa').filter(mahasiswa_id=mahasiswa)

    context={
        'prestasi':prestasi,
    }
    return render(request,'mahasiswa_template/manage_prestasi_template.html', context)  

def mahasiswa_add_prestasi(request):
    form = CreatePrestasiMhsForm()    
    context = {
        'form':form,
    }
    return render(request,'mahasiswa_template/add_prestasi_template.html',context)

def mahasiswa_add_prestasi_save(request):
    mhs = Mahasiswa.objects.get(admin_id=request.user.id)
    if request.method == 'POST':
        form_prestasi = CreatePrestasiMhsForm(request.POST,request.FILES)
        if form_prestasi.is_valid():
            prestasiForm = form_prestasi.save(commit=False)
            prestasiForm.mahasiswa_id = mhs.id
            prestasiForm.save()
            messages.success(request, "Data Disimpan!")
            return redirect('mahasiswa_add_prestasi')

    else:
        form_prestasi = CreatePrestasiMhsForm(request.FILES)
    context = {
        'form_prestasi':form_prestasi,
    }
    return render(request,'mahasiswa_template/add_prestasi_template.html',context)

def mahasiswa_hapus_prestasi(request,prestasi_id):
    prestasi = Prestasi.objects.get(id=prestasi_id)

    if len(prestasi.images) > 0:
        os.remove(prestasi.images.path)
        prestasi.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('mahasiswa_manage_prestasi')
    else:
        prestasi.delete()
        messages.success(request, 'Data Dihapus.')
        return redirect('mahasiswa_manage_prestasi')

def mahasiswa_update_prestasi(request,prestasi_id):
    
    prestasi = Prestasi.objects.get(id=prestasi_id)

    if request.method == 'POST':
        form_prestasi = UpdatePrestasiMhsForm(request.POST,request.FILES,instance=prestasi)
        if len(request.FILES) !=0 :
            if len(prestasi.images) > 0:
                os.remove(prestasi.images.path)
                if form_prestasi.is_valid():
                    form_prestasi.save()
                    messages.success(request, 'Data Diupdate.')
                    return redirect('mahasiswa_update_prestasi',prestasi.id)
            
    else:
        form_prestasi = UpdatePrestasiMhsForm(instance=prestasi)
    context={
        'form_prestasi':form_prestasi,
    }
    return render(request,'mahasiswa_template/edit_prestasi_template.html',context)