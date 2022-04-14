from unicodedata import name
from django.urls import path

from skpi_management_app import StaffViews, StudentViews,adminHome
from . import views



urlpatterns = [
    path('',views.loginPage,name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('update_user/<int:user_id>/',adminHome.update_user,name='update_user'),
    path('view_user_staff/<int:user_id>/',adminHome.view_user_staff,name='view_user_staff'),
    path('view_user_mahasiswa/<int:user_id>/',adminHome.view_user_mahasiswa,name='view_user_mahasiswa'),
    path('get_user_details/',views.get_user_details,name='get_user_details'),
    path('admin_home/',adminHome.admin_home,name='admin-home'),
    path('admin_profile/',adminHome.admin_profile,name='admin_profile'),
    path('check_email_exist/', adminHome.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', adminHome.check_username_exist, name="check_username_exist"),

    #perguruan tinggi
    path('manage_perguruan_tinggi/',adminHome.manage_perguruantinggi,name='manage_perguruan_tinggi'),
    path('hapus_perguruan_tinggi/<int:perguruantinggi_id>/',adminHome.hapus_perguruantinggi,name='hapus_perguruan_tinggi'),
    path('update_perguruan_tinggi/<int:perguruantinggi_id>/update',adminHome.edit_perguruantinggi,name='edit_perguruan_tinggi'),
    path('manage_fakultas/',adminHome.manage_fakultas,name='manage_fakultas'),
    path('hapus_fakultas/<int:fakultas_id>/',adminHome.hapus_fakultas,name='hapus_fakultas'),
    path('update_fakultas/<int:fakultas_id>/',adminHome.update_fakultas,name='update_fakultas'),
    path('manage_programstudi/',adminHome.manage_programstudi,name='manage_programstudi'),
    path('update_programstudi/<int:programstudi_id>',adminHome.update_programstudi,name='update_programstudi'),
    path('view_programstudi_detail/<int:programstudi_id>/',adminHome.view_programstudi_detail,name='view_programstudi_detail'),

    #staff/admin
    path('manage_staff/',adminHome.manage_staff,name='manage_staff'),
    path('add_staff/',adminHome.add_staff,name='add_staff'),
    path('add_staff_save/',adminHome.add_staff_save,name="add_staff_save"),
    path('edit_staff/<int:staff_id>/',adminHome.edit_staff,name="edit_staff"),
    path('hapus_staff/<int:staff_id>/',adminHome.hapus_staff,name='hapus_staff'),
    path('view_user_staff/<int:staff_id>/',adminHome.view_user_staff,name='view_user_staff'),

    

    #mahasiswa/admin
    path('manage_mahasiswa/',adminHome.manage_mahasiswa,name='manage_mahasiswa'),
    path('manage_user_mahasiswa/',adminHome.manage_user_mahasiswa,name='manage_user_mahasiswa'),
    path('add_mahasiswa/',adminHome.add_mahasiswa,name='add_mahasiswa'),
    path('add_mahasiswa_save/', adminHome.add_mahasiswa_save,name='add_mahasiswa_save'),
    path('hapus_mahasiswa/<int:mahasiswa_id>/',adminHome.hapus_mahasiswa,name='hapus_mahasiswa'),
    path('update_mahasiswa/<int:user_id>/',adminHome.update_mahasiswa,name='update_mahasiswa'),

    #mahasiswa/
    path('mahasiswa_home/',StudentViews.student_home,name='student_home'),
    path('student_view/',StudentViews.view_mahasiswa,name='student_view'),

    #gelar
    path('manage_gelar/',adminHome.manage_gelar,name='manage_gelar'),
    path('update_gelar/<int:gelar_id>/',adminHome.update_gelar,name='update_gelar'),
    path('manage_cpl/',adminHome.manage_cpl,name='manage_cpl'),
    path('update_cpl/<int:cpl_id>/',adminHome.update_cpl,name='update_cpl'),
    path('hapus_cpl/<int:cpl_id>/',adminHome.hapus_cpl,name='hapus_cpl'),
    path('manage_subcpl/',adminHome.manage_subcpl,name='manage_subcpl'),
    path('update_subcpl/<int:subcpl_id>/',adminHome.update_subcpl,name='update_subcpl'),
    path('hapus_subcpl/<int:subcpl_id>/',adminHome.hapus_subcpl,name='hapus_subcpl'),

    #staff
    path('staff_home/',StaffViews.staff_home,name='staff-home'),
    path('staff_manage_mahasiswa/',StaffViews.manage_mahasiswa,name='staff_manage_mahasiswa'),
    path('staff_add_mahasiswa/',StaffViews.add_mahasiswa,name='staff_add_mahasiswa'),
    path('staff_add_mahasiswa_save/', StaffViews.add_mahasiswa_save,name='staff_add_mahasiswa_save'),
    path('staff_hapus_mahasiswa/<int:mahasiswa_id>/',StaffViews.hapus_mahasiswa,name='staff_hapus_mahasiswa'),
    path('staff_check_email_exist/', StaffViews.staff_check_email_exist, name="staff_check_email_exist"),
    path('staff_check_username_exist/', StaffViews.staff_check_username_exist, name="staff_check_username_exist"),
    path('staff_update_mahasiswa/<int:user_id>/',StaffViews.update_mahasiswa,name='staff_update_mahasiswa'),
    path('staff_skpi_mahasiswa/<int:user_id>/',StaffViews.view_mahasiswa_skpi,name='staff_skpi_mahasiswa'),


    #pelatihan/admin
    path('manage_pelatihan/',adminHome.manage_pelatihan,name='manage_pelatihan'),
    path('add_pelatihan/',adminHome.add_pelatihan,name='add_pelatihan'),
    path('add_pelatihan_save/', adminHome.add_pelatihan_save,name='add_pelatihan_save'),
    path('hapus_pelatihan/<int:pelatihan_id>/', adminHome.hapus_pelatihan,name='hapus_pelatihan'),
    path('update_pelatihan/<int:pelatihan_id>/', adminHome.update_pelatihan,name='update_pelatihan'),

    #pelatihan/mahasiswa
    path('mahasiswa_pelatihan/',StudentViews.mahasiswa_manage_pelatihan,name='mahasiswa_manage_pelatihan'),
    path('mahasiswa_add_pelatihan/',StudentViews.mahasiswa_add_pelatihan,name='mahasiswa_add_pelatihan'),
    path('mahasiswa_add_pelatihan_save/',StudentViews.mahasiswa_add_pelatihan_save,name='mahasiswa_add_pelatihan_save'),
    path('mahasiswa_hapus_pelatihan/<int:pelatihan_id>/', StudentViews.mahasiswa_hapus_pelatihan,name='mahasiswa_hapus_pelatihan'),
    path('mahasiswa_update_pelatihan/<int:pelatihan_id>/', StudentViews.mahasiswa_update_pelatihan,name='mahasiswa_update_pelatihan'),

    #prestasi/admin
    path('manage_prestasi',adminHome.manage_prestasi,name='manage_prestasi'),
    path('add_prestasi/',adminHome.add_prestasi,name='add_prestasi'),
    path('add_prestasi_save/', adminHome.add_prestasi_save,name='add_prestasi_save'),
    path('hapus_prestasi/<int:prestasi_id>/', adminHome.hapus_prestasi,name='hapus_prestasi'),
    path('update_prestasi/<int:prestasi_id>/', adminHome.update_prestasi,name='update_prestasi'),

    #prestasi/mahasiswa
    path('mahasiswa_manage_prestasi',StudentViews.mahasiswa_manage_prestasi,name='mahasiswa_manage_prestasi'),
    path('mahasiswa_add_prestasi/',StudentViews.mahasiswa_add_prestasi,name='mahasiswa_add_prestasi'),
    path('mahasiswa_add_prestasi_save/',StudentViews.mahasiswa_add_prestasi_save,name='mahasiswa_add_prestasi_save'),
    path('mahasiswa_hapus_prestasi/<int:prestasi_id>/', StudentViews.mahasiswa_hapus_prestasi,name='mahasiswa_hapus_prestasi'),
    path('mahasiswa_update_prestasi/<int:prestasi_id>/', StudentViews.mahasiswa_update_prestasi,name='mahasiswa_update_prestasi'),



   


]
