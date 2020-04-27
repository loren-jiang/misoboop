var debounce = require('lodash/debounce');

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


$(document).ready(function () {
    let chipsInstances;
    const $recipeFilterForm = $('#recipe_filter_form');

    // for now, just support passing 'name__icontains' as query param
    const nameContains = getUrlParameter('name__icontains')
    if (nameContains) {
        $('input[name=name__icontains]').val(nameContains);
        cleanQueryParams();
    }

    // only do logic if we're at the right page (aka $recipeFilterForm is in DOM)
    if ($recipeFilterForm.length) {
        $.ajax({
            type: 'GET',
            url: '/api/ingredients/',
            async: false,
            success: function (response) {
                let ingredients = {}
                for (let i = 0; i < response.length; i++) {
                    if (Object.prototype.toString.call(response[i].name) === "[object String]") {
                        ingredients[response[i].name] = null;
                    }
                }
                chipsInstances = M.Chips.init($('#ingredient_chips'),
                    {
                        limit: 5,
                        onChipAdd: function () {
                            recipeSearch($recipeFilterForm);

                            /* wanted to change placeholder dynamically but doesn't seem possible */
                            // const instance = M.Chips.getInstance($('#ingredient_chips'));
                            // instance.options.secondaryPlaceholder = (instance.chipsData.length >= instance.options.limit - 1)
                            //     ? `limit of ${instance.options.limit}` : '';
                        },
                        onChipDelete: function () {
                            recipeSearch($recipeFilterForm);
                        },
                        placeholder: '+ ingredient',
                        // secondaryPlaceholder:' + ingredient',
                        autocompleteOptions: {
                            data: ingredients,
                            limit: 5,
                            minLength: 3,

                        }
                    });
            }
        });



        const $filterHeaderIcon = $("#collapsible_filter .collapsible-header .material-icons");
        const collapsibleInstances = M.Collapsible.init($('#collapsible_filter'), {
            inDuration: 200,
            onOpenStart: function () {
                $filterHeaderIcon.html(`arrow_drop_up`)
            },
            onCloseStart: function () {
                $filterHeaderIcon.html(`filter_list`)
            }
        });

        // retrieve those corresponding instances (will be unique)
        const chipsInstance = chipsInstances[0]; // = M.Chips.getInstance($("#ingredient_chips"));
        const filterCollapseInstance = collapsibleInstances[0]; // = M.Collapsible.getInstance($('#collapsible_filter'))

        // retrieve initial list
        recipeSearch($recipeFilterForm)
        /* Event handlers */

        // submit recipe search ajax
        $recipeFilterForm.submit(function (e) {
            e.preventDefault();
            recipeSearch($(this));
            M.Collapsible.getInstance($('#collapsible_filter')).close();

        })

        // submit form on ordering change
        $('#ordering').on('change', function () {
            recipeSearch($recipeFilterForm);
        })

        // clear fields and submit recipe search
        $('#clear_fields').on('click', function (e) {
            e.preventDefault();
            resetForm($recipeFilterForm, chipsInstance);
            recipeSearch($recipeFilterForm)
            // M.Collapsible.getInstance($('#collapsible_filter')).close();
        })

        $('ul.pagination').on('click', '.pagination-link', function (e) {
            e.preventDefault();
            $('#recipe_filter_page').val($(this).data("value")); // set page value input to corresponding pagination
            recipeSearch($recipeFilterForm, true)
        })

        $recipeFilterForm.find('#recipe_name_input').keyup(debounce(function () {
            recipeSearch($recipeFilterForm);
        }, 200));

        $("#ordering, #tags_input").on('change', function () {
            recipeSearch($recipeFilterForm);
        })


        /* blur not working? */
        // $('#collapsible_filter').on('blur', function (e) {
        //     filterCollapseInstance.close();
        // })

        // $('#demo_paginate').pagination({
        //     dataSource: '/api/recipes/',
        //     locator: 'results',
        //     totalNumberLocator: function (response) {
        //         // you can return totalNumber by analyzing response content
        //         return response.count;
        //     },
        //     pageSize: 20,
        //     ajax: {
        //         beforeSend: function () {
        //             dataContainer.html('Loading data from flickr.com ...');
        //         }
        //     },
        //     callback: function (data, pagination) {
        //         // template method of yourself
        //         var html = template(data);
        //         dataContainer.html(html);
        //     }
        // })
    }

})

