$(document).ready(function () {

    const $modal = $("#suggestionMenuModal");
    const $ratingContainer = $("#menuRating");
    const $tags = $("#menuTags .tag-btn");
    const $comment = $("#menuComment");

    $(".suggestionMenu").on("click", function () {
        $modal.removeClass("hidden");
    });

    $(".closeModalSuggestionMenu").on("click", function () {
        $modal.addClass("hidden");
    });

    $ratingContainer.on("click", ".rating-btn", function () {

        const value = parseInt($(this).data("value"));

        $ratingContainer.find(".rating-btn").each(function () {

            const btnVal = parseInt($(this).data("value"));

            $(this)
                .toggleClass("text-yellow-400", btnVal <= value)
                .toggleClass("text-gray-300", btnVal > value);
        });

        $ratingContainer.data("selected", value);
    });

    $tags.on("click", function () {
        $(this).toggleClass("bg-gray-900 text-white border-gray-900");
    });

    $("#sendMenuReviewBtn").on("click", function () {

        const rating = parseInt($ratingContainer.data("selected")) || null;

        const tags = [];

        $tags.filter(".bg-gray-900").each(function () {
            tags.push($(this).data("tag"));
        });

        const comment = $comment.val().trim();

        console.log({ rating, tags, comment });

        const payload = {
            to: storeName,
            by: "Anonymous",
            category: tags,
            description: comment,
            note: rating,
        };

        $.ajax({
            url: "/api/reviews",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(payload),

            success: function (response) {

                console.log("Sucesso:", response);

                $modal.addClass("hidden");

                $ratingContainer.removeData("selected");

                $ratingContainer.find(".rating-btn")
                    .removeClass("text-yellow-400")
                    .addClass("text-gray-300");

                $tags.removeClass("bg-gray-900 text-white border-gray-900");

                $comment.val("");
            },

            error: function (jqXHR, textStatus, errorThrown) {

                console.log("STATUS:", jqXHR.status);
                console.log("STATUS TEXT:", textStatus);
                console.log("ERROR THROWN:", errorThrown);
                console.log("RESPONSE TEXT:", jqXHR.responseText);
            }
        });
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