var t_id;
var Flask;
var user_color;
var temp_color;

$(document).ready(function(){

if (document.URL == "http://ide50-spongle.cs50.io:8080/"){
            //Passing retrieving user_color
                var parameters = {};
                $.getJSON(Flask.url_for("user"), parameters)
                .done(function(data, textStatus, jqXHR) {
                    user_color=data.color;
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    // log error to browser's console
                    console.log(errorThrown.toString());
                });
}

$(this).click(function(event)
    {
        t_id= event.target.id;
        if (!isNaN(t_id) || t_id) {
            var parameters = {
                    q: t_id
                };
                //Passing tile_id to ajax
                $.getJSON(Flask.url_for("update"), parameters)
                .done(function(data, textStatus, jqXHR) {
                    user_color=data.color;
                  $('#'+t_id).css("background-color");
                    $('#'+t_id).fadeOut(0).fadeIn(600);
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    // log error to browser's console
                    console.log(errorThrown.toString());
                });
        }
    });
});

function mouse_i(event) {
  var target = event.target;
  temp_color = target.style.background;
  target.style.background = user_color;
}

 function mouse_o(event) {
  var target = event.target;
  if (target.id != t_id){
        target.style.background = temp_color;
  }
}
