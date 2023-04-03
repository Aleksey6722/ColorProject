 $("#form").submit(function(event){
	event.preventDefault(); 
	$('.message').hide();
	var post_url = $(this).attr("action"); 
	var request_method = $(this).attr("method"); 
	var form_data = $(this).serializeArray(); 
	var data = {};
	$(form_data).each(function(index, obj){
	    data[obj.name] = obj.value;
	});
	delete data['csrfmiddlewaretoken'];
	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
    })
	$.ajax({
		url : post_url,
		type: request_method,
		dataType: 'json',
		contentType : 'application/json',
		data : JSON.stringify(data)
	}).done(function(xhr){
		console.log(xhr); 
		if(post_url == "/api/signup") {
			window.location.href = "/signin";
			console.log(xhr);
		} else {
			window.location.href = "/";
		};		
	}).fail(function (xhr) {
		var i=0;
		var data = xhr.responseJSON;
		console.log(data);
		for (var key in data) {
			i++;
			// console.log(data[key][0].message)
			$(`#message${i}`).html(data[key][0].message);
			$(`#message${i}`).show();
		};
	});
});