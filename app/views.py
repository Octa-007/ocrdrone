from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse

from datetime import datetime
from io import BytesIO
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib.styles import getSampleStyleSheet

from django.core.files.storage import FileSystemStorage


from .models import (
    Usuario,
    Administrador,
    Cita,
    RecuperarPassword
)

from datetime import date

# ========================================================== LOGIN ==========================================================
def login(request):

    if request.method == "POST":

        correo = request.POST.get("correo")
        contrasena = request.POST.get("contrasena")


        # -------------------------LOGIN ADMINISTRADOR -------------------------
        admin = Administrador.objects.filter(
            correo_admin=correo
        ).first()


        if admin and check_password(
            contrasena,
            admin.contrasena_admin
        ):

            request.session["admin_id"] = admin.id

            return redirect(
                "panel_admin"
            )


        # ------------------------- LOGIN USUARIO -------------------------

        usuario = Usuario.objects.filter(
            correo=correo
        ).first()


        if usuario and check_password(
            contrasena,
            usuario.contrasena
        ):

            request.session["usuario_id"] = usuario.id

            return redirect(
                "panel_usuario"
            )


        messages.error(
            request,
            "Correo o contraseña incorrectos"
        )

    mostrar_registro = request.session.pop(
    "registro_exitoso",
    False
)

    return render(
        request,
        "login.html"
    )

# ==========================================================
# REGISTRO DE USUARIO
# ==========================================================
def registrar_usuario(request):

    if request.method == "POST":

        try:

            # ==========================
            # OBTENER FECHAS DEL FORMULARIO
            # ==========================

            fecha_dron = request.POST.get("fecha_act_dron")

            fecha_generador = request.POST.get("fecha_act_generador")

            fecha_control = request.POST.get("fecha_act_control")


            # ==========================
            # CONVERTIR FECHAS
            # ==========================

            fecha_dron = datetime.strptime(
                fecha_dron,
                "%Y-%m-%d"
            ).date() if fecha_dron else None


            fecha_generador = datetime.strptime(
                fecha_generador,
                "%Y-%m-%d"
            ).date() if fecha_generador else None


            fecha_control = datetime.strptime(
                fecha_control,
                "%Y-%m-%d"
            ).date() if fecha_control else None

            hoy = date.today()


            # ==========================
            # VALIDAR FECHAS FUTURAS
            # ==========================

            if fecha_dron and fecha_dron > hoy:

                raise ValidationError(
                    "La fecha de activación del dron no puede ser posterior al día actual."
                )


            if fecha_generador and fecha_generador > hoy:

                raise ValidationError(
                    "La fecha de activación del generador no puede ser posterior al día actual."
                )


            if fecha_control and fecha_control > hoy:

                raise ValidationError(
                    "La fecha de activación del control no puede ser posterior al día actual."
                )



            # ==========================
            # CREAR USUARIO
            # ==========================

            usuario = Usuario(

                nombre_completo=request.POST.get(
                    "nombre_completo"
                ),

                correo=request.POST.get(
                    "correo"
                ),

                contrasena=request.POST.get(
                    "contrasena"
                ),

                telefono=request.POST.get(
                    "telefono"
                ),

                domicilio=request.POST.get(
                    "domicilio"
                ),


                foto=None,


                modelo_dron=request.POST.get(
                    "modelo_dron"
                ),

                num_serie_dron=request.POST.get(
                    "num_serie_dron"
                ),

                fecha_act_dron=fecha_dron,


                modelo_generador=request.POST.get(
                    "modelo_generador"
                ),

                num_serie_generador=request.POST.get(
                    "num_serie_generador"
                ),

                fecha_act_generador=fecha_generador,


                num_serie_control=request.POST.get(
                    "num_serie_control"
                ),

                fecha_act_control=fecha_control

            )



            # ==========================
            # GUARDAR FOTO
            # ==========================

            if request.FILES.get("foto"):

                usuario.foto = request.FILES["foto"]



            # ==========================
            # GUARDAR USUARIO
            # ==========================

            usuario.save()



            messages.success(
                request,
                "Usuario registrado correctamente."
            )


            return redirect(
                "login"
            )



        except ValidationError as e:


            messages.error(
                request,
                e.message
            )


            return redirect(
                "login"
            )



        except Exception as e:


            print("ERROR REGISTRO:", e)


            messages.error(
                request,
                "Verifique que todos los datos sean correctos."
            )


            return redirect(
                "login"
            )


    request.session["registro_exitoso"] = True
    return redirect(
        "login"
    )
