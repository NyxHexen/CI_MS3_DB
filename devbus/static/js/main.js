$(document).ready(function () {
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.tooltipped').tooltip();

  if ($('.toast')) {
    $('.toast').each(function () {
      if ($(this).hasClass('message')) {
        M.toast({
          html: $(this).text(),
          classes: 'light-blue'
        })
      } else {
        M.toast({
          html: $(this).text(),
          classes: $('.toast').attr('class')
        })
      }
    })
  }
});

$('.profile-languages .card-action span').click(function () {
  $('.user-languages').toggleClass('truncate');
  if ($(this).text() == "See All") {
    let text = $(this).text();
    $(this).text(text.replace("Show All", "Hide"))
  } else {
    let text = $(this).text();
    $(this).text(text.replace("Hide", "Show All"))
  }
});

// $(window).innerWidth() returns 17px less as a value
if ($(window).innerWidth() + 17 <= 475) {
  $('.post .card-action span').each(function () {
    let text = $(this).text();
    text = text.replace("comments", "");
    $(this).text(text)
  });
}

$('.collection-item').hover(function () {
  $(this).removeClass('deep-purple-text text-darken-3')
  $(this).addClass('deep-purple darken-3 active')
}, function () {
  $(this).removeClass('deep-purple darken-3 active')
  $(this).addClass('deep-purple-text text-darken-3')
})

$('#new_post .switch label').on('mouseup', function () {
  if ($('#code_switch').is(':checked')) {
    $('.code-switch').each(function () {
      $(this).addClass('visually-hidden')
    })
    $('#new_post .switch').parent().addClass('offset-s6')
  } else if (!$('#code_switch').is(':checked')) {
    console.log("3")
    $('.code-switch').each(function () {
      $(this).removeClass('visually-hidden')
    })
    $('#new_post .switch').parent().removeClass('offset-s6')
  }
})