function clearIngredientsAndOrdering() {
    // delete old input values to prevent form propagation
    $('input[name=ingredients]').remove();
    $('input[name=ordering]').remove();

}

function appendToForm($form, chipsData, orderings) {
    const orderingsString = Array.isArray(orderings) ? orderings.join(',') : orderings;
    clearIngredientsAndOrdering();

    chipsData.map(el => el.tag).forEach(ingredient => {
        $("<input />").attr("type", "hidden")
            .attr("name", "ingredients")
            .attr("value", ingredient)
            .appendTo($form);
    });
    if (orderingsString) {
        $("<input />").attr("type", "hidden")
            .attr("name", "ordering")
            .attr("value", orderingsString)
            .appendTo($form);
    }
}

function recipeSearch($form, paginating = false) {
    const chipInstance = M.Chips.getInstance($("#ingredient_chips"));

    appendToForm($form, chipInstance.chipsData, $('#ordering').val());

    if (!paginating) {
        $('#recipe_filter_page').val("1");
    }


    $('#recipes_loader').removeClass('hide')
    $.ajax({
        type: $form.attr('method'),
        url: '/api/recipes/',
        data: $form.serialize(),
        success: function (data) {
            console.log('Submission was successful.');
            console.log(data);
            template(data.results);

            const numPages = data.num_pages;
            let paginationHtml = "";
            const paginateWindowSize = 5;
            if (numPages > 1) {
                for (let k = 0; k < numPages; k++) {
                    paginationHtml += `
                        <li class="${parseInt(data.current_page) === k + 1 ? 'active' : ''}">
                            <a 
                                data-value="${k + 1}" 
                                class="pagination-link" 
                                href="#"> 
                                ${k + 1} 
                            </a>
                        </li>
                    `;
                }
                $('.pagination').html(paginationHtml);
                // $('.pagination').html(
                //     `
                //         <li class="disabled">
                //             <a class="pagination-link" href="#" data-value="${Math.max(parseInt(data.current_page) - 1, 1)}">
                //                 <i class="material-icons">chevron_left</i>
                //             </a>
                //         </li>
                //         <li class="active"><a href="#!">${data.current_page}</a></li>
                //         <li class="waves-effect">
                //             <a class="pagination-link" href="#" data-value="${Math.min(parseInt(data.current_page) + 1, numPages)}">
                //                 <i class="material-icons">chevron_right</i>
                //             </a>
                //         </li>
                //     `
                // )
            } else {
                $('.pagination').html('')
            }
        },
        complete: function () {
            $('#recipes_loader').addClass('hide')
        },
        error: function (data) {
            console.log('An error occurred.');
        },
    })
}


function template(recipes) {
    const $ul = $('#filtered_recipes');
    let htmlOut = "";
    for (let i = 0; i < recipes.length; i++) {
        htmlOut += `<li> <a href="${recipes[i].slugged_url}"> ${recipes[i].name} </a> </li>`;
    }

    $ul.html(htmlOut ? htmlOut : "No matching recipes...")
};

$.fn.resetToDefault = function () {
    this.each(function () {
        this.value = this.defaultValue;
    });
};

function resetForm($form, chipsInstance) {
    // clears form and delete ingredient chips
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox')
        .removeAttr('checked').removeAttr('selected');
    const numChips = chipsInstance.chipsData.length;
    for (let i = 0; i < numChips; i++) {
        chipsInstance.deleteChip();
    }

}


