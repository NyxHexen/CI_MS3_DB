$(document).ready(function () {
  $('.sidenav').sidenav();
});

$('.profile-languages .card-action a').click(function () {
  $('.user-languages').toggleClass('truncate');
  if ($(this).text() == "See All") {
    let text = $(this).text();
    $(this).text(text.replace("See All", "Hide"))
  } else {
    let text = $(this).text();
    $(this).text(text.replace("Hide", "See All"))
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