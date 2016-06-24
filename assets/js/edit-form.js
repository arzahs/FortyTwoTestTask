$(document).ready(function () {

    $("#status_save").hide();
    $("#status_error").hide();
    
    $.ajax({
        method: 'GET',
        url: '/',
        dataType: 'json',
        success: function (data) {
            $("#id_name").val(data['name']);
            $("#id_contacts").val(data['contacts']);
            $("#id_birthday").val(data['birthday']);
            $("#id_last_name").val(data['last_name']);
            $("#id_skype").val(data['skype']);
            $("#id_email").val(data['email']);
            $("#id_jabber").val(data['jabber']);
            $("#id_bio").text(data['bio']);
            $("#id_other_contacts").text(data['other_contacts']);
            $("#id_photo").val(data['photo']);
            $("#photo").attr('src', data['photo']);
            $("#photo").show();
            $("#status_load").hide();
        }
    });

    $(function() {
        $( "#id_birthday" ).datepicker({ dateFormat: 'yy-mm-dd' });
    }); 

}
);