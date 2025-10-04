let menuNameHTML = $("#menu-name")
let menuDescriptionHTML = $("#menu-description")
let btnContactMenu = $("#btn-contact-menu")

$(document).ready(function () {
      $.ajax({
        url: menuClient,
        method: "GET",
        success: function (res) {
            console.log("Response: ", res)

            let menuDescription = res.data.description;
            let menuName = res.data.name;
            let categories = res.data.categories;

            console.log("Name: ", menuName);
            console.log("Menu Description: ", menuDescription);

            menuNameHTML.text(menuName);
            menuDescriptionHTML.text(menuDescription);

            let categoriesContainer = $("#categoriesContainer");
            categoriesContainer.empty();

            categories.forEach(cat => {
                let categoryHTML = `
            <div class="bg-white cursor-pointer shadow-lg rounded-2xl p-6 w-[630px] h-[230px] rounded-3xl border-2 border-gray-300 flex items-center text-center transform transition duration-300 hover:scale-105 hover:shadow-xl">
                <div class="w-2/3 h-full flex items-center justify-center bg-gray-100 rounded-xl overflow-hidden border border-gray-200">
                    <img src="${cat.url_image}" alt="${cat.name}" class="w-full h-full object-cover">
                </div>
                <div class="w-full h-full">
                    <h3 class="text-2xl font-semibold text-gray-800 mb-2 pl-3 pt-3 text-left">${cat.name}</h3>
                    <p class="text-sm text-gray-500 line-clamp-2 pl-3 text-left">${cat.description}</p>
                </div>
            </div>
            `;
                categoriesContainer.append(categoryHTML);
            });
        },
          error: function (xhr) {
              console.error("Erro ao buscar menu:", xhr);
          }
      });
    $.ajax({
        url: aboutMeStore,
        method: "GET",
        success: function (response) {
            console.log("User Infos:", response);
            if (response) {

                let storeLogoURL = response.data.logo_url
                $("img[alt='Store Logo']").attr("src", storeLogoURL);
            }
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseText);
        }
    });

    btnContactMenu.click(() => {
        $("#modalContactMenuModal").removeClass("hidden");
    });

    $("#modalContactMenuModal button").click(() => {
        $("#modalContactMenuModal").addClass("hidden");
    });
})
