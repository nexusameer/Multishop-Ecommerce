(function($) {
    'use strict';

    // Configuration object
    var config = {
        cartTotalSelector: '#cart-total',
        cartTotal2Selector: '#cart-total2',
        cartItemRowSelector: '.align-middle tr',
        shippingCostSelector: '#shipping-cost',
        addToCartButtonSelector: '.add-to-cart',
        quantityButtonSelector: '.btn-plus, .btn-minus',
        removeButtonSelector: '.btn-remove'
    };

    // Helper functions
    function parsePrice(priceString) {
        return parseFloat(priceString.replace(/[^\d.]/g, '')) || 0;
    }

    function formatPrice(price) {
        return 'Rs: ' + price.toFixed(2);
    }

    function updateCartItemTotal($row) {
        var price = parsePrice($row.find('.item-price').text());
        var quantity = parseInt($row.find('.item-quantity').val(), 10) || 0;
        var total = price * quantity;
        $row.find('.item-total').text(formatPrice(total));
        return total;
    }

    function updateCartSummary() {
        var cartTotal = 0;
        var $cartItems = $(config.cartItemRowSelector);
        
        if ($cartItems.length > 0) {
            $cartItems.each(function() {
                cartTotal += updateCartItemTotal($(this));
            });
        } else {
            cartTotal = parseFloat(localStorage.getItem('cartTotal')) || 0;
        }

        var shippingCost = parsePrice($(config.shippingCostSelector).text());
        var totalWithShipping = cartTotal + shippingCost;

        $(config.cartTotalSelector).text(formatPrice(totalWithShipping));
        $(config.cartTotal2Selector).text(formatPrice(totalWithShipping));

        console.log('Cart total updated:', totalWithShipping);
        localStorage.setItem('cartTotal', totalWithShipping);
    }

    function fetchCartTotal() {
        $.ajax({
            url: '/api/cart/get_cart_total/',
            method: 'GET',
            success: function(response) {
                if (response.cart_total !== undefined) {
                    localStorage.setItem('cartTotal', response.cart_total);
                    updateCartSummary();
                }
            },
            error: function(xhr, status, error) {
                console.error("Error fetching cart total:", error);
            }
        });
    }

    // AJAX function
    function sendAjaxRequest(url, data, successCallback, errorCallback) {
        $.ajax({
            url: url,
            method: 'POST',
            data: Object.assign({}, data, { csrfmiddlewaretoken: csrftoken }),
            success: successCallback,
            error: function(xhr, status, error) {
                console.error("AJAX error:", error);
                if (errorCallback) errorCallback(error);
            }
        });
    }

    // Event handlers
    function handleAddToCart() {
        var productId = $(this).data('product-id');
        sendAjaxRequest('/api/cart/add_to_cart/', { product_id: productId, quantity: 1 },
            function(response) {
                if (response.cart_item_html) {
                    var $newRow = $(response.cart_item_html);
                    $('.align-middle').append($newRow);
                    updateCartItemTotal($newRow);
                    updateCartSummary();
                }
            },
            function() {
                alert("There was an error adding the item to your cart. Please try again.");
            }
        );
    }

    function handleQuantityChange() {
        var $button = $(this);
        var cartItemId = $button.data('cart-item-id');
        var $row = $button.closest('tr');
        var $quantityInput = $row.find('.item-quantity');
        var currentQuantity = parseInt($quantityInput.val(), 10);
        var isIncrement = $button.hasClass('btn-plus');
        var newQuantity = isIncrement ? currentQuantity + 1 : Math.max(currentQuantity - 1, 0);

        $quantityInput.val(newQuantity);
        updateCartItemTotal($row);
        updateCartSummary();

        var url = isIncrement ? '/api/cart/increment_quantity/' : '/api/cart/decrement_quantity/';
        sendAjaxRequest(url, { cart_item_id: cartItemId },
            function(response) {
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
                }
                updateCartItemTotal($row);
                updateCartSummary();
            },
            function() {
                alert("There was an error updating the quantity. Please try again.");
                $quantityInput.val(currentQuantity);
                updateCartItemTotal($row);
                updateCartSummary();
            }
        );
    }

    function handleRemoveItem() {
        var cartItemId = $(this).data('cart-item-id');
        var $row = $(this).closest('tr');

        sendAjaxRequest('/api/cart/remove_cart_item/', { cart_item_id: cartItemId },
            function() {
                $row.fadeOut(300, function() {
                    $(this).remove();
                    updateCartSummary();
                });
            },
            function() {
                alert("There was an error removing the item from your cart. Please try again.");
            }
        );
    }

    // Initialization
    function init() {
        console.log("Initializing cart functionality");

        var savedTotal = parseFloat(localStorage.getItem('cartTotal'));
        if (!isNaN(savedTotal)) {
            $(config.cartTotalSelector + ', ' + config.cartTotal2Selector).text(formatPrice(savedTotal));
        }

        if ($(config.cartItemRowSelector).length > 0) {
            updateCartSummary();
        } else {
            fetchCartTotal();
        }

        $(document).on('click', config.addToCartButtonSelector, handleAddToCart);
        $(document).on('click', config.quantityButtonSelector, handleQuantityChange);
        $(document).on('click', config.removeButtonSelector, handleRemoveItem);

        console.log("Cart functionality initialized");
    }

    // Run initialization when DOM is ready
    $(document).ready(init);

})(jQuery);