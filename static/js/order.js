$(".payment-confirm-order").click(function(){
        $("#form-submitted").addClass('active');
        setTimeout(function(){
            var redirect_to;
            var card_num = $("input[name=card_num]").val();
            var exp_date = $("input[name=exp_date]").val();
            var cvv = $("input[name=cvv]").val();
            var cardholder = $("input[name=cardholder]").val();
    
            var valid = false
    
            $.ajax({
                type: "POST",
                async : false,
                url: window.location.pathname,
                data: {
                  'card_num': card_num, 
                  'exp_date':exp_date, 
                  'cvv': cvv,
                  'cardholder': cardholder,
                  'csrfmiddlewaretoken': csrftoken
                },
                dataType: "json",
                success: function(data){
                    console.log(data)
                    if(data.data.status === 1) {
                        valid = true
                        if(data.data.transaction_status === 2 || data.data.transaction_status === 1 || data.data.transaction_status === 3){
                            redirect_to = data.data.authurl
                        } else if(data.data.transaction_status === 0){
                            $("#form-submitted").removeClass('active');
                            alert('Oops. Looks like your card details are invalid.');
                        }
                    } else {
                      if(data.data.validate.check_card === 0 && data.data.validate.check_exp === 0) {
                        alert('Please use a different card')
                        valid = false
                      } else if (data.data.validate.check_exp === 0) {
                        alert('Card expired')
                        valid = false
                      } else if (data.data.validate.check_card === 0) {
                        alert('Card invalid')
                        valid = false
                      } else if (data.errors !== undefined || data.errors.length != 0 || data.pm == '') {
                        alert('Card invalid')
                        valid = false
                      }
                    }
                }
            });
    
            if(!valid) return valid

            if(redirect_to){
                console.log(redirect_to)
                window.location.href = redirect_to
            }else{
                console.log(redirect_to)
                $("#form-submitted").removeClass('active');
                alert('Oops. Looks like your card details are invalid.');
            }
        }, 100);
        
});