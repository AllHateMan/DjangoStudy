// Когда html документ готов (прорисован)
$(document).ready(function () {
    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    // При клике по значку корзины открываем всплывающее(модальное) окно
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function() {
        var selectedValue = $(this).val();
        // Скрываем или отображаем input ввода адреса доставки
        $("#deliveryAddressField")[selectedValue === "1" ? "show" : "hide"]();
    });
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Оновлюємо повідомлення
                successMessage.html(data.message).fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Оновлюємо лічильник
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Оновлюємо вміст корзини
                $("#cart-items-container").html(data.cart_items_html);
                
                // Перевіряємо оновлення
                console.log("Оновлення корзини:", data.cart_items_html);
            },
            error: function (data) {
                console.log("Помилка при додаванні товару в корзину");
            },
        });
    });

    // Видалення товару з корзини
    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();
        var goodsInCartCount = $("#goods-in-cart-count");
        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Оновлюємо повідомлення
                successMessage.html(data.message).fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Оновлюємо лічильник загальної кількості
                goodsInCartCount.text(data.total_quantity);

                // Оновлюємо вміст корзини
                $("#cart-items-container").html(data.cart_items_html);
                
                // Показуємо/приховуємо кнопку створення замовлення
                if (data.total_quantity > 0) {
                    $(".order-button-container").show();
                } else {
                    $(".order-button-container").hide();
                }
            },
            error: function (data) {
                console.log("Помилка при видаленні товару з корзини");
            },
        });
    });

    // Зменшення кількості товару
    $(document).on("click", ".decrement", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());
        
        if (currentValue > 1) {
            var newValue = currentValue - 1;
            updateCart(cartID, newValue, url);
            $input.val(newValue);
        }
    });

    // Збільшення кількості товару
    $(document).on("click", ".increment", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());
        
        var newValue = currentValue + 1;
        updateCart(cartID, newValue, url);
        $input.val(newValue);
    });

    // Функція оновлення кошика
    function updateCart(cartID, quantity, url) {
        var successMessage = $("#jq-notification");
        
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Оновлюємо повідомлення
                successMessage.html(data.message).fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Оновлюємо вміст корзини
                $("#cart-items-container").html(data.cart_items_html);
                
                // Оновлюємо загальну кількість товарів
                $("#goods-in-cart-count").text(data.total_quantity);
                
                // Показуємо/приховуємо кнопку створення замовлення
                if (data.total_quantity > 0) {
                    $(".order-button-container").show();
                } else {
                    $(".order-button-container").hide();
                }
                
                console.log("Кошик оновлено:", data);
            },
            error: function (xhr, status, error) {
                console.log("Помилка:", error);
                console.log("Статус:", status);
                console.log("Відповідь:", xhr.responseText);
            },
        });
    }
});