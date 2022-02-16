// var updateBtns = document.getElementsByClassName('update-cart');
//
// for (i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function () { //클릭시 function 실행
//         var sellerCode = this.dataset.product;//커스텀 attribute를 통해 데이터를 가져옴 즉, store.html에 있는 product.id가져옴
//         var action = this.dataset.action;// add가져옴 this는 클릭이 된애
//
//         if (user == 'AnonymousUser') {
//             console.log('User is not authenticated');
//         } else {
//             updateUserOrder(sellerCode, action);
//         }
//     });
// }


// $('.update-cart').click(function (e) {
//     var sellerCode = $(this).data("product");
//     var action = $(this).data("action");// add가져옴 this는 클릭이 된애
//     var productQuantity = 1
//     $.ajax({
//         headers: {"X-CSRFToken": csrftoken},
//         url: '/update_item/',
//         type: 'POST',
//         dataType: "json",
//         data: JSON.stringify({'sellerCode': sellerCode, 'action': action, 'quantity': productQuantity,'option':'false'})
//     }).done(function () {
//     }).fail(function () {
//     })
// });


function updateUserOrder(sellerCode, action) {
    console.log('User is authenticated')

    var url = '/update_item/'  //POST request 보낼 view url

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'sellerCode': sellerCode, 'action': action})
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

// $.ajax({
//     url: '/productDetail/get_review/1004/1',
//     type: 'GET'
// }).done(function (data) {
//     console.log(data)
//     console.log("성공")
// }).fail(function () {
//     console.log("실패")
// })