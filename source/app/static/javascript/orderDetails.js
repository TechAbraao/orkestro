$(document).ready(function () {
    const orderContainer = $("#order-items")
    customerName.text(customerCredentialsData.name);
    customerTelephone.text(customerCredentialsData.telephone);
    customerAddress.text(customerCredentialsData.address);
    customerNumber.text(customerCredentialsData.number);

    cartData.products.forEach((prod) => {
        const itemHTML = `
                <div class="flex items-center justify-between w-[98%]
                bg-gray-50 p-4 rounded-xl border" data-id="${prod.product_id}">
                    
                    <div class="flex items-center gap-4">
                        
                        <img src="${prod.productImg}" class="w-[80px] h-[70px] rounded-lg bg-gray-200">

                        <div class="w-[250px]">
                            <h2 class="text-sm font-semibold">${prod.productName}</h2>
                            <p class="text-left text-sm font-semibold text-lg text-green-600 mt-1">
                                R$ ${(prod.price).toFixed(2)}
                            </p>
                            <p class="text-left text-sm">Quantidade: ${prod.quantity}</p>
                        </div>
                    </div>  
                </div>
            `;
        orderContainer.append(itemHTML)
    })
});
