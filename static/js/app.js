/* General purpose app initializations and functions mostly in vanilla javascript ES6 */

document.addEventListener('DOMContentLoaded', function () {

    /* Project level Materialize inits (prefer using vanilla js)
    * Because 'app.js' is placed at top of 'base.html' scripts,
    * subsequent inits will take priority
    * */

    // blanket auto init on all Materialize inits
    // to ignore a certain element, you can add the class .no-autoinit to that element
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

    // const swipeableTabsElems = document.querySelectorAll('.swipeable.tabs')
    // const swipeableTabsInstances = M.Tabs.init(swipeableTabsElems, {
    //     swipeable: true,
    //     // responsiveThreshold: 600, // todo:this doesn't seem to have an effect?
    // });

    lazifyImages();


})


// add 'lazy' class to img tags and 'data-src' for lazy loading with 'yall.js'
// also add 'responsive-img' class (materialize CSS)
// todo: is there a better way of doing this? a bit hacky...
function lazifyImages() {
    var region = document.getElementsByClassName("main-content");

    if (region.length) {
        for (k = 0; k < region.length; k++) {
            var img = region[k].querySelectorAll("img:not(.lazy)");

            for (i = 0; i < img.length; i++) {
                img[i].classList.add("lazy", "responsive-img");
                var src = img[i].src;
                img[i].removeAttribute("src");
                img[i].setAttribute("data-src", src);
            }
        }

        yall({
            idleLoadTimeout: 500,
            threshold: 200,
            observeChanges: true,
            observeRootSelector: 'main-content',
        });
    }


}

// initialize Materialize collapsible components with toggle icon for open/closed state
function initializeToggleIconCollapsible(collapsibleSelector, iconSelector, openedIcon, closedIcon, options) {
    const $filterHeaderIcon = $(iconSelector);
    const collapsibleInstances = $(collapsibleSelector).collapsible({
        onOpenStart: function (el) {
            $(el).find($filterHeaderIcon).html(openedIcon)
            // $filterHeaderIcon.html(openedIcon)
        },
        onCloseStart: function (el) {
            $(el).find($filterHeaderIcon).html(closedIcon)
            // $filterHeaderIcon.html(closedIcon)
        },
        ...options
    });
}


