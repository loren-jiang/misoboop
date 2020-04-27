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



// taken from https://davidwalsh.name/javascript-debounce-function
// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};


//
// module.exports = {
//     getUrlParameter: getUrlParameter,
// }