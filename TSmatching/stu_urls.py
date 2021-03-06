from django.conf.urls import url 
from . import stu_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^edit', stu_view.stu_edit, name='stu_edit'),
    url(r'^main', stu_view.main_page, name='stu_main'),
    url(r'^login',stu_view.stu_login, name='stu_login'),
    url(r'^register',stu_view.stu_register, name='stu_register'),
    url(r'^select',stu_view.select_teacher, name='stu_select'),
    url(r'^logout',stu_view.log_out, name='logout'),
    url(r'^password_change',stu_view.password_change, name='password_change'),
    url(r'^code_img',stu_view.create_code_image,name='code')
]