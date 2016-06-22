var id = 0;
var newRequest = 0;
setInterval(function(){
    var list_item =$('ul>li')[0];
    id = $(list_item).data('id');
    $.ajax({
        type: 'GET',
        url: '/request_list/',
        data: {id: id}
    }).success(function(responce){
        if (!responce.requests || !responce.requests.length) {
            return;
        }
            handlerMessages(responce.requests);
    });
}, 5000);

var handlerMessages = function(data){
    var requests = JSON.parse(data);
    newRequest += requests.length();
    document.title = newRequest + " new requests";
    $('h2').text(newRequest + " new requests");
    $.each(requests, function(i, item){
        var listItemString = "<li data-id='"+requests[i].id+"'>"+requests[i].method+" "+requests[i].path+" "+requests[i].status_code+" "+requests[i].server_protocol+" "+content_len+"</li>"
        $('ul').prepend(listItemString);
    });

};