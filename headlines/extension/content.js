$( document ).ready(function() {
    console.log( "ready!" );
    $( "a.DY5T1d" ).each(function(index){
        $( this ).css( "border", "3px solid red" );
        let headline = $( this ).text();
        let thingy = this
        fetch("http://localhost:5000/extension/headline/simple?q="+headline)
        .then(response => response.json())
        .then(data => {
            
            jQuery.each(data["relationships"], function() {
                $( thingy ).after('<p style="border: 3px solid blue">'+this+'</p>')
              });
              jQuery.each(data["voice"], function() {
                $( thingy ).after('<p style="color: green">'+this+'</p>')
              });
        });
        

    })
});

$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        $( "a.DY5T1d" ).each(function(index){
            $( this ).css( "border", "3px solid red" );
            let headline = $( this ).text();
            let thingy = this
            fetch("http://localhost:5000/extension/headline/simple?q="+headline)
            .then(response => response.json())
            .then(data => {
                
                jQuery.each(data["relationships"], function() {
                    $( thingy ).after('<p style="border: 3px solid blue">'+this+'</p>')
                  });
                  jQuery.each(data["voice"], function() {
                    $( thingy ).after('<p style="color: green">'+this+'</p>')
                  });
            });
            
    
        })    
    }
});
