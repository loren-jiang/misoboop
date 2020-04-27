document.addEventListener('DOMContentLoaded', function () {

    /* Project level Materialize inits (prefer using vanilla js)
    * Because 'app.js' is placed at top of 'base.html' scripts,
    * subsequent inits will take priority?
    * */

    // const selectElems = document.querySelectorAll('select');
    // const selectInstances = M.FormSelect.init(selectElems, {});
    //
    //


    // blanket auto init on all Materialize inits
    // to ignore a certain element, you can add the class .no-autoinit to that element
    M.AutoInit();

    // // table of contents for recipe directions
    const scrollSpyElems = document.querySelectorAll('.scrollspy');
    const scrollSpyInstances = M.ScrollSpy.init(scrollSpyElems, {
        scrollOffset: 0
    });

    lazifyImages();

    yall({
        idleLoadTimeout: 0,
        threshold: 0,
    });
})

function lazifyImages() {
    // add 'lazy' class to img tags and 'data-src' for lazy loading with 'yall.js'
    // todo: is there a better way of doing this? a bit hacky...
    var region = document.getElementsByClassName("main-content");
    if (region.length) {
        for (k = 0; k < region.length; k++) {
            var img = region[k].getElementsByTagName("img");
            for (i = 0; i < img.length; i++) {
                img[i].classList.add("lazy", "responsive-img");
                var src = img[i].src;
                img[i].removeAttribute("src");
                img[i].setAttribute("data-src", src);
            }
        }
    }
}

// https://materializecss.com/media-css.html
function responsifyImages(selector) {
    var images = $(selector).addClass('responsive-img')
}

// initalize Materialize collapsible components with toggle feature
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


