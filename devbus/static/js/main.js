$(document).ready(function () {
  // Materialize Inits
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.tooltipped').tooltip();
  $('.modal').modal();
  $('.carousel').carousel();

// If any flash messages are passed, this code turns it into a Materialize toast.
  if ($('.toast')) {
    $('.toast').each(function () {
      if ($(this).hasClass('message')) {
        M.toast({
          html: $(this).text(),
          classes: 'light-blue'
        });
      } else {
        M.toast({
          html: $(this).text(),
          classes: $('.toast').attr('class')
        });
      }
    });
  }

  // Redirect timer for error pages
  if ($('section.error').html() != undefined) {
    $(function () {
      let timerDuration = 30;
      let timer = setTimeout(function () {}, timerDuration * 1000);
      let countdown = setInterval(function () {
        timerDuration = timerDuration - 1;
        $('section.error .timer').text(timerDuration);
        if (timerDuration == 0) {
          clearInterval(countdown);
          clearTimeout(timer);
          location.href = '/';
        }
      }, 1000);
    });
  }

  // Adds a label to the Materialize generated Filter dropdown menu for compliance.
  if ($("input[name='search_field']").html() != undefined) {
    $("input.select-dropdown.dropdown-trigger").attr("id", "select-dropdown");
    $("input.select-dropdown.dropdown-trigger").prepend("<label for='select-dropdown'>Filter By</label>");
  }
});

// Controls the comments/assists text on smaller devices.
// If window is max-width 690, then comment(s) and assist(s) text is omitted.
// $(window).innerWidth() returns 17px less as a value
if ($(window).innerWidth() + 17 <= 690) {
  $('.post .card-action span').each(function () {
    let text = $(this).text();
    text = text.replace(/comments|comment/g, "");
    text = text.replace(/assists|assist/g, "");
    $(this).text(text);
  });
}

// Hover effect for quickmenu side nav
$('.collection-item').hover(function () {
  $(this).removeClass('deep-purple-text text-darken-3');
  $(this).addClass('deep-purple darken-3 active');
}, function () {
  $(this).removeClass('deep-purple darken-3 active');
  $(this).addClass('deep-purple-text text-darken-3');
});


// Controls if code fields are shown in new/edit post/comment/subcomment.
$('.switch label').on('mouseup', function () {
  if ($('#code_switch').is(':checked')) {
    $('.code-switch').each(function () {
      $(this).addClass('visually-hidden');
    });
  } else if (!$('#code_switch').is(':checked')) {
    $('.code-switch').each(function () {
      $(this).removeClass('visually-hidden');
    });
  }
});

// Vote Buttons AJAX call, used to capture click and feed to the back-end.
// Back-end response (count of votes) is then immediately updated to screen.
$(function () {
  $('.vote-button').each(function () {
    $(this).on('click', function (e) {
      e.preventDefault();
      let thisElem = $(this);
      let thisCounter = $(this).children('span');
      let siblingCounter = thisElem.siblings('.vote-button').children('span');
      let thisCounterCurrentNum = parseInt(thisCounter.text());
      let siblingCounterCurrentNum = parseInt(siblingCounter.text());
      $.ajax({
        url: $(this).attr('href'),
        type: 'POST',
        success: function (response) {
          // If user is not logged in (server returns false), redirect to login page and trigger a toast
          if (!response) {
            return window.location.replace(window.location.protocol + "//" + window.location.host + "/signin");
          } else {
            // Deconstruct; if button pressed is upvote assign response.length_up as thisCounterNewNum
            // and response_length_up as siblingCounterNewNum. If button pressed is down vote - reverse logic.
            let [thisCounterNewNum,
              siblingCounterNewNum
            ] = thisElem.attr('href').match('/up') ? [response.length_up, response.length_down] : [response.length_down, response.length_up];
            // Check current state of vote buttons
            if (thisCounterCurrentNum < thisCounterNewNum && siblingCounterCurrentNum == siblingCounterNewNum) {
              // If User hasn't voted before
              thisCounter.siblings('i').removeClass('text-lighten-2').addClass('accent-4');
              // In case the user has voted in a previous session, check if sibling
              // has appropriate styling
              if (siblingCounter.siblings('i').hasClass('accent-4')) {
                siblingCounter.siblings('i').removeClass('accent-4').addClass('text-lighten-2');
              }
            } else if (thisCounterCurrentNum > thisCounterNewNum && siblingCounterCurrentNum == siblingCounterNewNum) {
              // If User has voted before and is removing all votes
              thisCounter.siblings('i').removeClass('accent-4').addClass('text-lighten-2');
            } else if (thisCounterCurrentNum < thisCounterNewNum && siblingCounterCurrentNum > siblingCounterNewNum) {
              // If User has voted before and is changing their choice to alternative vote
              thisCounter.siblings('i').removeClass('text-lighten-2').addClass('accent-4');
              siblingCounter.siblings('i').removeClass('accent-4').addClass('text-lighten-2');
            }
            // Update variable values from response
            thisCounter.text(thisCounterNewNum);
            siblingCounter.text(siblingCounterNewNum);
          }
        },
        error: function (error) {
          M.toast({
            html: "Something went wrong, please refresh the page and try again!",
            classes: 'red'
          });
        }
      });
    });
  });
});

// Close animation for Search Bar
$('[data-target="search-field--container"]').on('mousedown', function () {
  $('#search').toggleClass('scale-out');
});

// Hover effect (visual) for Search Bar
$("#search .autocomplete")
  .on('focusin', function () {
    $("#search").children('.row').css("background-color", "rgba(255, 255, 255, 0.80)");
  }).on('focusout', function () {
    $("#search").children('.row').css("background-color", "rgba(255, 255, 255, 0.55)");
  });

// Search Bar AJAX call, used for the autocomplete (search) field.
// On server response creates a pop-up with any matching users.
$("#autocomplete-input")
  .on('keyup', function () {
    let filter = $('#filter_select').find(":selected").val();
    let arg = $('#autocomplete-input').val();
    let url = `/_search/${filter}/${arg}`;
    let newData = {};
    let username;
    $.ajax({
      url: url,
      type: 'POST',
      success: function (response) {
        if (response == false) {
          return;
        }
        for (let key in response.items) {
          if (filter == "user") {
            username = response.items[key].username;
            newData[username] = "";
          } else if (filter == "lang") {
            newData[response.items[key].code_language] = null;
          }
        }

        $('input.autocomplete').autocomplete({
          data: newData,
        });
        $('input.autocomplete').autocomplete('open');
      },
      error: function (error) {
        newData["Something went wrong..."] = "";
        $('input.autocomplete').autocomplete({
          data: newData,
        });
      }
    });
  });

// Helper function to dynamically change the href of the delete comment modal,
// instead of every comment/subcomment having their own modal generated at load.
$('a').each(function () {
  if ($(this).data().hasOwnProperty('uid')) {
    if ($(this).data().hasOwnProperty('suid')) {
      $(this).click(function () {
        $('#delete_comment a').first().attr("href", `/${$(this).data("uid")}/${$(this).data("suid")}/delete_subcomment`);
      });
    } else {
      $(this).click(function () {
        $('#delete_comment a').first().attr("href", `/${$(this).data("uid")}/delete_comment`);
      });
    }
  }
});