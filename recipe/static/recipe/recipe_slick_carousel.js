$(document).ready(function () {
    $('.recipe-carousel').slick({
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 3,
        slidesToScroll: 3,
        // nextArrow: '<button class="carousel-next"><i class="material-icons">navigate_next</i></button>',
        // prevArrow: '<button class="carousel-prev"><i class="material-icons">navigate_before</i></button>',
        responsive: [
            // {
            //   breakpoint: 1024,
            //   settings: {
            //     slidesToShow: 3,
            //     slidesToScroll: 3,
            //     infinite: true,
            //     dots: true
            //   }
            // },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
            // settings: "unslick" to unslick
        ]
    });


});


/* functions */
function showMediaLinks() {
    console.log("todo: showMediaLinks");
}

