$(document).ready(function(){
    $("#submit_credits").prop('disabled', true);
    // Function to restrict input to between 1 and 100.
    $("#credits").on('input', function(){
        console.log($("#credits").val().length);
        if($("#credits").val().length > 3){
            $("#credits").val($("#credits").val().substring(0,3));
        }
        if ($("#credits").val() >= 1 && $("#credits").val() <= 100){
            $("#submit_credits").prop('disabled', false);
        }
        else{
            $("#submit_credits").prop('disabled', true);
        }
    });
});