$(document).ready(function() {
    $(".increment-song-plays").on("playing", function(e){

        e.preventDefault();

        var post_id;
        var profile_id;
        post_id = $(this).attr("data-postid");
        profile_id = $(this).attr("data-profileid");

        $.ajax(
        {
            url: "/increment-song-plays/",
            type: "GET",
            data: {
                'post_id' : post_id
            },
            success: function()
            {
                $.ajax(
                {
                    url: "/increment-profile-plays/",
                    type: "GET",
                    data: {
                        'profile_id' : profile_id
                    },
                    success: function()
                    {
                        console.log("Success");
                    },
                    error: function() {
                        console.log("Failure: increment artist plays.");
                    }
                });
            },
            error: function() {
                console.log("Failure: increment song plays.");
            }
        });
    });

    $(".increment-song-downloads").click(function(e){

        var post_id;
        post_id = $(this).attr("data-postid");

        $.ajax(
        {
            url: "/increment-song-downloads/",
            type: "GET",
            data: {
                'post_id' : post_id
            },
            success: function()
            {
                console.log("Success");
            },
            error: function()
            {
                console.log("Failure: increment song downloads.");
            }
        });

    });
});