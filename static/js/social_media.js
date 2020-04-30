$(document).ready(function () {

    /* Facebook sharing */
    $('.fb-share-link').click(function (e) {
        var shareurl = window.location;
        window.open('https://www.facebook' +
            '.com/sharer/sharer.php?u=' + encodeURIComponent(shareurl) + '&t=' + document.title, '',
            'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=600');
        return false;
    });


})