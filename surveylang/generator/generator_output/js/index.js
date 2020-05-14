/* Generated on: Tue, May 12, 2020 17:22:49
Generated based on the template: survey_js.j2 */

$(document).ready(function(){
    $("form#myForm").submit(submitFunction(event));

	$.validator.messages.required = 'This field is required';
	$.validator.messages.email = 'Please enter a valid email address';
	$.validator.messages.maxlength = $.validator.format("Please enter no more than {0} characters.");
	$.validator.messages.minlength = $.validator.format("Please enter at least {0} characters.");
	$.validator.messages.number = 'Please enter a number';
	$.validator.messages.max = $.validator.format("Please enter a value less than or equal to {0}.");
    $.validator.messages.min = $.validator.format("Please enter a value greater than or equal to {0}.");

	$("form#myForm").validate({
		onkeyup : false,
		onclick : false,
		onfocusout : false,
		// validation rules definition
		rules: {
			Question0: {
				required: true,

			},

			Question1: {
				required: true,

			},

			Question2: {
				required: false,

			},

			Question3: {
				required: true,

			},

			Question4: {
				required: true,

			},

			Question5: {
				required: false,

			},

			Question6: {
				required: false,
				min: 0,
				max: 24,

			},

			Question7: {
				required: true,

			},

			Question8: {
				required: true,

			},

			Question9: {
				required: true,

			},

			Question10: {
				required: false,
				maxlength: 200,

			},

		},
		highlight: function (element, errorClass, validClass) {
			$(element).closest("div.card-question").addClass('errorBorder');
			$(element).addClass('errorTemplate');
			$(element).removeClass('errorTemplate');
		}, 
		unhighlight: function (element, errorClass, validClass) {
			$(element).closest("div.card-question").removeClass('errorBorder');
		},
		errorPlacement : function(error, element) {
			if(!element.is(':radio') && !element.is(':checkbox')) {
				error.addClass('errorMessage')
				error.insertAfter(element);
			}
		}

	});

	$('.alert-close').click(function(){
		$(this).parent().hide();
	})
});

function submitFunction(e) {
	return function(e) {
		e.preventDefault();
		var isValid = $("form#myForm").valid();

		if(isValid) {
			$.ajax({
				url: 'https://en96sm60rk9gv.x.pipedream.net',
				type: 'POST',
				data: $('#myForm').serialize(),
				success: function(){
					$('#myForm')[0].reset();

					$("#successAlertBox").fadeIn();
					closeSuccessAlertBox();
				},
				error: function (message) {
					$("#errorAlertBox").fadeIn();
					closeErrorAlertBox();
				}
			});
			return false;	
		}
		return false;
	}
}

function closeSuccessAlertBox(){
	window.setTimeout(function () {
	  $("#successAlertBox").fadeOut(300)
	}, 3000);
}

function closeErrorAlertBox(){
	window.setTimeout(function () {
	  $("#errorAlertBox").fadeOut(300)
	}, 3000);
}