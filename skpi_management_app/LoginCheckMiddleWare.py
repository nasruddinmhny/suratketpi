from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse

class LoginCheckMiddleWare(MiddlewareMixin):
   
   def process_view(self, request, view_func, view_args, view_kwargs):
        modulname = view_func.__module__
       #print modul name
        user = request.user

       #check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == '1':

                if modulname == 'skpi_management_app.adminHome':
                    pass
                elif modulname == 'skpi_management_app.views' or modulname == 'django.views.static':
                    pass
                else:
                    return redirect('admin_home')

            elif user.user_type == '2':
    
                if modulname == 'skpi_management_app.StaffViews':
                    pass
                elif modulname == 'skpi_management_app.views' or modulname == 'django.views.static':
                    pass
                else:
                    return redirect('staff-home')

            elif user.user_type == '3':
    
                if modulname == 'skpi_management_app.StudentViews':
                    pass
                elif modulname == 'skpi_management_app.views' or modulname == 'django.views.static':
                    pass
                else:
                    return redirect('student_home')
            
            else:
                return redirect('login')
        else:
            if request.path == reverse('login') or request.path == reverse('doLogin'):
                pass
            else:
                return redirect('login')
