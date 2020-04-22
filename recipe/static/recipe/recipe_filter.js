$(function () {
    $.ajax({
        type: 'GET',
        url: '/api/ingredients/',
        success: function (response) {
            const $chips = $('#ingredient_chips');
            let ingredients = {}
            for (let i = 0; i < response.length; i++) {
                if (Object.prototype.toString.call(response[i].name) === "[object String]") {
                    ingredients[response[i].name] = null;
                }
            }

            $chips.chips({
                placeholder: '+ ingredient',
                autocompleteOptions: {
                    data: ingredients,
                    limit: 5,
                    minLength: 1,
                }
            });

        }
    });
});

$("#recipe_filter_form").submit(function (e) {
    const chipInstance = M.Chips.getInstance($("#ingredient_chips"));
    chipInstance.chipsData.map(el => el.tag).forEach(tag => {
        $("<input />").attr("type", "hidden")
            .attr("name", "ingredients")
            .attr("value", tag)
            .appendTo("#recipe_filter_form");
    });
    return true;
})

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('#collapsible_filter');
    var instances = M.Collapsible.init(elems, {
        inDuration: 200
    });
});

function resetForm($form) {
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox')
        .removeAttr('checked').removeAttr('selected');
}

$('#clear_fields').on('click', function (e) {
    e.preventDefault();
    resetForm($('#recipe_filter_form')); // by id, recommended
    const chipInstance = M.Chips.getInstance($("#ingredient_chips"));
    const numChips = chipInstance.chipsData.length
    for (let i = 0; i < numChips; i++) {
        chipInstance.deleteChip();
    }
    const instance = M.Collapsible.getInstance($('#collapsible_filter'));
    instance.close()
    $('#recipe_filter_form').submit()
    return false;
})

$('#ordering').on('change', function () {
    $('#recipe_filter_form').submit()
})