
        document.getElementById("foto").addEventListener("change", function (e) {

            const archivo = e.target.files[0];

            if (archivo) {

                const lector = new FileReader();

                lector.onload = function (event) {

                    document.getElementById("previewFoto").src = event.target.result;

                };

                lector.readAsDataURL(archivo);

            }

        });

        document.addEventListener("DOMContentLoaded", function () {

            let hoy = new Date();

            let fecha = hoy.toISOString().split("T")[0];


            document.getElementById("fecha_act_dron").max = fecha;

            document.getElementById("fecha_act_generador").max = fecha;

            document.getElementById("fecha_act_control").max = fecha;

        });

    

   

        function mostrarPasswordRegistro() {

            let campo = document.getElementById(
                "contrasenaRegistro"
            );

            let icono = document.getElementById(
                "iconoRegistro"
            );


            if (campo.type === "password") {


                campo.type = "text";


                icono.classList.remove(
                    "bi-eye"
                );


                icono.classList.add(
                    "bi-eye-slash"
                );


            } else {


                campo.type = "password";


                icono.classList.remove(
                    "bi-eye-slash"
                );


                icono.classList.add(
                    "bi-eye"
                );

            }

        }


function mostrarPasswordLogin(){

    let campo = document.getElementById(
        "contrasenaLogin"
    );

    let icono = document.getElementById(
        "iconoLogin"
    );


    if(campo.type === "password"){


        campo.type = "text";


        icono.classList.remove(
            "bi-eye"
        );


        icono.classList.add(
            "bi-eye-slash"
        );


    }else{


        campo.type = "password";


        icono.classList.remove(
            "bi-eye-slash"
        );


        icono.classList.add(
            "bi-eye"
        );


    }

}

