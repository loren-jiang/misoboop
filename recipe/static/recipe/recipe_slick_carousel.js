$(document).ready(function () {
    /* Slick slider initialization with single-item */
    $('.fullwidth-slick-carousel').slick({
        arrows: false,
        dots: true,
    })

    /* Slick slider initialization with responsiveness */
    $('.responsive-slick-carousel').slick({
        // adaptiveHeight: true,
        centerMode: true,
        centerPadding: '60px',
        infinite: false,
        slidesToShow: 3,
        nextArrow: '<a class="carousel-next"><i class="material-icons carousel-arrow-icon">navigate_next</i></a>',
        prevArrow: '<a class="carousel-prev"><i class="material-icons carousel-arrow-icon">navigate_before</i></a>',
        responsive: [
            {

                breakpoint: 992,
                settings: {
                    // adaptiveHeight: true,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 600,
                settings: {
                    // adaptiveHeight: true,
                    arrows: false,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 1,
                }
            }
        ]
    });


});


/* functions */
function showMediaLinks() {
    console.log("todo: showMediaLinks");
}

