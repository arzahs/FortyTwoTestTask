var id = 0;
var newRequest = 0;
setInterval(function(){
    var list_item =$('tbody tr')[0];
    id = $(list_item).data('id');
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
        var listItemString = "<tr data-id='"+requests[i].pk+"'><td>"+requests[i].fields.method+"</td><td>"+requests[i].fields.path+"</td><td>"+requests[i].fields.status_code+"</td><td>"+requests[i].fields.server_protocol+"</td><td>"+requests[i].fields.content_len+"</td>"+ "<td><input class='priority' type='text' value='1'><span class='pior-text'> 1 </span></td>"+"</tr>";
        $('table').prepend(listItemString);
        if($('tbody tr').length > 10){
            $('tbody tr:last-child').remove();
        }
    });

};


$(document).ready(function () {
    $('body').on('click', 'tr td:last-child', function(event) {
       var $text = $(this).children('span');
        var priority = $text.text();
        $text.hide();
        $(this).children('input').val(priority).show();
        });

    $('body').on('keyup', '.priority', function(event) {
        if(event.which == 13){
            var value = $(this).val();
            $(this).hide();
            console.log(value);
            console.log($(this).parent().children('span').text());
            $(this).parent().children('span').text(value).show();
        }
    });
});

