 function paymentComplete(data) {
            url = "complete/" + data["response"]["merchant_uid"] + '/'

            fetch(url, {
                method: 'POST',
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data)
            }).then((response) => {
                window.location.replace(url)
            })
        }

        function requestPay(merchant_uid, name, amount, buyer_email, buyer_name, buyer_tel, buyer_addr, buyer_postcode) {
            var IMP = window.IMP; // 생략 가능
            IMP.init("imp55124420"); // 예: imp00000000l
            IMP.request_pay({ // param
                pg: "html5_inicis", //PG사
                pay_method: "card", //결제 수단
                merchant_uid: merchant_uid, //주문번호
                name: name,//상품명
                amount: amount, //가격
                buyer_email: buyer_email, //이메일
                buyer_name: buyer_name, //이름
                buyer_tel: buyer_tel, //전화번호
                buyer_addr: buyer_addr, //주소
                buyer_postcode: buyer_postcode //우편번호
            }, function (rsp) { // callback
                if (rsp.success) { //결제 성공식
                    jQuery.ajax({ //위변조 확인
                        headers: {

                            "X-CSRFToken": csrftoken,
                            "Content-Type": "application/json",
                        },
                        url: "complete/",
                        type: 'POST',
                        dataType: "json",
                        data: JSON.stringify({'imp_uid': rsp.imp_uid, 'merchant_uid': rsp.merchant_uid})
                    }).done(function (data) {
                        var info = JSON.parse(data)
                        if (info["response"]["status"] == "paid") {
                            alert("결제 성공");
                            paymentComplete(info)
                        } else if (info["response"]["status"] == "forgery") {
                            alert("자바 스크립트 위조");
                            location.reload();
                        } else {
                            alert(info["response"]["fail_reason"] + " 에러 지속시 고객센터에 문의 주세요");
                        }
                    });

                } else {
                    var msg = '결제에 실패하였습니다.';
                    msg += '에러내용 : ' + rsp.error_msg;
                }
            });
        }

        function submitFormData() {
            var data = {
                'orderer_name': null,
                'recipent_name': null,
                'email': null,
                'post_code': null,
                'recipent_address1': null,
                'recipent_address2': null,
                'recipent_number': null,
                'orderer_number': null,
                'order_request': null,
            }
            data.orderer_name = form.orderer_name.value
            data.recipent_name = form.recipent_name.value
            data.email = form.email.value
            data.post_code = form.post_code.value
            data.recipent_address1 = form.recipent_address1.value
            data.recipent_address2 = form.recipent_address2.value
            data.recipent_number = form.recipent_number.value
            data.orderer_number = form.orderer_number.value
            data.order_request = form.order_request.value
            var url = 'payment/';
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // {#"X-CSRFToken": token,#}
                    "X-CSRFToken": csrftoken,

                },
                body: JSON.stringify({'data': data})
            }).then((response) => response.json())
                .then((data) => {
                    obj = JSON.parse(data)

                    requestPay(obj['merchant_uid'], obj['name'], obj['amount'], obj['buyer_email'],
                        obj['buyer_name'], obj['buyer_tel'], obj['buyer_addr'], obj['post_code'])
                })
        }

        var token = '{{csrf_token}}';

        var form = document.getElementById('form')
        form.addEventListener('submit', function (e) { //결제 버튼 클릭시
            e.preventDefault()
            submitFormData();
        });