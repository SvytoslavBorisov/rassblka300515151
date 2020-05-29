$('#input_type_message_text').change(function(){
            $('#input_text_message').val(' ');
        });
        $('#input_type_message_html').change(function(){
            $('#input_text_message').val(`<!DOCTYPE html>
<html lang="en">
    <head>

    </head>
    <body>
        ` + $('#input_text_message').val() + `
    </body>
</html>`)});