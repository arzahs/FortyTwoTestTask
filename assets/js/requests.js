var id = 0;
var newRequest = 0;
var type_sort = '';
var order_load = 1;
var inputPriority = false;
var lastPriority = 0;

function sortTable($table, order){
    if(order !== ''){
        var $rows = $('tbody tr').get();
        $rows.sort(function (a, b) {
            var keyA = parseInt($('.prior-text', a).eq(0).text());
            var keyB = parseInt($('.prior-text', b).eq(0).text());
            if (order == "asc") {
                return (keyA > keyB) ? 1 : 0;
            } else {
                return (keyA > keyB) ? 0 : 1;
            }
        });
        $.each($rows, function (index, row) {
            $table.append(row);
        });
    }


}

setInterval(function(){
    var maxId = 0
    $('tbody tr').each(function() {

        if(maxId < $(this).data("id")){ maxId = $(this).data("id")}

    });
    var id = maxId;
    $.ajax({
        type: 'GET',
        url: location.href,
        data: {id: id, priority: type_sort},
        dataType: 'json'
    }).success(function(response){
        if (!response || !response.length) {
            return false;
        }
        var table_len = $('tbody tr').length;
        if((type_sort == '' || (type_sort !== '' && table_len < 10) || order_load < 1) && inputPriority === false){
            handlerMessages(response);
            if(type_sort !== ''){
                order_load++;
            }

        }
        $('.alert').hide();
        $('.alert').text('');



    });
}, 3000);

var handlerMessages = function(data){
    var requests = jQuery.parseJSON(JSON.stringify(data));
    if(type_sort !== ''){
        var len = $('tbody tr').length;
        if(len < requests.length){
            var count = requests.length - len;
            newRequest += count;
            document.title = newRequest + " new requests";
            $('h2').text(newRequest + " new requests");
        }
        $('tbody tr').remove();
    }

    if(type_sort === ''){
        newRequest += requests.length;
        document.title = newRequest + " new requests";
        $('h2').text(newRequest + " new requests");
    }
    $.each(requests, function(i, item){
        var listItemString = "<tr data-id='"+requests[i].pk+"'><td>"+requests[i].fields.method+"</td><td>"+requests[i].fields.path+"</td><td>"+requests[i].fields.status_code+"</td><td>"+requests[i].fields.server_protocol+"</td><td>"+requests[i].fields.content_len+"</td>"+ "<td><input class='priority' type='text' value='"+requests[i].fields.priority+"'><span class='prior-text'>"+requests[i].fields.priority+"</span></td>"+"</tr>";
        $('table').prepend(listItemString);
        if($('tbody tr').length > 10){
            $('tbody tr:last-child').remove();
        }
    });
    sortTable($('table'), type_sort);
};


$(document).ready(function () {
    $('body').on('click', 'tr td:last-child', function(event) {
        $('tr td:last-child').each(function(item, i){
            var elm = $(i).children('.priority');

            if ($(event.target).closest($(this)).length === 0 && $(elm).css('display') === 'inline-block'){
                sendPriority(elm);
            }
        });
       var $text = $(this).children('span');
        var priority = parseInt($text.text());
        $text.hide();
        $(this).children('input').val(priority).show();
        inputPriority = true;
        lastPriority = priority;
    });

    $('#sort').on('change', function () {
        type_sort = $(this).val();
        order_load = 0;
        $('.alert').show();
        $('.alert').text('Sorting...Wait one second!');
        if(type_sort == ''){
            location.reload(true);
        }
    });

    $('body').on('keyup', '.priority', function(event) {
        $(this).val($(this).val().replace(/[^+0-9]/gim,''));
        if(event.which == 13){
            sendPriority(this);
        }
    });

    $('body').on('focusout', '.priority', function(event) {
            event.preventDefault();
            sendPriority(this);
    });

});

function sendPriority(elm) {
    var value = parseInt($(elm).val());
        if(isNaN(value)){
                value = lastPriority;
            }

                $(elm).hide();
                $(elm).parent().children('span').text(value).show();
                var tr = $(elm).closest('tr');
                var id = $(tr).data('id');
                var csrf = $('#csrf').val();
                sortTable($(elm).closest('table'), type_sort);
                order_load = 0;
                inputPriority = false;
                if(type_sort !== ''){
                    $('.alert').show();
                    $('.alert').text('Sorting...Wait one second!');
                }
                $.ajax({
                    type: 'POST',
                    url: location.href,
                    data: {id: id, priority: value, csrfmiddlewaretoken: csrf},
                    dataType: 'json'
                }).success(function(response){
                    if (!response || !response.length) {
                        return false;
                    }
                });

}

