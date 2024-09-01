(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });

})

// ---------------------------- this start jqurey---

$(document).ready(function(){

    $('.remove-item').click(function(e) {
        e.preventDefault();
        let uuid = $(this).data('uuid');
        console.log("UUID to remove:", uuid);
        let $tbody = $(this).closest('tbody'); 

        $.ajax({
            type: "GET",
            url: "/remove_to_cart/",
            data: {
                'uuid': uuid
            },
            success: function(data) {
                console.log("Response data:", data);
                if (data.status === '200') {  // Check if status is a string
                    $tbody.fadeOut(300, function() {
                        $(this).remove();
                    });
                } else {
                    console.error("Failed to remove item:", data);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error);
            }
        });
    });

    $('.btn-minus').click(function (e) {
        e.preventDefault();
        const $qty  = $(this).closest('.input-group').find('.quantity-input');
        let qty = parseInt($qty.val())

        if(qty > 1) {
            let newQty = qty - 1
            $qty.val(newQty);
        }
    })

    $('.btn-plus').click(function (e) { 
        e.preventDefault();
        const $qty  = $(this).closest('.input-group').find('.quantity-input');
        let qty = parseInt($qty.val())
          
        if(qty >= 10 ) {
            alert('You can not add more than 10 items')
        }
        else{ 
            let newQty = qty + 1
            $qty.val(newQty);         
        }  
    });

    $('.changeqty').click(function (e) { 
        e.preventDefault();
    
        const $qty = $(this).closest('.input-group').find('.quantity-input');
        const $id = $(this).closest('.input-group').find('#pid');
        let qty = parseInt($qty.val())
        const $total = $(this).closest('tr').find('#fprice').text().trim();
        const priceText = $total.replace('₹', '').replace(',', '');
        let price = parseFloat(priceText);
        const $totalAmountElement = $(this).closest('tr').find('.total-amount');
        const subtotalElement = $('.border-bottom').find('#Subtotal');
        const finalAmount = $('.pt-2').find('#finalamount')
        const shippingCharges = $('.justify-content-between').find('#shipingCharges');
        
        $.ajax({
            type: "GET",
            url: "/changeQty/",
            data: {
                'id': $id.val(),
                'qty': qty,
                'price': price
            },
            success: function (data) {

                let newTotal = data.total
                subtotalElement.text(`₹${data.subtotal.toFixed(2)}`)
                finalAmount.text(`₹${data.finalAmount.toFixed(2)}`)
                $totalAmountElement.text(`₹${newTotal.toFixed(2)}`)
                shippingCharges.text(data.shippingCharges)
                if (data.subtotal >= 1000){
                    shippingCharges.text(0)
                } else {
                    shippingCharges.text(data.shippingCharges)
                }

            },
            error: function (status, error) {
                console.error('AJAX request failed:', status, error);
            }
        }); 
    });

})

