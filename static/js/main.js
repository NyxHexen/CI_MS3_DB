$(document).ready(function(){
    $('.sidenav').sidenav();
  });

$('.profile-languages .card-action a').click(function() {
  $('.user-languages').toggleClass('truncate');
  if (this.text == "See All") {
    this.text = "Hide"
  } else {
    this.text = "See All"
  }
});