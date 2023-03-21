$(document).ready(function () {
    $("img").click(function () {
        $("#div1").fadeOut("slow");
    });
});

$(document).ready(function () {
    $("img").click(function () {
        $("#div2").fadeOut("slow");
    });
});

$(document).ready(function () {
    $("img").click(function () {
        $("#div3").fadeOut("slow");
    });
});

function showDate() {
  let now = new Date();
  let date = now.toLocaleDateString();
  document.getElementById('date').innerHTML = date;
}

function showTime() {
  let now = new Date();
  let time = now.toLocaleTimeString();
  document.getElementById('time').innerHTML = time;
}

//refresh every second
setInterval(showDate, 1000);
setInterval(showTime, 1000);