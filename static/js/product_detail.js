var updateBtns = document.getElementsByClassName('more-comment');
console.log(updateBtns)

for (var i = 0; i < updateBtns.length; i++) {//for문을 돌리는 이유는 모든 updateBtns에게 기능을 추가하기 위함이다.
    console.log("updateBtns")
	updateBtns[i].addEventListener('click', function(e){ //클릭시 function 실행
        e.preventDefault();
        console.log('product detail clicked')

	})
}

function morecomment() {
    document.getElementById("moreComment2").style.visibility = "visible"
    console.log('morecomment2')

    //style display: none
    // element.style.visibility = show;
}