var id = 0;
var newRequest = 0;
setInterval(function(){
    var list_item =$('table tr')[0];
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
        var listItemString = "<tr data-id='"+requests[i].pk+"'><td>"+requests[i].fields.method+" "+requests[i].fields.path+" "+requests[i].fields.status_code+" "+requests[i].fields.server_protocol+" "+requests[i].fields.content_len+"</td>"+ "<td>priority:<input class='priority' type='text' value='"+requests[i].fields.priority+"'></td>"+"</tr>";
        $('table').prepend(listItemString);
        if($('table tr').length > 10){
            $('table tr:last-child').remove();
        }
    });

};


