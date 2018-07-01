// Carousel animations
$(document).ready(function(){
  $('.multiple-items').slick({
    lazyLoad: 'ondemand',
    dots: true,
    infinite: true,
    speed: 500,
    fade: true,
    adaptiveHeight: false,
  });
});