from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import  receiver


# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = (
        (1,'HOD'),
        (2,'Staff'),
        (3,'Mahasiswa'),
    )
    user_type = models.CharField(default=1, choices=user_type_data,max_length=100)
    

class AdminHOD(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class PerguruanTinggi(models.Model):
    nama = models.CharField(max_length=150, null=False, verbose_name='Nama PT')
    nosk = models.CharField(max_length=150, verbose_name='NO SK')
    logo = models.ImageField(upload_to='logo', max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = "Kampus"

    def __str__(self):
        return self.nama

class Fakultas(models.Model):
    nama = models.CharField(max_length=100, null=False, verbose_name='Fakultas')
    namasingkat = models.CharField(max_length=50, blank=True, verbose_name='Singkatan')
    kampus = models.ForeignKey(PerguruanTinggi, on_delete=models.CASCADE, verbose_name='Kampus', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = "Fakultas"

    def __str__(self):
        return self.nama

class ProgramStudi(models.Model):
    kodeprodi = models.CharField(max_length=10, verbose_name='Kode Prodi')
    nama = models.CharField(max_length=150, null=False, verbose_name='Program Studi')
    namasingkat = models.CharField(max_length=150, null=False, verbose_name="Singkatan")
    JENJANG = (
        ('D3','DIPLOMA-3'),
        ('S1','STRATA-1'),
        ('S2','STRATA-2'),
        ('S3','STRATA-3'),
    )
    jenis = models.CharField(max_length=150,verbose_name='Jenis Program Pendidikan',blank=True)
    jenjang = models.CharField(max_length=150, choices=JENJANG, default='1')
    LEVEL = (
        ('1','level 1'),
        ('2','level 2'),
        ('3','level 3'),
        ('4','level 4'),
        ('5','level 5'),
        ('5','level 6'),
    )
    levelkualifikasi = models.CharField(max_length=20, verbose_name='Level Kualifikasi', blank=True,choices=LEVEL)
    persyaratan = models.CharField(max_length=100, verbose_name='Syarat Penerimaan', blank=True)
    noskakreditasi = models.CharField(max_length=20, blank=True, verbose_name='No.SK Akreditasi')
    nilaiakreditasi = models.CharField(max_length=50, verbose_name='Nilai Akreditasi', blank=True)
    lamastudi = models.CharField(max_length=10, verbose_name='Lama Studi', blank=True)
    sistempenilaian = models.TextField(verbose_name='Sistem Penilaian', blank=True)
    BAHASA=(
        ('Indonesia','Indonesia'),
        ('English','English')
    )
    bahasapengantar = models.CharField(max_length=20, verbose_name='Bahasa Pengantar', blank=True, choices=BAHASA)
    LANJUTAN = (
        ('D3','DIPLOMA-3'),
        ('S1','STRATA-1'),
        ('S2','STRATA-2'),
        ('S3','STRATA-3'),
    )
    Pendidikanlanjutan = models.CharField(max_length=50,verbose_name='Pindidikan Lanjut', blank=True,choices=LANJUTAN)
    fakultas = models.ForeignKey(Fakultas,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images_akreditasi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = "Program Studi"
            unique_together = ['kodeprodi']


    def __str__(self):
        return self.nama


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.TextField()
    programstudi = models.ForeignKey(ProgramStudi,on_delete=models.CASCADE, verbose_name="Program Studi",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Cpl(models.Model):
    namaindo = models.CharField(max_length=100, null=False,verbose_name='Aspek')
    namainggris = models.CharField(max_length=100, null=False,verbose_name='Attitude')
    programstudi = models.ForeignKey(ProgramStudi,on_delete=models.CASCADE, verbose_name='Program Studi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = "Capaian Pembelajaran Lulusan"

    def __str__(self):
        return self.namaindo

class SubAspekCpl(models.Model):
    namaindo = models.CharField(max_length=255, null=True,blank=True, verbose_name='Sub Aspek')
    namainggris = models.CharField(max_length=100, null=False,verbose_name='Sub Attitude')
    cpl = models.ForeignKey(Cpl, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = "Sub Aspek Cpl"

    def __str__(self):
        return self.namaindo

class Gelar(models.Model):
    namasingkat = models.CharField(max_length=100, verbose_name='Gelar Singkat')
    nama = models.CharField(max_length=100, verbose_name='Gelar')
    programstudi = models.ForeignKey(ProgramStudi,on_delete=models.CASCADE,default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Gelar Pendidikan"

    def __str__(self):
        return self.namasingkat+" - "+self.nama


class Mahasiswa(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    nim = models.CharField(max_length=30, blank=True,null=True)
    JK = (
        ('LAKI-LAKI','LAKI-LAKI'),
        ('PEREMPUAN','PEREMPUAN'),
    )
    gender = models.CharField(max_length=50,choices=JK)
    address = models.TextField(blank=True,max_length=250,null=True)
    tempatlahir = models.CharField(max_length=200,null=True)
    tgllahir = models.DateField(auto_created=True,null=True)
    noseriijazah = models.CharField(max_length=150, blank=True, verbose_name='No. Seri Ijazah')
    tglmasukkuliah = models.DateField(auto_created=True,verbose_name='Tanggal Masuk', null=True)
    tglluluskuliah = models.DateField(auto_created=True, verbose_name='Tanggal Lulus',null=True)
    gelar = models.ForeignKey(Gelar, on_delete=models.CASCADE, verbose_name='Gelar', default=1)
    programstudi = models.ForeignKey(ProgramStudi,on_delete=models.CASCADE, blank=True, null=True, verbose_name="Program Studi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    class Meta:
        verbose_name_plural = "Mahasiswa"

    def __str__(self):
        return self.nim+" - "+self.admin.first_name
    


class Skpi(models.Model):
    noseriijazah = models.CharField(max_length=150, blank=True, verbose_name='No. Seri Ijazah')
    tglmasukkuliah = models.DateField(auto_created=True,verbose_name='Tanggal Masuk', null=True)
    tglluluskuliah = models.DateField(auto_created=True, verbose_name='Tanggal Lulus',null=True)
    gelar = models.ForeignKey(Gelar, on_delete=models.CASCADE, verbose_name='Gelar', default=1)
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Data SKPI"
    
    def __str__(self):
        return self.mahasiswa.admin

class Prestasi(models.Model):
    namaprestasi = models.CharField(max_length=150, blank=True, verbose_name='Nama Prestasi')
    tglkegiatan = models.DateField(auto_created=True,blank=True, verbose_name='Tanggal')
    penyelenggara = models.CharField(max_length=150, blank=True,verbose_name='Penyelenggara')
    atasnama = models.CharField(max_length=150, blank=True, verbose_name='Atas Nama Pribadi/Instansi')
    LEVEL = (
        ('Lokal','Lokal'),
        ('Nasional','Nasional'),
        ('Internasional','Internasional'),
    )
    tingkat = models.CharField(max_length=50, default='Lokal',choices=LEVEL)
    images = models.ImageField(upload_to='img_prestasi')
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Prestasi"

    def __str__(self):
        return self.namaprestasi
    

class Pelatihan(models.Model):
    kegiatan = models.CharField(max_length=150, blank=True, verbose_name='Kegiatan')
    tglpelatihan = models.DateField(auto_created=True, verbose_name='Tgl. Pelatihan')
    penyelenggara = models.CharField(max_length=150, blank=True, verbose_name='Penyelenggara')
    status = models.CharField(max_length=150,blank=True,verbose_name='Status')
    image= models.ImageField(upload_to='img_pelatihan',null=False, verbose_name='Image')
    mahasiswa = models.ForeignKey(Mahasiswa,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name_plural = "Pelatihan"


    def __str__(self):
        return self.kegiatan

class Organisasi(models.Model):
    nama = models.CharField(max_length=150, blank=True, verbose_name='Nama Organisasi')
    periode = models.CharField(max_length=150, blank=True, verbose_name='Periode')
    jabatan = models.CharField(max_length=150, blank=True, verbose_name='Jabatan')
    berkaspendukung = models.CharField(max_length=150, blank=True, verbose_name='Berkas Pendukung')
    images = models.ImageField(upload_to='img_organisasi', verbose_name='Image',null=False)
    mahasiswa = models.ForeignKey(Mahasiswa,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = "Organisasi"

    def __str__(self):
        return self.nama
        
class KonfirmasiData(models.Model):
    setuju = models.BooleanField(default=False)
    mahasiswa = models.OneToOneField(Mahasiswa,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
            verbose_name_plural = "Konfirmasi Data"

    def __str__(self):
        return self.setuju

#creating django signal
@receiver(post_save,sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Mahasiswa.objects.create(admin=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type== 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.mahasiswa.save()



