// multishop/static/js/cart.js

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $('.add-to-cart').click(function() {
        var productId = $(this).data('product-id');
        $.ajax({
            url: '/api/cart/add_to_cart/',
            method: 'POST',
            data: {
                product_id: productId,
                quantity: 1,
            },
            success: function(response) {
                alert('Product added to cart successfully!');
                // Optionally update cart UI here
            },
            error: function(response) {
                alert('Error adding product to cart.');
            }
        });
    });
});
    