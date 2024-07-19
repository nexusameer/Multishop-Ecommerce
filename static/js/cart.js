$(document).ready(function() {
    function updateCartItemTotal($row) {
        var priceText = $row.find('.item-price').text().replace('Rs:', '').trim();
        var price = parseFloat(priceText) || 0;
        var quantityText = $row.find('.item-quantity').val().trim();
        var quantity = parseInt(quantityText, 10) || 0;
        var total = price * quantity;
        $row.find('.item-total').text('Rs: ' + total.toFixed(2));
        return total;
    }

    function updateCartSummary() {
        var cartTotal = 0;
        $('.align-middle tr').each(function() {
            cartTotal += updateCartItemTotal($(this));
        });
        $('#subtotal').text('Rs: ' + cartTotal.toFixed(2));
        var shippingCost = parseFloat($('#shipping-cost').text().replace('', '')) || 0;
        var totalWithShipping = cartTotal + shippingCost;
        $('#cart-total').text('Rs: ' + totalWithShipping.toFixed(2));
    }

    updateCartSummary();

    $(document).on('click', '.add-to-cart', function() {
        var productId = $(this).data('product-id');
        $.ajax({
            url: '/api/cart/add_to_cart/',
            method: 'POST',
            data: {
                product_id: productId,
                quantity: 1,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                if (response.cart_item_html) {
                    var $newRow = $(response.cart_item_html);
                    $('.align-middle').append($newRow);
                    updateCartItemTotal($newRow);
                    updateCartSummary();
                } else {
                    console.error("Invalid response format:", response);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error adding to cart:", error);
                alert("There was an error adding the item to your cart. Please try again.");
            }
        });
    });

    $(document).on('click', '.btn-plus, .btn-minus', function() {
        var cartItemId = $(this).data('cart-item-id');
        var $row = $(this).closest('tr');
        var $quantityInput = $row.find('.item-quantity');
        var currentQuantity = parseInt($quantityInput.val(), 10);
        var isIncrement = $(this).hasClass('btn-plus');

        var newQuantity = isIncrement ? currentQuantity + 1 : Math.max(currentQuantity - 1, 0);
        $quantityInput.val(newQuantity);

        updateCartItemTotal($row);
        updateCartSummary();

        $.ajax({
            url: isIncrement ? '/api/cart/increment_quantity/' : '/api/cart/decrement_quantity/',
            method: 'POST',
            data: {
                cart_item_id: cartItemId,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                var serverQuantity = parseInt(response.new_quantity, 10);
                if (!isNaN(serverQuantity)) {
                    if (serverQuantity > 0) {
                        $quantityInput.val(serverQuantity);
                    } else {
                        $row.fadeOut(300, function() {
                            $(this).remove();
                            updateCartSummary();
                        });
                    }
                } else {
                    console.error("Invalid quantity response:", response);
                    $quantityInput.val(currentQuantity);
                }
                updateCartItemTotal($row);
                updateCartSummary();
            },
            error: function(xhr, status, error) {
                console.error("Error updating quantity:", error);
                alert("There was an error updating the quantity. Please try again.");
                $quantityInput.val(currentQuantity);
                updateCartItemTotal($row);
                updateCartSummary();
            }
        });
    });

    $(document).on('click', '.btn-remove', function() {
        var cartItemId = $(this).data('cart-item-id');
        var $row = $(this).closest('tr');

        $.ajax({
            url: '/api/cart/remove_cart_item/',
            method: 'POST',
            data: {
                cart_item_id: cartItemId,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                $row.fadeOut(300, function() {
                    $(this).remove();
                    updateCartSummary();
                });
            },
            error: function(xhr, status, error) {
                console.error("Error removing cart item:", error);
                alert("There was an error removing the item from your cart. Please try again.");
            }
        });
    });
});