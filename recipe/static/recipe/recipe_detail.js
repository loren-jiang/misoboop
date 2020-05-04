document.addEventListener("DOMContentLoaded", function () {
    /* Servings range input */

    // Initialize materialize css dropdown for servings input change
    $('.dropdown-range.dropdown-trigger').dropdown({
        hover: false,
        coverTrigger: false,
        constrainWidth: false,
        closeOnClick: false
    });

    // Gather DOM elements needed
    const $servingsRangeInput = $('#num_servings');
    const $sliderTarget = $('#'+$servingsRangeInput.data('target'));

    // Set initial value
    $sliderTarget.html($servingsRangeInput.val());

    // On input, change slider target html
    $servingsRangeInput.on('input', function() {
       $sliderTarget.html($(this).val());
    });

    /* On servings change, scale ingredients accordingly */
    const origServings = recipe_servings; // passed Django context variable (see inline js)
    const $ingredientAmt = $('span.ingredient-amount');
    const ingredientDefaultValues = ($ingredientAmt.toArray().map(el => parseFloat(el.innerHTML)));

    // Initialize ingredient amounts to input value
    displayIngAmt($ingredientAmt, ingredientDefaultValues, origServings, $servingsRangeInput.val());

    // On inout change, change ingredient amount displays
    $servingsRangeInput.on('change', () => displayIngAmt($ingredientAmt, ingredientDefaultValues, origServings, $servingsRangeInput.val()));

    // On button reset, return values accordingly to original servings
    $('#reset_servings').on('click', function () {
        $servingsRangeInput.val(recipe_servings);
        $sliderTarget.html(recipe_servings);
        $servingsRangeInput.change();
    })

    /* Direction ingredient amounts collapsibles */

    // Initialize collapsibles for ingredient amounts displays on directions
    initializeToggleIconCollapsible(
        '.direction-ingredients.collapsible',
        '.direction-ingredients.collapsible .material-icons',
        'arrow_drop_up',
        'arrow_drop_down',
        {
            inDuration: 200,
        }
    );

    /* Floating action buttons */
    $('.fixed-action-btn').floatingActionButton({
        hoverEnabled: false
    });

    $('.fixed-action-btn').blur(function () {
        $(this).floatingActionButton('close')
    })


    var anchorElement = $('#content_copy');
    const copyCopyTooltipOriginalMsg = anchorElement.attr('data-tooltip');

    if ($(window).width() > 600) {
        $('.mobile-fab-tip').addClass('hide');

    } else {
        $('.material-tooltip').addClass('hide');
    }


    // anchorElement.on('click', function () {
    //     const msg = copyTextToClipboard(location.href);
    //     if (msg === 'successful') {
    //         anchorElement.attr('data-tooltip', 'Url copied');
    //         M.Tooltip.getInstance(anchorElement).destroy();
    //         anchorElement.tooltip();
    //         M.Tooltip.getInstance(anchorElement).open();
    //
    //         //resets tooltip to original after set delay
    //         //setTimeout(function () {
    //         //  M.Tooltip.getInstance(anchorElement).destroy();
    //         //anchorElement.attr('data-tooltip', copyCopyTooltipOriginalMsg);
    //         //anchorElement.tooltip();
    //         //}, 1500)
    //     }
    // })
    //
    // anchorElement.on('mouseout touchmove blur', function () {
    //     M.Tooltip.getInstance(anchorElement).destroy();
    //     anchorElement.attr('data-tooltip', copyCopyTooltipOriginalMsg);
    //     anchorElement.tooltip();
    // })


    /* Click respective share link on mobile-fab-tip click */
    $('.mobile-fab-tip').click(function (e) {
        e.preventDefault();
        document.getElementById($(this).data('href')).click(); // can't use jQuery here
    })

    /* Like button */
    $('#like_plus_one').on('click', function () {
        $(this).addClass("liked")
        $.ajax({
            url: 'like/',
            data: {
                'id': recipe_id
            },
            dataType: 'json',
            success: function (data) {
                if (data) {
                    $('#like_count').html(data.numLikes)
                }
            }
        });
    });

})


const decToFracMap = {
    '10': '1/8',
    '11': '1/8',
    '12': '1/8',
    '13': '1/8',
    '14': '1/8',
    '15': '1/8',
    '16': '1/8',
    '17': '1/8',
    '18': '1/8',
    '19': '1/4',
    '20': '1/4',
    '21': '1/4',
    '22': '1/4',
    '23': '1/4',
    '24': '1/4',
    '25': '1/4',
    '26': '1/4',
    '27': '1/4',
    '28': '1/4',
    '29': '1/4',
    '30': '1/3',
    '31': '1/3',
    '32': '1/3',
    '33': '1/3',
    '34': '1/3',
    '35': '1/3',
    '36': '3/8',
    '37': '3/8',
    '38': '3/8',
    '39': '3/8',
    '40': '3/8',
    '41': '3/8',
    '42': '3/8',
    '43': '3/8',
    '44': '1/2',
    '45': '1/2',
    '46': '1/2',
    '47': '1/2',
    '48': '1/2',
    '49': '1/2',
    '50': '1/2',
    '51': '1/2',
    '52': '1/2',
    '53': '1/2',
    '54': '1/2',
    '55': '1/2',
    '56': '1/2',
    '57': '5/8',
    '58': '5/8',
    '59': '5/8',
    '60': '5/8',
    '61': '5/8',
    '62': '5/8',
    '63': '5/8',
    '64': '5/8',
    '65': '2/3',
    '66': '2/3',
    '67': '2/3',
    '68': '2/3',
    '69': '2/3',
    '70': '2/3',
    '71': '3/4',
    '72': '3/4',
    '73': '3/4',
    '74': '3/4',
    '75': '3/4',
    '76': '3/4',
    '77': '3/4',
    '78': '3/4',
    '79': '3/4',
    '80': '3/4',
    '81': '3/4',
    '82': '7/8',
    '83': '7/8',
    '84': '7/8',
    '85': '7/8',
    '86': '7/8',
    '87': '7/8',
    '88': '7/8',
    '89': '7/8',
    '90': '7/8',
    '91': '7/8',
    '92': '7/8',
    '93': '7/8',
    '94': '1',
    '95': '1',
    '96': '1',
    '97': '1',
    '98': '1',
    '99': '1',
    '00': '0',
    '01': '0',
    '02': '0',
    '03': '0',
    '04': '0',
    '05': '0',
    '06': '0',
    '07': '1/8',
    '08': '1/8',
    '09': '1/8'
}


function displayIngAmt(ingredientAmounts, defaultValues, origServings, currServings) {
    ingredientAmounts.each(
        (idx, el) => {
            const numOut = defaultValues[idx] * currServings / origServings;
            if (imperial_ingredients_set.has($(el).data('name'))) {
                const splitNum = numOut.toFixed(2).split('.');
                const frac = splitNum[1] === '00' ? '' : parseFrac(decToFracMap[splitNum[1]]);
                const base = splitNum[0] === '0' ? '' : splitNum[0];
                $(el).html(base + ' ' + frac)
            } else {
                $(el).html(numOut)
            }

        }
    )

}

function parseFrac(fracStr) {
    const splitFrac = fracStr.split('/');
    return `<sup>${splitFrac[0]}</sup>&frasl;<sub>${splitFrac[1]}</sub>`
}