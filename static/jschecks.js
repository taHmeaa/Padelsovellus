function check(form) {
    var checked = 0;
    var chks = document.getElementsByTagName("input");
    for (var i = 0; i < chks.length; i++) {
        if (chks[i].checked) {
            checked++;
        }
    }
    if (checked > 3) {
        return true;
    }   
    else {
        alert("Valitse vähintään 4 pelaajaa");
        return false;
    }
}


function checkplayer(form) {
    if (4 < form.player.value.length < 9) {
        return true
    }
    
    else {
        alert("Nimen pituus pitää olla 4-10 kirjainta");
        return false;
    }
}