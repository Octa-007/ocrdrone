document.addEventListener("DOMContentLoaded", () => {

    // ==================== FECHA MÍNIMA PARA AGENDAR CITA ====================

    const fecha = document.getElementById("fecha_cita");

    if (fecha) {
        const hoy = new Date();
        hoy.setDate(hoy.getDate() + 1);

        fecha.min = hoy.toISOString().split("T")[0];
    }

    // ==================== PREVISUALIZAR FOTO ====================

    const inputFotoUsuario = document.getElementById("fotoUsuario");
    const previewUsuario = document.getElementById("previewUsuario");

    if (inputFotoUsuario && previewUsuario) {

        inputFotoUsuario.addEventListener("change", function () {

            const archivo = this.files[0];

            if (!archivo) return;

            const lector = new FileReader();

            lector.onload = function (e) {
                previewUsuario.src = e.target.result;
            };

            lector.readAsDataURL(archivo);
        });
    }

    // ==================== FECHAS MÁXIMAS ====================

    const hoy = new Date().toISOString().split("T")[0];

    const editarFechaDron = document.getElementById("editarFechaDron");
    const editarFechaGenerador = document.getElementById("editarFechaGenerador");
    const editarFechaControl = document.getElementById("editarFechaControl");

    if (editarFechaDron) {
        editarFechaDron.setAttribute("max", hoy);
    }

    if (editarFechaGenerador) {
        editarFechaGenerador.setAttribute("max", hoy);
    }

    if (editarFechaControl) {
        editarFechaControl.setAttribute("max", hoy);
    }

});

// ==================== MOSTRAR CONTRASEÑA ====================

function mostrarPassword() {

    const campo = document.getElementById("nuevaContrasena");
    const icono = document.getElementById("iconoPassword");

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

