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
            console.log("test");
            $(this).parent().remove();
        });

        $(".ingredient-cotainer").append(newIngredient);
    })

$(document).on("click", ".remove-ingredient", function () {
    console.log("test");
    $(this).parent().remove();
});

