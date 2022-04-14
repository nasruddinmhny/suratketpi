
from distutils.command.clean import clean
from django import forms
from .models import Cpl, CustomUser, KonfirmasiData, Mahasiswa, Organisasi, Pelatihan, PerguruanTinggi,Fakultas, Prestasi, ProgramStudi, Staff,Gelar, SubAspekCpl
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput
#form perguruan tinggi
class CreatePerguruanTinggiForm(forms.ModelForm):
    class Meta:
        model = PerguruanTinggi
        fields = '__all__'

class UpdatePerguruanTinggiForm(forms.ModelForm):
    class Meta:
        model = PerguruanTinggi
        fields = '__all__'
#update customeuser
class UpdateCustomeuseForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email']
        #exclude = ['user_type']

#form fakultas
class CreateFakultasForm(forms.ModelForm):
    class Meta:
        model = Fakultas
        fields = '__all__'

class UpdateFakultasForm(forms.ModelForm):
    class Meta:
        model = Fakultas
        fields = '__all__'

#programstudi
class CreateProgramStudiForm(forms.ModelForm):
    class Meta:
        model = ProgramStudi
        fields = '__all__'

class UpdateProgramStudiForm(forms.ModelForm):
    class Meta:
        model = ProgramStudi
        fields = '__all__'

#staff
class CreateStaffForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    

    class Meta:
        model = Staff
        exclude=['admin']

    def save(self, commit=True):
        user = super(CreateStaffForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data['address']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password']

        if commit:
            user.save()
        return user

class UpdateStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['address','programstudi']

class UpdateMAhasiswaForm(forms.ModelForm):

    tgllahir = forms.DateField(label='Tgl. Lahir',widget=NumberInput(attrs={'type': 'date'}))
    tglmasukkuliah = forms.DateField(label='Tgl. Masuk Kuliah',widget=NumberInput(attrs={'type': 'date'}))
    tglluluskuliah = forms.DateField(label='Tgl. Lulus Kuliah',widget=NumberInput(attrs={'type': 'date'}))
    tempatlahir = forms.CharField(label='Temp. Lahir')
    address = forms.CharField(label='Alamat')

    class Meta:
        model = Mahasiswa
        fields = ['nim','gender','tgllahir','tempatlahir','programstudi','address','noseriijazah','tglmasukkuliah','tglluluskuliah','gelar']

        

#gelar
class CreateGelarfForm(forms.ModelForm):
    class Meta:
        model = Gelar
        fields = '__all__'

class UpdateGelarfForm(forms.ModelForm):
    class Meta:
        model = Gelar
        fields = '__all__'

#cpl
class CreateCplForm(forms.ModelForm):
    class Meta:
        model = Cpl
        fields = '__all__'

class UpdateCplForm(forms.ModelForm):
    class Meta:
        model = Cpl
        fields = '__all__'

#cpl
class CreateSubCplForm(forms.ModelForm):
    class Meta:
        model = SubAspekCpl
        fields = '__all__'

class UpdateSubCplForm(forms.ModelForm):
    class Meta:
        model = SubAspekCpl
        fields = '__all__'

#organisasi
class CreateOrganisasiForm(forms.ModelForm):
    class Meta:
        model = Organisasi
        fields = '__all__'
        #fields = ['nama','periode','jabatan','berkaspendukung','images']

class UpdateOrganisasiForm(forms.ModelForm):
    class Meta:
        model = Organisasi
        fields = '__all__'

class CreateCustomUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2','first_name','last_name']

    def clean(self):
        cleaned_data = super().clean()

        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError('Password tidak sesuai!')
        return cleaned_data
        

    def clean_email(self):
        cleaned_data = super().clean()

        email1 = cleaned_data.get('email')
        if CustomUser.objects.filter(email=email1):
            raise forms.ValidationError("Email Sudah Ada!")
        return email1

    def clean_username(self):
        cleaned_data = super().clean()

        username1 = cleaned_data.get('username')
        if CustomUser.objects.filter(username=username1):
            raise forms.ValidationError("username Sudah Ada!")
        return username1



class CreatePelatihanForm(forms.ModelForm):
    class Meta:
        model = Pelatihan
        fields = ['kegiatan','tglpelatihan','penyelenggara','status','image','mahasiswa']

    try:
        mahasiswa = Mahasiswa.objects.select_related('admin__first_name')
        mahasiswa_list = []
        for mhs in mahasiswa:
            mahasiswa_single = (mhs.id,mhs.nim)
            mahasiswa_list.append(mahasiswa_single)
    except:
         mahasiswa_list = []

    mahasiswa = forms.ChoiceField(label="mahasiswa", choices=mahasiswa_list, widget=forms.Select(attrs={"class":"form-control"}))

    tglpelatihan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date','Labels':'Tgl. Masuk'}))

class UpdatePelatihanForm(forms.ModelForm):
    class Meta:
        model = Pelatihan
        fields = '__all__'
        
    #image = forms.ImageField(label='Image',widget = FileInput())
    tglpelatihan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date','Labels':'Tgl. Masuk'}))

#prestasi
class CreatePrestasiForm(forms.ModelForm):
    tglkegiatan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Prestasi
        fields = '__all__'

class UpdatePrestasiForm(forms.ModelForm):
    tglkegiatan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Prestasi
        fields = '__all__'


#area mahasiswa
class CreatePelatihanMhsForm(forms.ModelForm):
    class Meta:
        model = Pelatihan
        exclude = ['mahasiswa']
        
    
   
    tglpelatihan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date','Labels':'Tgl. Masuk'}))

class UpdatePelatihanMhsForm(forms.ModelForm):
    class Meta:
        model = Pelatihan
        exclude = ['mahasiswa']
        
    #image = forms.ImageField(label='Image',widget = FileInput())
    tglpelatihan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date','Labels':'Tgl. Masuk'}))

class CreatePrestasiMhsForm(forms.ModelForm):
    tglkegiatan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Prestasi
        exclude = ['mahasiswa']

class UpdatePrestasiMhsForm(forms.ModelForm):
    tglkegiatan = forms.DateField(label='Tanggal',widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Prestasi
        exclude = ['mahasiswa']

class CreateKonfirmasiData(forms.ModelForm):
    class Meta:
        model = KonfirmasiData
        exclude = ['mahasiswa']