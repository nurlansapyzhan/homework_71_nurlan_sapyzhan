$(document).ready(function () {
    $('.like_button').click(function (event) {
        event.preventDefault();
        let post = $(this).data('post');
        let url = "post/" + post + "/like";
        let like_button = $(this);
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                let like_count = parseInt(document.getElementById("like_count").textContent.split(" ")[0]);
                let liked = document.getElementsByClassName("liked")
                console.log(liked)
                if (liked.length > 0) {
                    like_count = like_count - 1
                    like_button.removeClass('liked')
                }
                else {
                    like_count = like_count + 1
                    like_button.addClass('liked')
                }
                let like_count_element = like_button.siblings('#like_count');
                like_count_element.text(like_count + " Отметок \"Нравится\"");
            }
            ,
            error: function (xhr, status, error) {
                console.log("Error:", error);
            }
        });
    });
});