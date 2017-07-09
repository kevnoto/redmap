function uniqID(idlength) {
            var charstoformid = '_0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz'.split('');
            if (! idlength) {
                idlength = Math.floor(Math.random() * charstoformid.length);
            }
            var uniqid = '';
            for (var i = 0; i < idlength; i++) {
                uniqid += charstoformid[Math.floor(Math.random() * charstoformid.length)];
            }
            // one last step is to check if this ID is already taken by an element before
            if(jQuery("#"+uniqid).length == 0)
                return uniqid;
            else
                return uniqID(20)
        };

var rtime;
var timeout = false;
var delta = 200;
$(window).resize(function() {
    rtime = new Date();
    if (timeout === false) {
        timeout = true;
        setTimeout(resizeend, delta);
    }
});

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function make_div(data,p_id) {
    var m_id = uniqID(20);
    var cls
    if (data.split_type == "vertical") {
        cls = 'row'
    } else {
        cls = 'col'
    }
    if (p_id == ".wrapper") {
        cls += ' table'
    } else if (data.children.length ==0) {
        cls += ' cell'
    }
    $("<div/>",{text:data.title,id:String(m_id),class:cls,style:'flex:'+data.ratio+';background-color:'+data.color+';font-size:'+String(data.font_size)+';'}).appendTo(String(p_id));
    if (data.children.length > 0) {
        for (var i = 0; i < data.children.length; i ++){
            make_div(data.children[i],"#"+String(m_id))
    }} else {
        $("#"+String(m_id)).wrap($("<a href=\""+data.url+"\">"+"</a>"))
    }
};

function render(){
    $(".wrapper").empty();
    var payload = new Object()
    payload.width = $(document).width()
    payload.height = $(document).height()
    payload.reddits = ["all","funny"]
    $.get("get_data/",payload,function(data,status){
        make_div(data,".wrapper")
    });
};

function resizeend() {
    if (new Date() - rtime < delta) {
        setTimeout(resizeend, delta);
    } else {
        timeout = false;
        render();
        shape_data();
    }
};

var reddit_data

function get_data(callback){
    var payload = new Object()
    payload.reddits = ["all","funny"]
    $.get("get_sr_data/",payload,function(data,status){
        reddit_data = data;
        callback();
    });
};

function shape_data(){
    console.log("This is shape data");
    console.log(reddit_data);
};

$(document).ready(function(){
    get_data(shape_data);
    render();
});

$("div").on_clock
