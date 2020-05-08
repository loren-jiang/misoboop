/* General purpose utility functions mostly in vanilla javascript ES6 */

// todo: might need something more robust if more complex parsing needed
// doesn't support multiple query params as list
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

function cleanQueryParams() {
    // get the string following the ?
    var query = window.location.search.substring(1)
    // is there anything there ?
    if (query.length) {
        // are the new history methods available ?
        if (window.history != undefined && window.history.pushState != undefined) {
            // if pushstate exists, add a new state to the history, this changes the url without reloading the page

            window.history.pushState({}, document.title, window.location.pathname);
        }
    }
}

// Copies text to browser's clipboard
function copyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    // Place in top-left corner of screen regardless of scroll position.
    textArea.style.position = 'fixed';
    textArea.style.top = 0;
    textArea.style.left = 0;

    // Ensure it has a small width and height. Setting to 1px / 1em
    // doesn't work as this gives a negative w/h on some browsers.
    textArea.style.width = '2em';
    textArea.style.height = '2em';

    // We don't need padding, reducing the size if it does flash render.
    textArea.style.padding = 0;

    // Clean up any borders.
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';

    // Avoid flash of white box if rendered for any reason.
    textArea.style.background = 'transparent';


    textArea.value = text;

    document.body.appendChild(textArea);

    textArea.select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
    } catch (err) {
    }

    document.body.removeChild(textArea);
    return msg;
}


// taken from https://davidwalsh.name/javascript-debounce-function
// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    }
}

// add 'lazy' class to img tags and 'data-src' for lazy loading with 'lozad.js'
// also add 'responsive-img' class (materialize CSS)
// todo: is there a better way of doing this? a bit hacky...
function lazifyAndResponsifyImages() {
    var region = document.getElementsByClassName("main-content");

    if (region.length) {
        for (k = 0; k < region.length; k++) {
            // var img = region[k].querySelectorAll("img:not(.lozad)");
            var img = region[k].querySelectorAll("img");

            for (i = 0; i < img.length; i++) {
                img[i].classList.add("responsive-img"); // Materialize CSS class
                // img[i].classList.add("lozad", "responsive-img");
                // var src = img[i].src;
                // img[i].removeAttribute("src");
                // img[i].setAttribute("data-src", src);
            }
        }
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

//
// module.exports = {
//     getUrlParameter: getUrlParameter,
// }