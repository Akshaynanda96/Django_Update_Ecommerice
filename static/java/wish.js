$(document).ready(function () {
    
    $('.product-action').click(function (e) { 
        e.preventDefault();
        const id = $(this).closest('.product-img').find('#uuid');
        const uuid = id.val();
        console.log(uuid);
        $.ajax({
            type: "GET",
            url: "url",
            data: "data",
            dataType: "dataType",
            success: function (response) {
                
            }
        });
        
    });

});