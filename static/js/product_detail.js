var updateBtns = document.getElementsByClassName('more-comment');

for (var i = 0; i < updateBtns.length; i++) {//for문을 돌리는 이유는 모든 updateBtns에게 기능을 추가하기 위함이다.
	updateBtns[i].addEventListener('click', function(e){ //클릭시 function 실행
        e.preventDefault();
        var trId = this.dataset.id;
        if (document.getElementById(trId).style.visibility == "collapse") {
            document.getElementById(trId).style.visibility = "visible";
        } else {
            document.getElementById(trId).style.visibility = "collapse"
        }


	})
}

function morecomment() {
    document.getElementById("moreComment2").style.visibility = "visible"

    //style display: none
    // element.style.visibility = show;
}

var updateBtns = document.getElementsByClassName('add-option');
for (var i = 0; i < updateBtns.length; i++) {//for문을 돌리는 이유는 모든 updateBtns에게 기능을 추가하기 위함이다.
	updateBtns[i].addEventListener('click', function(e){ //클릭시 function 실행
        e.preventDefault();
        // var trId = this.dataset.id;
        // if (document.getElementById(trId).style.visibility == "collapse") {
        //     document.getElementById(trId).style.visibility = "visible";
        // } else {
        //     document.getElementById(trId).style.visibility = "collapse"
        // }


	})
}