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
    
    
    $("#id_photo").change(function () {
        if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#photo").show().attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
    });


    $("#edit_form").ajaxForm({
        beforeSubmit: function () {
            $("#status_save").show();
            $('input').prop('disabled', true);
            $('textarea').prop('disabled', true);

        },
        success: function () {
            $("#status_success").show();
          setTimeout(function(){
              location.reload()
          }, 5000);

        },
        error: function () {
            $("#status_save").hide();
            $('input').prop('disabled', false);
            $('textarea').prop('disabled', false);
            $("#status_error").show();
        }
    });

}
);