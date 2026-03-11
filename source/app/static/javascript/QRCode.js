$(document).ready(function () {

    const modalQRCode = $("#modalQRCodeModal")
    const btnQRCode = $("#btn-qrcode-open")
    
    btnQRCode.on("click", function () {
        const btnGenerateQRCode = $("#btn-generate-qrcode")
        const QRCodeSection = $("#QRCodeSection")
        modalQRCode.removeClass("hidden")
        
        btnGenerateQRCode.on("click", function () {
            QRCodeSection.empty()

            new QRCode(QRCodeSection[0], {
                text: `http://localhost/menus/${menuSlug}`,
                width: 300,
                height: 300
            })
        })
    })
})