# ==========================================================
# PANEL USUARIO
# ==========================================================


def panel_usuario(request):


    if "usuario_id" not in request.session:

        return redirect(
            "login"
        )


    usuario = get_object_or_404(
        Usuario,
        id=request.session["usuario_id"]
    )


    citas = Cita.objects.filter(
        usuario=usuario
    ).order_by(
        "-id"
    )



    # MODALES

    mostrar_modal = request.session.pop(
        "perfil_actualizado",
        False
    )


    mostrar_modal_cita = request.session.pop(
        "cita_agendada",
        False
    )


    mostrar_modal_eliminar = request.session.pop(
        "cita_eliminada",
        False
    )


    mostrar_modal_error = request.session.pop(
        "error_eliminar_cita",
        False
    )



    return render(
        request,
        "panel_usuario.html",
        {

            "usuario": usuario,

            "citas": citas,


            "mostrar_modal":
                mostrar_modal,


            "mostrar_modal_cita":
                mostrar_modal_cita,


            "mostrar_modal_eliminar":
                mostrar_modal_eliminar,


            "mostrar_modal_error":
                mostrar_modal_error

        }
    )






# ==========================================================
# PANEL ADMINISTRADOR
# ==========================================================


def panel_admin(request):


    if "admin_id" not in request.session:

        return redirect(
            "login"
        )



    admin = get_object_or_404(
        Administrador,
        id=request.session["admin_id"]
    )



    # ======================================================
    # BUSCADOR DE USUARIOS
    # ======================================================


    buscar = request.GET.get(
        "buscar",
        ""
    ).strip()



    usuarios = Usuario.objects.all()



    if buscar:


        usuarios = usuarios.filter(

            Q(nombre_completo__icontains=buscar)

            |

            Q(correo__icontains=buscar)

            |

            Q(modelo_dron__icontains=buscar)

        )





    # ======================================================
    # FILTROS DE CITAS
    # ======================================================


    citas = Cita.objects.all().order_by(
        "-id"
    )



    estatus = request.GET.get(
        "estatus",
        ""
    )


    servicio = request.GET.get(
        "servicio",
        ""
    )



    if estatus:


        citas = citas.filter(
            estatus=estatus
        )



    if servicio:


        citas = citas.filter(
            tipo_servicio=servicio
        )





    citas_pendientes = Cita.objects.filter(
        estatus="Pendiente"
    ).count()





    # ======================================================
    # MODALES
    # ======================================================


    mostrar_modal_admin = request.session.pop(
        "admin_actualizado",
        False
    )


    mostrar_modal_eliminar = request.session.pop(
        "usuario_eliminado",
        False
    )




    return render(

        request,

        "panel_admin.html",

        {


            "admin": admin,


            "usuarios": usuarios,


            "buscar": buscar,


            "citas": citas,


            "estatus": estatus,


            "servicio": servicio,


            "citas_pendientes":
                citas_pendientes,


            "mostrar_modal_admin":
                mostrar_modal_admin,


            "mostrar_modal_eliminar":
                mostrar_modal_eliminar

        }

    )


