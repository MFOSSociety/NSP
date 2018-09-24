$(".messages").animate({ scrollTop: $(document).height() }, "fast");
function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}

var sender = document.getElementById("sender_username").value;
var sender_id = document.getElementById("sender_id").value;
var sender_user_profile_photo_url = document.getElementById("sender_user_profile_photo_url").value; 
var receiver_user_profile_photo_url = document.getElementById("receiver_user_profile_photo_url").value; 
var receiver = document.getElementById("receiver_username").value;
var receiver_id = document.getElementById("receiver_id").value;
var messages_len = 0;
var messages_div = document.getElementById("messages");

function clear() {
	var messages_div = document.getElementById("messages");
	messages_div.innerHTML = "";
}
function show(json) {
	var ul = document.createElement("ul")
	for (var key in json) {
		if (json[key]["fields"].sender == sender_id) {
			console.log(1);
			li = document.createElement("li");
			li.setAttribute("class","sent");
			img = document.createElement("img");
			img.src = sender_user_profile_photo_url;
		} else {
			li = document.createElement("li");
			li.setAttribute("class","replies");
			img = document.createElement("img");
			img.src = receiver_user_profile_photo_url;		
		}
		p = document.createElement("p")
		p.innerHTML = json[key]["fields"]["msg_content"];
		li.appendChild(img);
		li.appendChild(p);
		ul.appendChild(li);
	}
	messages_div.appendChild(ul);
}

function update() {
	var csrftoken = getCookie('csrftoken');
	$.ajax({
		method: "POST",
		data: {"csrfmiddlewaretoken":csrftoken},
		url: `/account/chat/get_messages_api/${receiver}`,
	}).done(function (json){
		console.log(json);
		if (messages_len < json.length){
			clear();
			show(json);
		}
		messages_len = json.length
	})
window.setTimeout(update,500);
}
update();
