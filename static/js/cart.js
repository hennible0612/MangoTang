$('.update-cart').click(function (e) {
    var sellerCode = $(this).data("product");
    var action = $(this).data("action");// add가져옴 this는 클릭이 된애
    var productQuantity = 1
    $.ajax({
        headers: {"X-CSRFToken": csrftoken},
        url: '/update_item/',
        type: 'POST',
        dataType: "json",
        data: JSON.stringify({'sellerCode': sellerCode, 'action': action, 'quantity': productQuantity,'option':'false'})
    }).done(function (data) {
        if (data == 'false') {
            alert("로그인을 해주세요")
            window.location.replace('/login/')
        } 
    }).fail(function () {
    })
});


// function updateUserOrder(sellerCode, action) {
//     console.log('User is authenticated')
//
//     var url = '/update_item/'  //POST request 보낼 view url
//
//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({'sellerCode': sellerCode, 'action': action})
//     })
//         .then((response) => {
//             return response.json()
//         })
//         .then((data) => {
//             location.reload()
//         });
// }

