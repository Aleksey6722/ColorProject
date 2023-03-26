$("#form").submit(function(event){
	event.preventDefault(); 
	var post_url = $(this).attr("action"); 
	var request_method = $(this).attr("method"); 
	var form_data = $(this).serializeArray(); 
	var data = {};
	$(form_data).each(function(index, obj){
	    data[obj.name] = obj.value;
	});
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
		// $("#message").html(xhr.email);
		// $("#message").css("display", "block");
		// window.location.href = "/";
		if(post_url == "/signup") {
			window.location.href = "/signin";
		} else {
			window.location.href = "/";
		};		
	}).fail(function (xhr) {
		console.log(xhr);
		// console.log(xhr.responseJSON.error);
		$("#message").html(xhr.responseJSON.error);
		$("#message").css("display", "block");
	});
});