// ==================== CAMBIO DE SECCIONES ====================
function mostrar(id) {
    document.querySelectorAll(".seccion").forEach(sec => {
        sec.classList.remove("activa");
    });

    const seccion = document.getElementById(id);

    if (seccion) {
        seccion.classList.add("activa");
        localStorage.setItem("seccionAdmin", id);
    }
}

// ==================== MENÚ ====================
function toggleMenu(){

    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");


    sidebar.classList.toggle("collapsed");

    main.classList.toggle("expand");

}

// ==================== AL CARGAR LA PÁGINA ====================
document.addEventListener("DOMContentLoaded", () => {

    // Restaurar última sección
    const ultima = localStorage.getItem("seccionAdmin");

    if (ultima) {
        mostrar(ultima);
    } else if (document.getElementById("inicio")) {
        mostrar("inicio");
    }

    // ==================== MODAL INFORMACIÓN USUARIO ====================
    const modalUsuario = document.getElementById("verUsuarioModal");

    if (modalUsuario) {
        modalUsuario.addEventListener("show.bs.modal", function (event) {

            const boton = event.relatedTarget;

            document.getElementById("modalFoto").src = boton.dataset.foto;
            document.getElementById("mNombre").textContent = boton.dataset.nombre;
            document.getElementById("mCorreo").textContent = boton.dataset.correo;
            document.getElementById("mTelefono").textContent = boton.dataset.telefono;
            document.getElementById("mDomicilio").textContent = boton.dataset.domicilio;
            document.getElementById("mModelo").textContent = boton.dataset.modelo;
            document.getElementById("mSerie").textContent = boton.dataset.serie;
            document.getElementById("mFecha").textContent = boton.dataset.fecha;
            document.getElementById("mGenerador").textContent = boton.dataset.generador;
            document.getElementById("mSerieG").textContent = boton.dataset.serieg;
            document.getElementById("mFechaG").textContent = boton.dataset.fechag;
            document.getElementById("mSerieC").textContent = boton.dataset.seriec;
            document.getElementById("mFechaC").textContent = boton.dataset.fechac;
        });
    }

    // ==================== MODAL ELIMINAR ====================
    const modalEliminar = document.getElementById("confirmarEliminarModal");

    if (modalEliminar) {
        modalEliminar.addEventListener("show.bs.modal", function (event) {

            const boton = event.relatedTarget;

            document.getElementById("btnEliminarUsuario").href =
                "/eliminar/" + boton.dataset.id + "/";

            document.getElementById("nombreUsuarioEliminar").textContent =
                boton.dataset.nombre;
        });
    }

    // ==================== PREVISUALIZAR FOTO ====================
    const inputFotoAdmin = document.getElementById("fotoAdminInput");
    const previewAdmin = document.getElementById("previewAdmin");

    if (inputFotoAdmin && previewAdmin) {

        inputFotoAdmin.addEventListener("change", function () {

            const archivo = this.files[0];

            if (!archivo) return;

            const lector = new FileReader();

            lector.onload = function (e) {
                previewAdmin.src = e.target.result;
            };

            lector.readAsDataURL(archivo);
        });
    }

});

// ==================== MOSTRAR CONTRASEÑA ====================
function mostrarPasswordAdmin() {

    const campo = document.getElementById("contrasenaAdmin");
    const icono = document.getElementById("iconoAdmin");

    if (!campo || !icono) return;

    if (campo.type === "password") {

        campo.type = "text";

        icono.classList.remove("bi-eye");
        icono.classList.add("bi-eye-slash");

    } else {

        campo.type = "password";

        icono.classList.remove("bi-eye-slash");
        icono.classList.add("bi-eye");
    }
}