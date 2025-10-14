$(document).ready(() => {
    console.log(`Category ID in Products Page: ${categoryId}`)

    const productsSection = $("#productsSection")

    $.ajax({
        url: `/api/categories/${categoryId}/products`,
        method: "GET",
        success: function (response) {
            const products = response.data
            console.log("Resposta:", response)

            productsSection.empty()

            if (!products || products.length === 0) {
                productsSection.append(`
                    <p class="text-gray-500 text-center">Nenhum produto encontrado para esta categoria.</p>
                `)
                return
            }

             products.forEach(product => {
                const productCard = `
                    <div class="relative bg-white cursor-pointer shadow-lg rounded-2xl p-6 w-[630px] 
                    h-[230px] border-2 border-gray-300 flex items-center text-center transform 
                    transition duration-300 hover:scale-105 hover:shadow-xl product-item">
                        <div class="w-2/3 h-full flex items-center justify-center bg-gray-100 rounded-xl overflow-hidden border border-gray-200">
                            <img src="${product.image_url || '/static/images/default.png'}" alt="${product.name}" class="w-full h-full object-cover">
                        </div>
                        <div class="w-full h-full">
                            <h3 class="text-2xl font-semibold text-gray-800 mb-2 pl-3 pt-3 text-left">${product.name}</h3>
                            <p class="text-sm text-gray-500 line-clamp-2 pl-3 text-left">${product.description || "Sem descrição"}</p>
                            <p class="text-gray-800 font-medium mt-2 pl-3 text-left">R$ ${product.price.toFixed(2)}</p>
                        </div>
                        
                        <a href="/menus/${menuSlug}/products/${product.id}" class="absolute inset-0 z-10"></a>
                    </div>
                `
                productsSection.append(productCard)
            })
        },
        error: function (xhr, status, error) {
            console.error("Erro ao carregar produtos da categoria")

            console.group("Detalhes do erro")
            console.log("Status HTTP:", xhr.status)
            console.log("Status text:", xhr.statusText)
            console.log("Response text:", xhr.responseText)
            console.log("Ready state:", xhr.readyState)
            console.log("Status da requisição:", status)
            console.log("Mensagem de erro do jQuery:", error)
            console.groupEnd()

            $("#productsSection").html(`
                <p class="text-red-500 text-center">Erro ao carregar produtos. Tente novamente mais tarde.</p>
            `)
        }
    })

})
