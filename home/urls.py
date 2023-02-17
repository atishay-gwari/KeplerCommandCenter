from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.Home,name='home'),
    path('fileiploader/',views.FileUploader,name='uploader'),
    path('converttodb/',views.csvconverter,name='csv'),
    path('table/',views.table,name='table'),
    path('profile/',views.profile,name='profile'),
    path('login/', views.loginpage,name="login"),
    path('logout/',views.logoutpage,name='logout'),
    path('signup/', views.signuppage,name="signup"),
    path('sales/', views.CovertedToDB_list, name='dblist'),
    path('delete/<str:id>/', views.deletefiles,name="delete"),
    path('update/<str:id>/', views.updatefiles,name="update")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
