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