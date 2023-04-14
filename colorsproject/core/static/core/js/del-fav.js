$(".form__button").click(function() {
	var id = $(this).attr("id");
	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
    });
    $.ajax({
		url : 'api/fav',
		type: 'delete',
		data : {'car_id': id}
	}).done(function(xhr){
		$(`[class="frame"][id="${id}"]`).remove();
	}).fail(function (xhr) {
		var data = xhr.responseJSON;
		console.log(data);
		$('.color_message').html(data.error)
		$('.color_message').show();
	});
	console.log($('.frame').length)
	if ($('.frame').length==1) {$('.car_container').append('<div class="fav_message">Нет ни одной машины в избранном')};
})
