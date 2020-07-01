$(function (){
	function render_time() {
		return moment($(this).data('timestamp')).format('l')
	}
	$('[data-toggle="tooltip"]').tooltip(
		{title:render_time}
	);
});

// hide or show tag edit form
$('#tag-btn').click(function () {
	$('#tags').hide();
	$('#tag-form').show();
});
$('#cancel-tag').click(function () {
	$('#tag-form').hide();
	$('#tags').show();
});

 // delete confirm modal
 $('#confirm-delete').on('show.bs.modal', function (e) {
	$('.delete-form').attr('action', $(e.relatedTarget).data('href'));
});


$(document).ready(function(){
	$('[data-toggle="popover-hover"]').popover({
		 //trigger: 'focus',
		 trigger: 'hover',
		 html: true,
		 placement: 'bottom',
		 content: function () {
			   return '<img class="img-fluid" src="'+$(this).data('img') + '" />';
		 }
   }) 
});

$(document).ready(function(){
	$('.sidenav').sidenav();
});