# ==========================================================
# EDITAR PERFIL USUARIO
# ==========================================================
def editar_perfil(request):

    if "usuario_id" not in request.session:
        return redirect("login")


    usuario = Usuario.objects.get(
        id=request.session["usuario_id"]
    )


    if request.method == "POST":

        try:

            hoy = date.today()

            fecha_dron = request.POST.get("fecha_act_dron")

            fecha_generador = request.POST.get("fecha_act_generador")

            fecha_control = request.POST.get("fecha_act_control")


            if fecha_dron:

                fecha_dron = datetime.strptime(
                    fecha_dron,
                    "%Y-%m-%d"
                ).date()

            else:

                fecha_dron = usuario.fecha_act_dron



            if fecha_generador:

                fecha_generador = datetime.strptime(
                    fecha_generador,
                    "%Y-%m-%d"
                ).date()

            else:

                fecha_generador = usuario.fecha_act_generador

            if fecha_control:

                fecha_control = datetime.strptime(
                    fecha_control,
                    "%Y-%m-%d"
                ).date()

            else:

                fecha_control = usuario.fecha_act_control

            if fecha_dron > hoy:

                raise ValidationError(
                    "La fecha del dron no puede ser futura."
                )

            if fecha_generador > hoy:

                raise ValidationError(
                    "La fecha del generador no puede ser futura."
                )


            if fecha_control > hoy:

                raise ValidationError(
                    "La fecha del control no puede ser futura."
                )


            usuario.nombre_completo = request.POST.get(
                "nombre_completo"
            )

            usuario.correo = request.POST.get(
                "correo"
            )

            usuario.telefono = request.POST.get(
                "telefono"
            )

            usuario.domicilio = request.POST.get(
                "domicilio"
            )


            usuario.modelo_dron = request.POST.get(
                "modelo_dron"
            )

            usuario.num_serie_dron = request.POST.get(
                "num_serie_dron"
            )

            usuario.fecha_act_dron = fecha_dron



            usuario.modelo_generador = request.POST.get(
                "modelo_generador"
            )

            usuario.num_serie_generador = request.POST.get(
                "num_serie_generador"
            )

            usuario.fecha_act_generador = fecha_generador



            usuario.num_serie_control = request.POST.get(
                "num_serie_control"
            )

            usuario.fecha_act_control = fecha_control



            # ==========================
            # FOTO
            # ==========================

            if request.FILES.get("foto"):

                usuario.foto = request.FILES["foto"]



            # ==========================
            # CONTRASEÑA
            # ==========================

            nueva = request.POST.get(
                "contrasena"
            )


            if nueva:

                usuario.contrasena = make_password(
                    nueva
                )



            usuario.save()


            request.session["perfil_actualizado"] = True


            return redirect(
                "panel_usuario"
            )


        except ValidationError as e:


            messages.error(
                request,
                str(e)
            )


            return redirect(
                "panel_usuario"
            )



        except Exception as e:


            print("ERROR:", e)


            messages.error(
                request,
                "Error al actualizar perfil."
            )


            return redirect(
                "panel_usuario"
            )


    return redirect(
        "panel_usuario"
    )
# ==========================================================
# ELIMINAR USUARIO (ADMIN)
# ==========================================================


def eliminar_usuario(request, id):


    if "admin_id" not in request.session:

        return redirect(
            "login"
        )



    usuario = get_object_or_404(
        Usuario,
        id=id
    )



    usuario.delete()



    request.session[
        "usuario_eliminado"
    ] = True



    return redirect(
        "panel_admin"
    )

# ==========================================================
# CERRAR SESIÓN
# ==========================================================


def logout(request):


    request.session.flush()


    return redirect(
        "login"
    )

# ==========================================================
# AGENDAR CITA
# ==========================================================


