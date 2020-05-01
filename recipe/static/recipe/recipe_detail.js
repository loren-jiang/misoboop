document.addEventListener("DOMContentLoaded", function () {
    var elems = document.querySelectorAll(".dropdown-range.dropdown-trigger");
    var instances = M.Dropdown.init(elems, {
        hover: false,
        coverTrigger: false,
        constrainWidth: false,
        closeOnClick: false
    });

    var servingsRangeInput = document.getElementById("num_servings");
    var sliderTarget = document.getElementById(servingsRangeInput.dataset.target);
    sliderTarget.innerHTML = servingsRangeInput.value;

    servingsRangeInput.addEventListener("input", function () {
        sliderTarget.innerHTML = this.value;
    });

    initializeToggleIconCollapsible(
        '.direction-ingredients.collapsible',
        '.direction-ingredients.collapsible .material-icons',
        'arrow_drop_up',
        'arrow_drop_down',
        {
            inDuration: 200,
        }
    );

    // floating action buttons
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

    /* On servings change, scale ingredients accordingly */
    const $servings = $('#num_servings');
    const origServings = recipe_servings;
    const $ingredientAmt = $('span.ingredient-amount');
    const ingredientDefaultValues = ($ingredientAmt.toArray().map(el => parseFloat(el.innerHTML)));

    $servings.on('change', function () {

        $ingredientAmt.each(
            (idx, el) => {
                $(el).html(ingredientDefaultValues[idx] * $servings.val() / origServings)
            }
        )
    })

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
;


