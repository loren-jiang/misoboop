// tocbot.init({
//     // Where to render the table of contents.
//     tocSelector: '.js-toc',
//     // Where to grab the headings to build the table of contents.
//     contentSelector: '.js-toc-content',
//     // Headings that match the ignoreSelector will be skipped.
//     ignoreSelector: '.js-toc-ignore',
//     // Which headings to grab inside of the contentSelector element.
//     headingSelector: 'h1, h2, h3',
//     // For headings inside relative or absolute positioned containers within content.
//     hasInnerContainers: true,
// });

$(document).ready(function () {
    $('.scrollspy').scrollSpy();
});
