$(".django-ckeditor-widget").css("display", "block")
$(".main-footer > .float-right").text("MUOJ version 0.0.1")
$('.login-logo').html('<h2> MU Online Judge </h2>')

var searchFilters = $('#changelist-search > .form-group');
searchFilters.each(function () {
    $(this).css('marginRight', '10px')
});