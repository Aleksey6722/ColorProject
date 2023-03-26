$('#form').on('click', '.password__checkbox', function(){
    if ($(this).is(':checked')){
        $('#password-input').attr('type', 'text');
    } else {
        $('#password-input').attr('type', 'password');
    }
});

