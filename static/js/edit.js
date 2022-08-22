function flash(msg){
	$('#flashes').append('<div class="alert alert-info fade in"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + msg + '</div>')
}

function save_all(url){
	$('form').each(function(index, form){
		$.ajax({
			type : "POST",
			url : url,
			data: $(form).serialize(),
			success: function(errors) {
				fields = $(form).find('.form-group');
				fields.attr('class', 'form-group');
				// fields.addClass('has-success has-feedback');
				// fields.children('span').remove();
				// fields.append('<span class="glyphicon glyphicon-ok form-control-feedback"></span>');
				for (var fieldname in errors) {
					field = $(form).find('#'+fieldname).children('.form-group');
					field.attr('class', 'form-group');
					field.addClass('has-error has-feedback');
					// field.children('span').remove();
					// field.append('<span class="glyphicon glyphicon-remove form-control-feedback"></span>');
				}
			}
		});
	})
}