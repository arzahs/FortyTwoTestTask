var id = 0;
var newRequest = 0;
var type_sort = '';

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
        url: '/requests_list',
        data: {id: id},
        dataType: 'json'
    }).success(function(response){
        if (!response || !response.length) {
            return false;
        }
        handlerMessages(response);



    });
}, 5000);

var handlerMessages = function(data){
    var requests = jQuery.parseJSON(JSON.stringify(data));
    newRequest += requests.length;
    document.title = newRequest + " new requests";
    $('h2').text(newRequest + " new requests");
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
       var $text = $(this).children('span');
        var priority = parseInt($text.text());
        $text.hide();
        $(this).children('input').val(priority).show();
        });
    
    $('#sort').on('change', function () {
        type_sort = $(this).val();
        sortTable($('table'), type_sort);
    });
    
    $('body').on('keyup', '.priority', function(event) {
        $(this).val($(this).val().replace(/[^+0-9]/gim,''));
        if(event.which == 13){
            var value = parseInt($(this).val());
            if(isNaN(value)){
                alert('Input error!');
            }else{
                $(this).hide();
                $(this).parent().children('span').text(value).show();
                var tr = $(this).closest('tr');
                var id = $(tr).data('id');
                var csrf = $('#csrf').val();
                sortTable($(this).closest('table'), type_sort);
                $.ajax({
                    type: 'POST',
                    url: '/requests_list/',
                    data: {id: id, priority: value, csrfmiddlewaretoken: csrf},
                    dataType: 'json'
                }).success(function(response){
                    if (!response || !response.length) {
                        return false;
                    }
                });

            }


        }
    });
});

