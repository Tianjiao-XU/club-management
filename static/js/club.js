//click on img, fadeout slow
$(document).ready(function () {
    $("img").click(function () {
        $("#div1").fadeOut("slow");
    });
});
//click on img, fadeout slow
$(document).ready(function () {
    $("img").click(function () {
        $("#div2").fadeOut("slow");
    });
});
//click on img, fadeout slow
$(document).ready(function () {
    $("img").click(function () {
        $("#div3").fadeOut("slow");
    });
});
//data now
function showDate() {
  let now = new Date();
  let date = now.toLocaleDateString();
  document.getElementById('date').innerHTML = date;
}
//time now
function showTime() {
  let now = new Date();
  let time = now.toLocaleTimeString();
  document.getElementById('time').innerHTML = time;
}

//refresh every second
setInterval(showDate, 1000);
setInterval(showTime, 1000);