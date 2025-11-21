$(document).ready(function () {
    console.log("Hello, World!")
    // Capturando valores dos Inputs (dados do Cliente). //
    let customerName = $("#modalCustomerName");
    let customerTelephone = $("#modalCustomerTelephone");
    let customerAddress = $("#modalCustomerAddress");
    let customerNumber = $("#modalCustomerNumber");

    // Botão para enviar os dados do cliente. //
    const btnConfirmOrder = $(".confirm-order");
    btnConfirmOrder.on("click", function() {
        // Pegando os dados atuais do Input. //
        let name = customerName.val();
        let address = customerAddress.val();
        let telephone = customerTelephone.val();
        let number = customerNumber.val();
        console.log(`Nome: ${name} - Endereço: ${address} - Telefone: ${telephone} - Número: ${number}`)

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
                // Verificando caso dê sucesso. //
                console.log("Mensagem de sucesso: ", res)
                let hasRedirect = res.data.success
                console.log(`Sucesso no redirecionamento: ${hasRedirect}.`)
                if (hasRedirect) {
                    window.location.href = `/menus/${menuSlug}/confirm`;
                }
            },
            error: function (xhr, status, errorThrown) {
                console.group("ERRO NA REQUISIÇÃO AJAX");

                // Tentando pegar o JSON enviado pelo backend. //
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

                // Caso o back-end envie flag de sucesso. //
                let hasRedirect = errorResponse?.success ?? false;
                console.log("Sucesso no redirecionamento:", hasRedirect);
                if (hasRedirect == false) {
                    window.location.href = `/menus/${menuSlug}/payment`;
                }
                console.groupEnd();
            },
            complete: function () {
                let storage = window.localStorage
                storage.setItem("customerCredentials", JSON.stringify({
                    "name": name,
                    "address": address,
                    "telephone": telephone,
                    "number": number
                }))
            }
        })
    })
})