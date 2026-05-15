$(document).ready(function() {
    const $suggestionAdmin = $(".suggestionAdmin");
    const $modalSuggestionAdmin = $(".modalSuggestionAdmin");
    const $closeModalSuggestionAdmin = $(".closeModalSuggestionAdmin");

    $suggestionAdmin.on("click", function() {
        $modalSuggestionAdmin.removeClass("hidden");
    });

    $closeModalSuggestionAdmin.on("click", function() {
        $modalSuggestionAdmin.addClass("hidden");
    });
});


$(document).ready(function () {
    const toName = "administrator";

    const $suggestionMenu = $(".suggestionMenu");
    const $modalSuggestionMenu = $(".modalSuggestionMenu");
    const $closeModalSuggestionMenu = $(".closeModalSuggestionMenu");

    // abrir modal
    $suggestionMenu.on("click", function () {
        $modalSuggestionMenu.removeClass("hidden");
    });

    $closeModalSuggestionMenu.on("click", function () {
        $modalSuggestionMenu.addClass("hidden");
    });

    $("#sendReviewBtn").on("click", function () {

        const ratingBtn = $(".rating-btn.bg-gray-900");
        const rating = ratingBtn.length ? parseInt(ratingBtn.data("value")) : null;

        const tags = [];
        $(".tag-btn.bg-gray-900").each(function () {
            tags.push($(this).data("tag"));
        });

        const comment = $("#comment").val();

        if (!rating) {
            alert("Selecione uma nota.");
            return;
        }

        const payload = {
            to: toName,
            by: byName,
            category: tags,
            description: comment,
            note: rating,
        };

        console.log("Payload enviado:", payload);

        $.ajax({
            url: "/api/reviews",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(payload),

            success: function (response) {
                console.log("Sucesso:", response);

                $modalSuggestionMenu.addClass("hidden");

                $(".rating-btn").removeClass("bg-gray-900 text-white border-gray-900");
                $(".tag-btn").removeClass("bg-gray-900 text-white border-gray-900");
                $("#comment").val("");
            },

            error: function (jqXHR, textStatus, errorThrown) {
                console.log("STATUS:", jqXHR.status);
                console.log("STATUS TEXT:", textStatus);
                console.log("ERROR THROWN:", errorThrown);

                console.log("RESPONSE TEXT:", jqXHR.responseText);

                try {
                    const response = JSON.parse(jqXHR.responseText);
                    console.log("BACKEND MESSAGE:", response.message);
                } catch (e) {
                    console.log("Resposta não é JSON válido");
                }
            }
        });
    });

});