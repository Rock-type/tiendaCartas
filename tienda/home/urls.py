from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.home, name="home"),
    path('registrar',views.registrar, name="registrar"),
    path('login',views.login_usuario, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("prueba2/", views.prueba2, name="vistaYugioh"),
    path('busqueda/', views.busqueda, name='busqueda'),
    path('agregarCarro/', views.agregar_carro, name='agregar_carro'),
    path('carro/', views.carroVista, name='carroVista'),
    path('eliminarProductoCarro/<str:id>/', views.eliminarProductoCarro, name="eliminarProductoCarro"),
    path('eliminarCarro/', views.eliminarCarro, name="eliminarCarro"),
    path('modificarCantidadCarro/<str:id>/<int:cantidad>/', views.modificarCantidadCarro, name="modificarCantidadCarro"),
    path('realizarCompra/', views.realizarCompra, name="realizarCompra"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)