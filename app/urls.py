from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.login, name='login'),

    path('registrar/', views.registrar_usuario, name='registrar_usuario'),

    path('panel_usuario/', views.panel_usuario, name='panel_usuario'),

    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),

    path('eliminar_cita/<int:id>/', views.eliminar_cita, name='eliminar_cita'),

    path('panel_admin/', views.panel_admin, name='panel_admin'),

    path("cambiar_estatus/<int:id>/", views.cambiar_estatus, name="cambiar_estatus"),

    path('editar_admin/', views.editar_admin, name='editar_admin'),

    path("reporte_citas/", views.reporte_citas, name="reporte_citas"),

    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),

    path("nueva_password/<uuid:token>/", views.nueva_password, name="nueva_password"),

    path('logout/', views.logout, name='logout'),

    path("recuperar_password/", views.recuperar_password, name="recuperar_password"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )