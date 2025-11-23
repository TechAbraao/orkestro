$(document).ready(async function () {
    let customerName = $("#modalCustomerName");
    let customerTelephone = $("#modalCustomerTelephone");
    let customerAddress = $("#modalCustomerAddress");
    let customerNumber = $("#modalCustomerNumber");

    const btnConfirmOrder = $(".confirm-order");
    btnConfirmOrder.on("click", async function() {
        let storage = window.localStorage

        let name = customerName.val();
        let address = customerAddress.val();
        let telephone = customerTelephone.val();
        let number = customerNumber.val();

        const exists = await fetch(`/api/customers?telephone=${telephone}`)
        const dataExists = await exists.json()
        if (dataExists.success == true) {
            const customer_id = dataExists.data.user_id
            const userDetails = await fetch(`/api/customers?id=${customer_id}`)
            const userDetailsData = await userDetails.json()
            let dataUser = userDetailsData.data

            storage.setItem("customerCredentials", JSON.stringify({
                "name": dataUser.name,
                "address": dataUser.address,
                "telephone": dataUser.telephone,
                "number": dataUser.house_number
            }))
            window.location.href = `/menus/${menuSlug}/payment`;
        }

        const url = `/api/customers`;
        $.ajax({
            method: "POST",
            contentType: "application/json",
            url: url,
            data: JSON.stringify({
                name: name,
                address: address,
                telephone: telephone,
                number: number
            }),
            success: function (res) {
                console.log("Mensagem de sucesso: ", res)
                storage.setItem("customerCredentials", JSON.stringify({
                    "name": name,
                    "address": address,
                    "telephone": telephone,
                    "number": number
                }))
                window.location.href = `/menus/${menuSlug}/payment`;
            },
            error: function (xhr, status, errorThrown) {
                console.group("ERRO NA REQUISIÇÃO AJAX");

                let errorResponse = null;
                try {
                    errorResponse = JSON.parse(xhr.responseText);
                } catch (e) {
                    errorResponse = {
                        message: "Erro inesperado. Resposta não é JSON.",
                        raw: xhr.responseText
                    };
                }

                console.error("Mensagem de erro do servidor:", errorResponse);
                console.error("Status:", status);
                console.error("Detalhes do jQuery:", errorThrown);

                let hasRedirect = errorResponse?.success ?? false;
                console.log("Sucesso no redirecionamento:", hasRedirect);
                if (hasRedirect == false) {
                    window.location.href = `/menus/${menuSlug}/payment`;
                }
                console.groupEnd();
            },
        })
    })
})