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
            .attr("name", "ingredient")
            .attr("value", tag)
            .appendTo("#recipe_filter_form");
    });
    return true;
})