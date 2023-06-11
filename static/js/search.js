var swiper = new Swiper('.swiper-container', {
    direction: 'horizontal',
    autoHeight: true,
    slidesPerView: 1,
    centeredSlides: true,
    spaceBetween: 30,
});

document.querySelector('.slide-name').addEventListener('click', function (e) {
    e.preventDefault();
    $(this).addClass('active');
    $('.slide-ingredient').removeClass('active');
    swiper.slideTo(0, 300);
});

document.querySelector('.slide-ingredient').addEventListener('click', function (e) {
    e.preventDefault();
    $(this).addClass('active');
    $('.slide-name').removeClass('active');
    swiper.slideTo(1, 300);
});

$(".add-ingredient").click(function () {
        var newIngredient = "<div class='input-group mb-3'>" + 
                                "<a class='btn remove-ingredient'><i class='fa fa-times'></i></a>" +
                                "<input type='text' class='form-control' placeholder='Enter Ingredient' name='ingredient-name'>" +
                                "<a class='btn edit-ingredient'><i class='fa fa-pencil'></i></a>" +
                            "</div>";

        $('.remove-ingredient').click(function(){
            $(this).parent().remove();
        });

        $(".ingredient-cotainer").append(newIngredient);
    })

$(document).on("click", ".remove-ingredient", function () {
    $(this).parent().remove();
});

let timeoutID = null;

function findRecipe(str) {
    var settings = {
        "url": "http://127.0.0.1:4000/search",
        "method": "POST",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json"
        },
        "data": JSON.stringify({
            "query": str
        }),
    };
    
    $.ajax(settings).done(function (response) {
        var results = response.results;
        var div = $(".search-results");
        div.empty();
        for (var i = 0; i < results.length; i++) {
            console.log(results[i]);
            if (i % 2 == 0) {
                console.log("row open");
                div.append("<div class='row'>");
                div = $(".search-results .row:last-child")
            }

            
            console.log("result");
            div.append("<div class='col recipe'>"+
                                            "<a href='recipe/" + results[i].id + "'>" +
                                                "<img class='recipe-image' src='" + results[i].imageURL + "'>" +
                                                "<div class='favorite-overlay'>" +
                                                    "<a class='heart'>" +
                                                        "<i class='fa fa-heart'></i>" +
                                                    "</a>" +
                                                "</div>" +
                                                "<div class='overlay'>" +
                                                    "<p class='recipe-title'>" + results[i].title + "</p>" +
                                                "</div>" +
                                            "</a>" +
                                        "</div>")

            if (i % 2 == 1) {
                console.log("row close");
                div.append("</div>")
                div = $(".search-results")
            }
        }
    });
}

$('#searchInput').keyup(function(e) {
  clearTimeout(timeoutID);
  const value = e.target.value
  timeoutID = setTimeout(() => findRecipe(value), 500)
});