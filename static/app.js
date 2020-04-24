document.addEventListener('DOMContentLoaded', function () {

    /* Project level Materialize inits (prefer using vanilla js)
    * Because 'app.js' is placed at top of 'base.html' scripts,
    * subsequent inits will take priority?
    * */

    // const selectElems = document.querySelectorAll('select');
    // const selectInstances = M.FormSelect.init(selectElems, {});
    //
    //
    // // table of contents for recipe directions
    // const scrollSpyElems = document.querySelectorAll('.scrollspy');
    // const scrollSpyInstances = M.ScrollSpy.init(scrollSpyElems, {});

    // blanket auto init on all Materialize inits
    // to ignore a certain element, you can add the class .no-autoinit to that element
    M.AutoInit();
})