function searchFunction() {
    // Declare variables
    var input, filter, i, recipeTitleValue, recipeCategoryValue, recipeTitle, recipeGrid, recipeGridCards, recipeCategory;
    input = document.getElementById("searchRecipes");
    filter = input.value.toUpperCase();
    recipeGrid = document.getElementById("recipeGrid");
    recipeGridCards = recipeGrid.getElementsByClassName('col-md-4');

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < recipeGridCards.length; i++) {
      recipeTitle = recipeGridCards[i].getElementsByClassName("recipeTitle")[0];
      recipeCategory = recipeGridCards[i].getElementsByClassName("recipeCategory")[0];
      console.log(recipeTitle,recipeCategory);
      if (recipeTitle || recipeCategory) {
        recipeTitleValue = recipeTitle.textContent || recipeTitle.innerText;
        recipeCategoryValue = recipeCategory.textContent || recipeCategory.innerText;
        if (recipeTitleValue.toUpperCase().indexOf(filter) > -1 || recipeCategoryValue.toUpperCase().indexOf(filter) > -1) {
          recipeGridCards[i].style.display = "";
        } else {
          recipeGridCards[i].style.display = "none";
        }
      }
    }
  }

$(document).on("click", ".delete-recipe-button", function () {
    var recipeTitle = $(this).data('title');
    var recipeID = $(this).data('id');
    document.getElementById("recipeTitle").innerHTML = recipeTitle;
    document.getElementById("confirm-delete-button").setAttribute("href", "/deleteRecipe/" + recipeID);
});

// Global Sorting of Tables
const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;
const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));
document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    const table = th.closest('table');
    Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table.appendChild(tr) );
})));

$( document ).ready(function() {
    user_name = $('.user-name').text().slice(1,2);
    $('.user-letter').text(user_name.toUpperCase());
});

setTimeout(function() {
  $('#alert').hide();
}, 5000); // <-- time in milliseconds

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
	});
});

$(".heart").click(function(){
  var id = $(this).attr('data-id');
  var action = $(this).attr('data-action');
  var token = $(this).attr('data-token');
  var icon = $(this).children();
  var parent = $(this);

  if(action == 'unsave') {
    var settings = {
      "url": "http://ecochef-api-env.ap-southeast-2.elasticbeanstalk.com/unsaverecipe/" + id,
      "method": "POST",
      "timeout": 0,
      "headers": {
        "x-access-token": token,
        "Content-Type": "application/json"
      },
      "data": JSON.stringify({
        "user_id": 1,
        "recipe_id": id
      }),
    };
    
    $.ajax(settings).done(function (response) {
      icon.removeClass('fa').addClass('far');
      parent.attr('data-action', 'save');
      $('#alertId').removeClass('hide').removeClass('alert-success').addClass('alert-danger');
      $('#alertId').children('center').children('span').text("Recipe Removed!");

      setTimeout(function() {
        $("#alertId").addClass('hide');
      }, 3000);
    });
  } else if (action == 'save') {
    var settings = {
      "url": "http://ecochef-api-env.ap-southeast-2.elasticbeanstalk.com/saverecipe/" + id,
      "method": "POST",
      "timeout": 0,
      "headers": {
        "x-access-token": token,
        "Content-Type": "application/json"
      }
    };
    
    $.ajax(settings).done(function (response) {
      icon.removeClass('far').addClass('fa');
      parent.attr('data-action', 'unsave');
      $('#alertId').removeClass('hide').removeClass('alert-danger').addClass('alert-success');
      $('#alertId').children('center').children('span').text("Recipe Saved!");

      setTimeout(function() {
        $("#alertId").addClass('hide');
      }, 3000);

    });
  }
  
});

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



