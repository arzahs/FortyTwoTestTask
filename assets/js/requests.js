var id = 0;
var newRequest = 0;
setInterval(function(){
    var list_item =$('ul>li')[0];
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
        var listItemString = "<li data-id='"+requests[i].pk+"'>"+requests[i].fields.method+" "+requests[i].fields.path+" "+requests[i].fields.status_code+" "+requests[i].fields.server_protocol+" "+requests[i].fields.content_len+"</li>"
        $('ul').prepend(listItemString);
        if($('ul li').length > 10){
            $('ul li:last-child').remove();
        }
    });

};
