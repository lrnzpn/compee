
function receiveOrder(pk) {
    var order_id = pk;
    var button = document.getElementById("recOrder");
    var url = button.value;
    $.ajax({
        url: url,
        data: {
            'order_id': order_id
        },
        success: function(data) {
            location.reload();
        }
    });
}

function addToWishlist(pk, type) {
    var button = document.getElementById("AddWishlist");
    var url = button.value;
    $.ajax({
        url: url,
        data: {
            'id': pk,
            'type':type
        },
        success: function(data) {
            location.reload();
        }
    });
}

function addToCart(pk, type) {
    var button = document.getElementById("AddCart");
    var url = button.value;
    var quantity = 1;
    var quantityInput = document.getElementById('quantityInput');
    if(quantityInput){
        quantity = quantityInput.value;
    }
    $.ajax({
        url: url,
        data: {
            'id':pk,
            'type':type,
            'quantity': quantity
        },
        success: function(data) {
            location.reload();
        }
    });
}

$("#order-filter").change(function () {
    var url = $("#order-table").attr("data-sort-url");
    var optionSel = $(this).val();  
    $.ajax({                      
      url: url,                    
      data: {
        'option': optionSel      
      }, 
      success: function(data){
        var n = data.includes('<table');
        if (n){
            var divStart = '<table border="1">';
            var divClose = '<div class="order-sort">';
            var newData = data.substring(data.indexOf(divStart), data.indexOf(divClose));
            $("#order-table").html(newData);
        } else{
            var newData = "<h3>There are no orders to display.</h3>";
            $("#order-table").html(newData);
        }
      }
    });
  });

// for compee conceirge
$('.question-header').click(function() { 
    $(this).find('i').toggleClass('fas fa-plus fas fa-minus'); 
}); 

// for compee cares
$('.cares-header').click(function() { 
    $(this).find('i').toggleClass('fas fa-plus fas fa-minus'); 
}); 

// for indiv vendor
$('.btn-more').click(function () { 
    $(this).find('i').toggleClass('fas fa-chevron-down fas fa-chevron-up'); 
}); 



