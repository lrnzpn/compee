function addToWishlist(pk) {
    var product_id = pk;
    var button = document.getElementById("AddWishlist");
    var url = button.value;
    $.ajax({
        url: url,
        data: {
            'product_id': product_id
        },
        success: function(data) {
        }
    });
}

function addToCart(pk) {
    var product_id = pk;
    var button = document.getElementById("AddCart");
    var url = button.value;
    var quantity = 1;
    if(document.getElementById('quantity')){
        quantity = quantity.value;
    }
    $.ajax({
        url: url,
        data: {
            'product_id':pk,
            'quantity': quantity
        },
        success: function(data) {
        }
    });
}