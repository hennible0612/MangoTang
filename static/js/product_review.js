$(".page-link").click(function () {
    var page = this.dataset.page;
    $.ajax({
        url: '/product/review/{{ product.seller_code }}/' + page + '/',
        type: 'GET'
    }).done(function (data) {
        nextReview(data, page)
    }).fail(function () {
        console.log("실패")
    })
});

function nextReview(data, page) {


    $.each(jQuery.parseJSON(data), function (id, data) {

        console.log(data)
        console.log(data)
        console.log("product : ", data.fields.product)
        console.log("customer : ", data.fields.customer)
        console.log("date_added : ", data.fields.date_added)
        console.log("long_review : ", data.fields.long_review)
        console.log("review_bool : ", data.fields.review_bool)
        console.log("short_review : ", data.fields.short_review)
        console.log("star_rating : ", data.fields.star_rating)
        console.log("-" * 100)


    });

}
