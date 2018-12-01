// Open the side nav bar on click.
// Max width of 250px
function openNav() {
    document.getElementById("nav").style.width = "250px";
}

// Close the side nav bar on click
function closeNav() {
    document.getElementById("nav").style.width = "0";
}

// Youtube video embed code borrowed from:
// https://sarmadgardezi.com/blog/youtube/how-to-embed-youtube-video-as-an-audio-player-in-website/1000/
// Note: code has been modified to fit our needs
function onYouTubeIframeAPIReady(){
    var e=document.getElementById("youtube-audio"),
    t=document.createElement("img");t.setAttribute("id","youtube-icon"),
    t.style.cssText="cursor:pointer;cursor:hand",
    e.appendChild(t);

    var a=document.createElement("div");
    a.setAttribute("id","youtube-player"),
    e.appendChild(a);
    // 1st png is a play icon, 2nd is a stop icon
    // pictures hosted using imgur
    // var o=function(e){var a=e?"IDzX9gL.png":"quyUPXN.png";
    // t.setAttribute("src","https://i.imgur.com/"+a)};
    var o=function(e){var a=e?"../api-project/images/play.png":"../api-project/images/pause.png";
    t.setAttribute("src", a)};
    e.onclick=function(){r.getPlayerState()===YT.PlayerState.PLAYING||
        r.getPlayerState()===YT.PlayerState.BUFFERING?(
            r.pauseVideo(),o(!1)):
        (r.playVideo(),o(!0))};var r=new YT.Player("youtube-player",
        {height:"0",width:"0",videoId:e.dataset.video,playerVars:
        {autoplay:e.dataset.autoplay,loop:e.dataset.loop},events:
        {onReady:function(e){r.setPlaybackQuality("small"),
        o(r.getPlayerState()!==YT.PlayerState.CUED)},
        onStateChange:function(e){e.data===YT.PlayerState.ENDED&&o(!1)}}})
    }

// jQuery: select form from 1 to 31 days of the month
function selectDay() {
    var select = '';
    for (num = 1; num <= 31; num++) {
        select += '<option val=' + num + '>' + num + '</option>';
    }
    $('#day').html(select);
}

// validate birthday for horoscope
function validateForm(form) {
    var month = form['month'].value;
    var day = form['day'].value;
    var days30 = [4, 6, 9, 11];
    var bool = false;
    if (month == 2 && day > 29) {
        alert("Oops! The date you entered is invalid, please try again.")
    } else if (!days30.includes(month) && day > 30) {
        alert("Oops! The month you entered only has 30 days, please try again.")
    } else {
        bool = true;
    }
    return bool;
}