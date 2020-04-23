document.addEventListener('DOMContentLoaded', function () {

    /* Materialize inits (prefer using vanilla js) */

    const modalElems = document.querySelectorAll('.modal');
    const modalInstances = M.Modal.init(modalElems, {});

    // table of contents for recipe directions
    var scrollSpyElems = document.querySelectorAll('.scrollspy');
    var scrollSpyInstances = M.ScrollSpy.init(scrollSpyElems, options);

    // blanket auto init
    // to ignore a certain element, you can add the class .no-autoinit
    // M.AutoInit();
})