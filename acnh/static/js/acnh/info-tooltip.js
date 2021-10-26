$(document).ready(function(){
    $("div.graphic-box").hover(function(){
        // On mouseenter, get information on that entry and show tooltip.
        var tooltip = $(this).find("span.critter-tooltip");
        var image = $(this).find("img.critter");
        // Pull critter info from the database and place it in the associated tooltip span.
        tooltip.load("./critter_info/", {
            csrfmiddlewaretoken : $("input[name='csrfmiddlewaretoken']").val(), 
            name : image.attr('alt'),
            hemisphere : $("#hemisphere").val()
        });
        tooltip.show();
    }, function(){
        // On mouseleave, clear information and hide tooltip.
        var tooltip = $(this).find("span.critter-tooltip");
        tooltip.html("");
        tooltip.hide();
    });
});