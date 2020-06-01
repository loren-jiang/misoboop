/* General purpose app initializations and functions mostly in vanilla javascript ES6 */

document.addEventListener('DOMContentLoaded', function () {
    // blanket auto init on all Materialize inits
    M.AutoInit();

    // // table of contents for recipe directions
    const scrollSpyElems = document.querySelectorAll('.scrollspy');
    const scrollSpyInstances = M.ScrollSpy.init(scrollSpyElems, {
        scrollOffset: 0
    });

    var fullWidthCarouselElems = document.querySelectorAll('.carousel');
    var fullWidthCarouselInstances = M.Carousel.init(fullWidthCarouselElems, {
        fullWidth: true,
        indicators: true
    });

    lazifyAndResponsifyImages();

    // adding lazy loading for images is tricky for HTML field content
    // const el = document.querySelectorAll('img');
    const observer = lozad(document.querySelectorAll('.main-content img')); // lazy loads elements with default selector as '.lozad'
    observer.observe();

    // masonry layout
    $('.grid').colcade({
        columns: '.grid-col',
        items: '.grid-item'
    });
})



