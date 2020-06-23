const GOOGLE_NEWS_HEADLINE_SELECTOR = "a.DY5T1d"
const HEADLINES_SERVER_REQUEST_URL = "http://localhost:5000/extension/headline/simple?q="
const ENTER_BUTTON_KEY_CODE = 13

let annotate_headlines = function() {
    $( GOOGLE_NEWS_HEADLINE_SELECTOR ).each(function(index){
        
        //Draw red box arround actual headline
        $( this ).css( "border", "3px solid red" );
        
        //get text of headline
        let headline_text = $( this ).text();
        
        //save headline selector object so we can append annotations to it later
        let original_headline_object = this
        
        //grap annotations from headlines backend
        fetch(HEADLINES_SERVER_REQUEST_URL + headline_text)
        .then(response => response.json())
        .then(data => {
        
            //for each relationship the openie notices (called 'relationships' in the backend, add a blue highlighted paragraph)
            $.each(data["relationships"], function() {
                $( original_headline_object ).after('<p style="border: 3px solid blue">'+this+'</p>')
            });

            //for each instance of passive or activate voice the depparse notices (called 'voice' in the backend, add a green highlighted paragraph)
            $.each(data["voice"], function() {
                $( original_headline_object ).after('<p style="color: green">'+this+'</p>')
            });
        });
        

    })
}

//when the page loads annotate every headline on screen
$( document ).ready(annotate_headlines);

//when the enter key is pressed, annotate current visble headlines
$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == ENTER_BUTTON_KEY_CODE){
        annotate_headlines()
    }
});
