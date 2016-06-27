$(document).ready(function () {
    var photo = '';
    $("#status_save").hide();
    $("#status_error").hide();
    $('#error_list').hide();
    
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
            photo = data['photo'];
            $("#photo").attr('src', data['photo']);
            $("#photo").show();
            $("#status_load").hide();
        }
    });

    $(function() {
        $( "#id_birthday" ).datepicker({ dateFormat: 'yy-mm-dd', maxDate: -1});
    });
    
    
    $("#id_photo").change(function () {
        if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#photo").show().attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
            $('#cancel_load').show();
    }
    });

    $('#cancel_load').click(function (event) {
        event.preventDefault();
        $("#id_photo").val('');
        $("#photo").attr('src', photo);
        $('#cancel_load').hide();
    });


    $("#edit_form").ajaxForm({
        beforeSubmit: function () {
            $("#status_error").hide();
            $('#error_list').hide();
            $("#status_save").show();
            $('input').prop('disabled', true);
            $('textarea').prop('disabled', true);

        },
        success: function (data) {
            if(data['result'] == 'error'){
                console.log(data['errors']);
            }
            $("#status_save").hide();
            $("#status_success").show();
          setTimeout(function(){
              location.reload()
          }, 5000);

        },
        error: function (data) {
            $('#error_list').text('');
            $.each(JSON.parse(data.responseText)['errors'], function (i, item) {
                $('#error_list').text($('#error_list').text()+item[0]+' ');
            });
            $("#status_error").text();
            $("#status_save").hide();
            $('input').prop('disabled', false);
            $('textarea').prop('disabled', false);
            $("#status_error").show();
            $('#error_list').show();
        }
    });

}
);