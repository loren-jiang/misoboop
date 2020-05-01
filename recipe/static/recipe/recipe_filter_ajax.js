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

        $recipeFilterForm.find('#recipe_name_input, #recipe_search_input').keyup(debounce(function () {
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
    // console.log('new search')
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
            // console.log('Submission was successful.');
            // console.log(data);
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
            } else {
                $('.pagination').html('')
            }
        },
        complete: function () {
            $('#recipes_loader').addClass('hide')
        },
        error: function (data) {
            // console.log('An error occurred.');
        },
    })
}


function template(recipes) {
    const $ul = $('#filtered_recipes');
    let htmlOut = `<table class=''><tr><th>Name</th><th>Tags</th><th>Image</th></tr> <tbody>`;
    for (let i = 0; i < recipes.length; i++) {
        formattedTags = ``;
        console.log(recipes[i])
        for (let k = 0; k < recipes[i].tags.length; k++) {
            formattedTags += `<span class="chip"> ${recipes[i].tags[k]} </span>`
        }
        htmlOut += `<tr> 
                        <td>
                            <a href="${recipes[i].slugged_url}"> ${recipes[i].name} </a>
                        </td> 
                        <td>${formattedTags}</td>
                        <td><img class="" width="auto" height="100" src="${recipes[i].image ? recipes[i].image.thumbnail : recipes[i].placeholder_url}"></td>
                    </tr>`;
    }
    htmlOut += `</tbody> </table>`;
    $ul.html(recipes.length ? htmlOut : `<p>No recipes found... <br> <div class="table-flip">(╯°□°)╯︵ ┻━┻</div></p>`)
};

$.fn.resetToDefault = function () {
    this.each(function () {
        this.value = this.defaultValue;
    });
};

function resetForm($form, chipsInstance) {
    // clears form and delete ingredient chips
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox').removeAttr('checked').removeAttr('selected');
    const numChips = chipsInstance.chipsData.length;
    for (let i = 0; i < numChips; i++) {
        chipsInstance.deleteChip();
    }

}


