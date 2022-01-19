var updateBtns = document.getElementsByClassName('update-cart');

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () { //클릭시 function 실행
        var productId = this.dataset.product;//커스텀 attribute를 통해 데이터를 가져옴 즉, store.html에 있는 product.id가져옴
        var action = this.dataset.action;// add가져옴 this는 클릭이 된애
        console.log('productId:', productId, 'Action:', action);

        console.log('USER:', user);
        if (user == 'AnonymousUser') {
            console.log('User is not authenticated');
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated')

    var url = '/update_item/'  //POST request 보낼 view url

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            location.reload()
        });
}


// $.ajax({
//     url: 'http://127.0.0.1:8000/productDetail/12312/?page=3',
//     type: 'GET'
// }).done(function (data) {
//     console.log(data)
//     console.log("성공")
// }).fail(function () {
//     console.log("실패")
// })
// //
