/* search bar features
* todo: maybe later implement with autoComplete.js (https://tarekraafat.github.io/autoComplete.js) */

document.addEventListener('DOMContentLoaded', function () {
    // fetch('/api/recipes/?format=json')
    //     .then(res => res.json())
    //     .then((out) => {
    //         const ns1 = $('#ns1');
    //         ns1.prop('disabled', false);
    //         $('.nav-search').css( "visibility", 'visible' );
    //         let obj = {}
    //         let hrefs = {}
    //
    //         for (let i = 0; i < out.length; i++) {
    //             obj[out[i].name] = null;
    //             hrefs[out[i].name] = out[i].slugged_url
    //         }
    //
    //         const goToRecipeLink = (value) => {
    //             if (value in hrefs) {
    //                 window.location = hrefs[value];
    //             }
    //
    //         }
    //
    //         const instances = M.Autocomplete.init(ns1, {
    //             limit: 5,
    //             minLength: 1,
    //             sortFunction: false,
    //             data: obj,
    //             onAutocomplete: goToRecipeLink
    //         });
    //
    //         // const ns2 = $('#ns2');
    //         // const instance2 = M.Autocomplete.init(ns2, {
    //         //     sortFunction: false,
    //         //     data: obj,
    //         //     onAutocomplete: goToRecipeLink
    //         // });
    //     })
    //     .catch(err => {
    //         throw err
    //     });

    //Autocomplete with ajax xhr
    $.ajax({
        type: 'GET',
        url: '/api/recipes_list/',
        success: function (response) {
            const ns1 = $('#ns1');
            ns1.prop('disabled', false);
            $('.nav-search').css("visibility", 'visible');
            let obj = {}
            let hrefs = {}

            for (let i = 0; i < response.length; i++) {
                obj[response[i].name] = null;
                hrefs[response[i].name] = response[i].slugged_url
            }

            const goToRecipeLink = (value) => {
                if (value in hrefs) {
                    window.location = hrefs[value];
                }

            }

            ns1.autocomplete({
                limit: 5,
                minLength: 1,
                sortFunction: false,
                data: obj,
                onAutocomplete: goToRecipeLink
            });
        }
    });

    // redirect form search to /search/recipes/?
    $('#nav_recipe_search').on('submit', function(e) {
        // e.preventDefault();

    })
});
