$(document).ready(function () {
    const btnHoursConfig = $("#btn-hours-config");
    const modalOpeningHours = $("#modalOpeningHours");
    const btnRestoreHours = $("#restoreHoursBtn");

    /* Abrir -> true | Fechar -> false */
    function toggleModalOpeningHours(open) {
        modalOpeningHours.toggleClass("hidden", !open);
    }

    function restoreHoursMenu() {
        console.log("Restaurar horários acionado");

        let URLDelete = `/api/menus/${menuId}/opening-hours`
        $.ajax({
            url: URLDelete,
            method: "DELETE",
            success: function(res) {
                console.log(`Res: ${res.data}`)
                toggleModalOpeningHours(false)
            },
            error: function(xhr) {
                // let resError = xhr.responseText;
                // alert(resError)
                toggleModalOpeningHours(false)
            }
        })
    }
    function addHoursMenu(event)  {
        event.preventDefault();

        const daysMap = {
            "segunda": "monday",
            "terca": "tuesday",
            "quarta": "wednesday",
            "quinta": "thursday",
            "sexta": "friday",
            "sabado": "saturday",
            "domingo": "sunday"
        };

        const openingHours = [];

        for (const [ptDay, enDay] of Object.entries(daysMap)) {
            const open = $(`#${ptDay}_open`).val();
            const close = $(`#${ptDay}_close`).val();

            if (open && close) {
                openingHours.push({
                    day: enDay,
                    open,
                    close
                });
            }
        }

        $.ajax({
            url: `/api/menus/${menuId}/opening-hours`,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(openingHours),
            success: function (res) {
                console.log(res);
                $("#openingHoursForm input[type='time']").val("");
            },
            error: function (err) {
                console.error(err.responseText);
            }
        });

        console.log(openingHours);
    }
    function getHoursMenu() {
        toggleModalOpeningHours(true)
        $.ajax({
            url: `/api/menus/${menuId}/opening-hours`,
            method: "GET",
            success: function(res) {
                let data = res.data;
                console.log("Res de Horas:", JSON.stringify(data, null, 2));
            },
            error: function(err) {
                console.error(err);
            }
        });
    }

    btnHoursConfig.on("click", getHoursMenu)
    $("#openingHoursForm").on("submit", addHoursMenu);
    btnRestoreHours.on("click", restoreHoursMenu);
});
