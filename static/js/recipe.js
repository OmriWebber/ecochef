$(document).ready(function() {
    // Add button click event
    $('#addServingsButton').click(function() {
        console.log("test");
        var servings = $('#servingsCount').text();
        var oldServings = servings;
        servings++;
        $('#servingsCount').text(servings);
        changeIngredientAmount(oldServings, servings)
    });
  
    // Subtract button click event
    $('#minusServingsButton').click(function() {
        console.log("test");
        var servings = $('#servingsCount').text();
        var oldServings = servings;
        if (servings > 1) {
            servings--;
        } else {
            servings = 1;
        }
        $('#servingsCount').text(servings);
        changeIngredientAmount(oldServings, servings)
    });

    var description = $('.recipeDescription').text();
    description = htmlEntityChecker(description)
    $('.recipeDescription').html(description);

    var maxRating = 5; // Maximum rating value
    var currentRating = 0; // Current rating value

    // Generate star icons
    for (var i = 1; i <= maxRating; i++) {
        var star = $('<i class="star fa fa-star"></i>');
        star.attr('data-rating', i);
        $('#starRating').append(star);
    }

    // Handle star click event
    $('.star').click(function() {
        var rating = $(this).data('rating');
        updateRating(rating);
    });

    // Update the rating value and selected stars
    function updateRating(rating) {
        currentRating = rating;
        $('.star').removeClass('selected');
        $('.star').each(function() {
        if ($(this).data('rating') <= rating) {
            $(this).addClass('selected');
        }
        });
        $('#ratingValue').text(rating);
    }

});

function changeIngredientAmount(oldServings, newServings) {
    var ingredients = document.getElementsByClassName('ingredient-amount');
    for (var i = 0; i < ingredients.length; i++) {
        var ingredient = ingredients[i];
        var amount = ingredient.textContent;
        var newAmount = amount * (newServings / oldServings);
        ingredient.textContent = parseFloat(newAmount.toFixed(2));
    }
}

function htmlEntityChecker(input) {
    var characterArray = ['&amp;', '&nbsp;', '&#39;'];
    $.each(characterArray, function(idx, ent) {
        if (input.indexOf(ent) != -1) {
            var re = new RegExp(ent, "g");
            input = input.replace(re, '<span>' + ent + '</span>');
        }
    });
    return input;
}


