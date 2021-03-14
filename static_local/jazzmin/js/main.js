$(".django-ckeditor-widget").css("display", "block")
$(".main-footer > .float-right").text("MUOJ version 0.0.1")
$('.login-logo').html('<h2> MU Online Judge </h2>')

$(document).ready(function () {
    $('.related-widget-wrapper').find('.select2').each(function () {
        console.log($(this))
        $(this).css({
            maxWidth: "570px",
            height: "38px"
        })
    });
})