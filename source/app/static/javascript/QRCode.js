$(document).ready(function() {
    
    const modalQRCode = $("#modalQRCodeModal")
    const btnQRCode = $("#btn-qrcode-open")

    btnQRCode.on("click", function() {
        modalQRCode.removeClass("hidden")
        
        const QRCodeSection = $("#QRCodeSection")
        
        QRCodeSection.empty()
        
        new QRCode(QRCodeSection[0], {
            text: `http://localhost/menus/${menuSlug}`,
            width: 1000,
            height: 1000
        })
    })
})