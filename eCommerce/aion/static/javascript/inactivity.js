
var idleTime = 0;
$(document).ready(function () {
    //Increment the idle time counter every minute.
    var idleInterval = setInterval(timerIncrement, 60000); // 1 minute

    //Zero the idle timer on mouse movement.
    $(this).mousemove(function (e) {
        idleTime = 0;
    });
    $(this).keypress(function (e) {
        idleTime = 0;
    });
});

function timerIncrement() {
    idleTime = idleTime + 1;

    if (idleTime > 1) { // 20 minutes
        console.log("expired");
        window.location.reload();
        window.alert('Session expired!');
    }
    // if (idleTime == 1) {
    //     window.alert('Session will expire in 1min due to inactivity!');
    // }
}
