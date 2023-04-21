function sendColor () {
	$('.color_message').remove();
	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
    })
	$.ajax({
		url : 'api/find-cars',
		type: 'get',
		data : {'c': $('#text').val(), 'n': $('#num').val()}
	}).done(function(xhr){
		$('#car-container').empty()
		console.log(xhr);
		$.each(xhr, function(index, element) {
			$('#car-container').append(`<div class='frame'><img class="image" src="${element.url}.jpg" align="left"><label>Цвет: <span>#${element.color}</span></label><div class="colorbox" style="background-color: #${element.color};"></div><br><p>Марка: <span>${element.brand}</span></p><p>Модель: <span>${element.model}</span></p><p>Страна: <span>${element.country}</span></p><button id="${element.id}" class="form__button">Добавить в избранное</button><button id="${element.id}" class="added__button" style="display: none">Добавлено</button></div>`);
		});
		$('#car-container').append('<script type="text/javascript" src="/static/core/js/send-fav.js" %}"></script>')
	}).fail(function (xhr) {
		var data = xhr.responseJSON
		console.log(xhr)
		console.log(data);
		$.each(data, function(index, element) {
			var message = ''
			console.log(index);
			console.log(element[0]);
			if(index == 'n'){
				message = 'Введите целое число больше нуля'
			} else if (index =='color') {
				message = 'Введите корректное значение цвета в формате HEX'
			} else {
				message=element[0]
			}
			$('#div_error').append(`<div class="color_message" style="">${message}</div>`);
		});		
	});
}