def agendar_cita(request):


    if "usuario_id" not in request.session:

        return redirect(
            "login"
        )



    if request.method == "POST":



        usuario = get_object_or_404(

            Usuario,

            id=request.session["usuario_id"]

        )



        cita = Cita.objects.create(


            usuario=usuario,


            nombre_completo=
            usuario.nombre_completo,


            modelo_dron=
            usuario.modelo_dron,


            equipo=request.POST.get(
                "equipo"
            ),


            tipo_servicio=request.POST.get(
                "tipo_servicio"
            ),


            fecha_cita=request.POST.get(
                "fecha_cita"
            ),


            hora_cita=request.POST.get(
                "hora_cita"
            ),


            descripcion=request.POST.get(
                "descripcion"
            ),


            estatus="Pendiente"

        )




        # Buscar administrador

        admin = Administrador.objects.first()



        if admin:


            asunto = (
                "📅 Nueva cita registrada "
                "OCRDrone Service"
            )



            mensaje = f"""

OCRDrone Service

Nueva cita de mantenimiento registrada.


DATOS DEL CLIENTE
-------------------------

Nombre:
{usuario.nombre_completo}


Correo:
{usuario.correo}


Teléfono:
{usuario.telefono}



DATOS DEL EQUIPO
-------------------------

Equipo:
{cita.equipo}


Modelo del dron:
{cita.modelo_dron}



SERVICIO SOLICITADO
-------------------------

Servicio:
{cita.tipo_servicio}


Fecha:
{cita.fecha_cita}


Hora:
{cita.hora_cita}



DESCRIPCIÓN:

{cita.descripcion}


Ingrese al panel administrativo
para revisar la solicitud.

"""



            try:


                send_mail(


                    subject=asunto,


                    message=mensaje,


                    from_email=
                    settings.DEFAULT_FROM_EMAIL,


                    recipient_list=[
                        admin.correo_admin
                    ],


                    fail_silently=False

                )


            except Exception as error:


                print(
                    "Error enviando correo:",
                    error
                )





        request.session[
            "cita_agendada"
        ] = True



    return redirect(
        "panel_usuario"
    )







# ==========================================================
# ELIMINAR CITA USUARIO
# ==========================================================
def eliminar_cita(request, id):


    if "usuario_id" not in request.session:

        return redirect(
            "login"
        )



    cita = get_object_or_404(

        Cita,

        id=id,

        usuario_id=
        request.session["usuario_id"]

    )



    # Solo pendientes

    if cita.estatus != "Pendiente":


        request.session[
            "error_eliminar_cita"
        ] = True


        return redirect(
            "panel_usuario"
        )




    cita.delete()



    request.session[
        "cita_eliminada"
    ] = True



    return redirect(
        "panel_usuario"
    )







# ==========================================================
# CAMBIAR ESTATUS DE CITA
# ==========================================================


def cambiar_estatus(request, id):


    if "admin_id" not in request.session:

        return redirect(
            "login"
        )



    cita = get_object_or_404(
        Cita,
        id=id
    )



    if cita.estatus == "Pendiente":


        cita.estatus = "En proceso"



    elif cita.estatus == "En proceso":


        cita.estatus = "Completado"



    cita.save()



    return redirect(
        "/panel_admin/#citas"
    )








# ==========================================================
# EDITAR ADMINISTRADOR
# ==========================================================
def editar_admin(request):

    if "admin_id" not in request.session:
        return redirect("login")


    admin = Administrador.objects.get(
        id=request.session["admin_id"]
    )


    if request.method == "POST":


        admin.nombre_admin = request.POST.get(
            "nombre_admin"
        )


        admin.correo_admin = request.POST.get(
            "correo_admin"
        )


        admin.telefono_admin = request.POST.get(
            "telefono_admin"
        )



        nueva = request.POST.get(
            "contrasena_admin"
        )


        if nueva:

            admin.contrasena_admin = make_password(
                nueva
            )



        # FOTO

        if request.FILES.get(
            "foto_admin"
        ):


            foto = request.FILES[
                "foto_admin"
            ]


            ruta = os.path.join(
                settings.BASE_DIR,
                "static",
                "admin"
            )


            os.makedirs(
                ruta,
                exist_ok=True
            )


            fs = FileSystemStorage(
                location=ruta
            )


            if admin.foto_admin:


                foto_anterior = os.path.join(
                    ruta,
                    os.path.basename(
                        admin.foto_admin
                    )
                )


                if os.path.exists(
                    foto_anterior
                ):

                    os.remove(
                        foto_anterior
                    )



            nombre = fs.save(
                foto.name,
                foto
            )


            admin.foto_admin = (
                "admin/" + nombre
            )



        admin.save()


        request.session[
            "admin_actualizado"
        ] = True



    return redirect(
        "panel_admin"
    )
# ==========================================================
# REPORTE PDF DE CITAS
# ==========================================================


