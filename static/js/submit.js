$("input:file").change(function (){
	$('#upload-file-info').html($(this).val().replace('C:\\fakepath\\',''));
});
