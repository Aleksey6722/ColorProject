$(".form__button").click(function() {
	$('.color_message').remove();
	var id = $(this).attr("id");
	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
    })
    $.ajax({
		url : 'api/fav',
		type: 'post',
		data : {'car_id': id}
	}).done(function(xhr){
		$(`[class="form__button"][id="${id}"]`).hide();
		$(`[class="added__button"][id="${id}"]`).show();
	}).fail(function (xhr) {
		$('.color_message').remove();
		var data = xhr.responseJSON;
		console.log(data);
		$('#div_error').append(`<div class="color_message" style="">${data.error}</div>`);
	})
})

$(".added__button").click(function() {
	$('.color_message').remove();
	var id = $(this).attr("id");
	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
    })
    $.ajax({
		url : 'api/fav',
		type: 'delete',
		data : {'car_id': id}
	}).done(function(xhr){
		$(`[class="form__button"][id="${id}"]`).show();
		$(`[class="added__button"][id="${id}"]`).hide();
	}).fail(function (xhr) {
		var data = xhr.responseJSON;
		console.log(data);
		$('#picker').append(`<div class="color_message" style="display: block;">${data.error}</div>`);
	})
})