$(document).ready(function () {
    let chipsInstances;

    // initialize materialize css instances
    const multiSelectElems = document.querySelectorAll('select');
    const multiSelectInstances = M.FormSelect.init(multiSelectElems, {});

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
                    placeholder: '+ ingredient',
                    autocompleteOptions: {
                        data: ingredients,
                        limit: 5,
                        minLength: 1,
                    }
                });
        }
    });

    const collapsibleInstances = M.Collapsible.init($('#collapsible_filter'), {
        inDuration: 200
    });

    // retrieve those corresponding instances (will be unique)
    const chipsInstance = chipsInstances[0]; // const chipsInstance = M.Chips.getInstance($("#ingredient_chips"));
    const filterCollapseInstance = collapsibleInstances[0];
    const $recipeFilterForm = $('#recipe_filter_form');

    // retrieve intial list
    recipeSearch($recipeFilterForm)

    // event handlers

    // submit recipe search ajax
    $recipeFilterForm.submit(function (e) {
        e.preventDefault();
        recipeSearch($recipeFilterForm);
        filterCollapseInstance.close();

    })

    // submit form on ordering change
    $('#ordering').on('change', function() {
        recipeSearch(($recipeFilterForm));
    })

    // clear fields and submit recipe search
    $('#clear_fields').on('click', function (e) {
        e.preventDefault();
        resetForm($recipeFilterForm, chipsInstance);
        recipeSearch($recipeFilterForm)
        filterCollapseInstance.close();
    })

    $('ul.pagination').on('click','.pagination-link', function (e) {
        e.preventDefault();
        $('#recipe_filter_page').val($(this).data("value"));
        recipeSearch($recipeFilterForm)
    })
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

function recipeSearch($form) {
    const chipInstance = M.Chips.getInstance($("#ingredient_chips"));

    appendToForm($form, chipInstance.chipsData, $('#ordering').val())

    $('#recipes_loader').removeClass('hide')
    $.ajax({
        type: $form.attr('method'),
        url: '/api/recipes/',
        data: $form.serialize(),
        success: function (data) {
            // console.log('Submission was successful.');
            // console.log(data);
            $ul = $('#filtered_recipes');
            htmlOut = "";
            for (let i=0; i < data.length; i++) {
                htmlOut += `<li> ${data[i].name} </li>`
            }

            $ul.html(htmlOut ? htmlOut : "No matching recipes...")

            // const numPages = Math.ceil(data.count / data.page_size);
            // if (numPages > 1) {
            //
            //     $('.pagination').html(
            //         `
            //             <li class="disabled">
            //                 <a class="pagination-link" href="#" data-value="${Math.max(parseInt(data.current_page) - 1, 1)}">
            //                     <i class="material-icons">chevron_left</i>
            //                 </a>
            //             </li>
            //             <li class="active"><a href="#!">${data.current_page}</a></li>
            //             <li class="waves-effect">
            //                 <a class="pagination-link" href="#" data-value="${Math.min(parseInt(data.current_page) + 1, numPages)}">
            //                     <i class="material-icons">chevron_right</i>
            //                 </a>
            //             </li>
            //         `
            //     )
            // }
            // else {
            //     $('.pagination').html('')
            // }
        },
        complete: function () {
            $('#recipes_loader').addClass('hide')
        },
        error: function (data) {
            // console.log('An error occurred.');
        },
    })
}


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


