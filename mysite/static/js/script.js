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
    $("<div/>",{text:data.title,id:String(m_id),class:cls,style:'flex:'+data.ratio+';background-color:'+getRandomColor()}).appendTo(String(p_id));
    if (data.children.length > 0) {
        for (var i = 0; i < data.children.length; i ++){
            make_div(data.children[i],"#"+String(m_id))
    }}
};

$(document).ready(function(){
    var payload = new Object()
    payload.width = $(document).width()
    payload.height = $(document).height()

    $.get("get_data/",payload,function(data,status){
        make_div(data,".wrapper")
    });
});