def reporte_citas(request):


    if "admin_id" not in request.session:

        return redirect(
            "login"
        )



    estatus = request.GET.get(
        "estatus",
        ""
    )


    servicio = request.GET.get(
        "servicio",
        ""
    )



    citas = Cita.objects.select_related(
        "usuario"
    ).all()



    if estatus:


        citas = citas.filter(
            estatus=estatus
        )



    if servicio:


        citas = citas.filter(
            tipo_servicio=servicio
        )




    buffer = BytesIO()



    documento = SimpleDocTemplate(

        buffer,

        pagesize=letter

    )



    estilos = getSampleStyleSheet()



    elementos = []



    titulo = Paragraph(

        "<b>Reporte de Citas OCRDrone Service</b>",

        estilos["Title"]

    )


    elementos.append(
        titulo
    )



    fecha = Paragraph(

        f"Fecha de generación: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}",

        estilos["Normal"]

    )


    elementos.append(
        fecha
    )



    elementos.append(
        Paragraph(
            "<br/>",
            estilos["Normal"]
        )
    )




    datos = [

        [

            "Cliente",

            "Correo",

            "Dron",

            "Servicio",

            "Fecha",

            "Hora",

            "Estado"

        ]

    ]




    for cita in citas:


        datos.append(

            [

                cita.usuario.nombre_completo,

                cita.usuario.correo,

                cita.modelo_dron,

                cita.tipo_servicio,

                str(cita.fecha_cita),

                str(cita.hora_cita),

                cita.estatus

            ]

        )





    tabla = Table(
        datos
    )



    tabla.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.darkgreen
                ),


                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,0),
                    colors.white
                ),


                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    1,
                    colors.black
                ),


                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER"
                ),


            ]

        )

    )



    elementos.append(
        tabla
    )



    documento.build(
        elementos
    )



    pdf = buffer.getvalue()



    buffer.close()




    response = HttpResponse(

        pdf,

        content_type="application/pdf"

    )



    response["Content-Disposition"] = (

        'attachment; filename="Reporte_Citas.pdf"'

    )



    return response







# ==========================================================
# RECUPERAR PASSWORD
# ==========================================================


def recuperar_password(request):


    if request.method == "POST":


        correo = request.POST.get(
            "correo"
        )



        try:


            usuario = Usuario.objects.get(

                correo=correo

            )



            recuperar = RecuperarPassword.objects.create(

                usuario=usuario

            )




            enlace = request.build_absolute_uri(

                reverse(

                    "nueva_password",

                    args=[recuperar.token]

                )

            )




            mensaje = f"""

OCRDrone Service


Hola {usuario.nombre_completo}


Recibimos una solicitud para cambiar
tu contraseña.


Ingresa al siguiente enlace:


{enlace}



Si tú no realizaste esta solicitud,
puedes ignorar este mensaje.


Saludos.

OCRDrone Service

"""





            send_mail(


                subject=
                "Recuperación de contraseña OCRDrone Service",


                message=mensaje,


                from_email=
                settings.DEFAULT_FROM_EMAIL,


                recipient_list=[
                    correo
                ],


                fail_silently=False

            )



            messages.success(

                request,

                "Se envió un enlace de recuperación a tu correo"

            )




        except Usuario.DoesNotExist:



            messages.error(

                request,

                "El correo no está registrado"

            )




    return redirect(
        "login"
    )








# ==========================================================
# NUEVA CONTRASEÑA
# ==========================================================


def nueva_password(request, token):


    recuperar = get_object_or_404(

        RecuperarPassword,

        token=token

    )




    if request.method == "POST":


        password = request.POST.get(
            "password"
        )


        confirmar = request.POST.get(
            "confirmar_password"
        )



        if password != confirmar:


            messages.error(

                request,

                "Las contraseñas no coinciden"

            )


            return redirect(
                request.path
            )





        if len(password) < 8:


            messages.error(

                request,

                "La contraseña debe tener mínimo 8 caracteres"

            )


            return redirect(
                request.path
            )





        usuario = recuperar.usuario



        usuario.contrasena = make_password(
            password
        )



        usuario.save()



        recuperar.delete()



        messages.success(

            request,

            "Contraseña actualizada correctamente"

        )



        return redirect(
            "login"
        )





    return render(

        request,

        "nueva_password.html"

    )