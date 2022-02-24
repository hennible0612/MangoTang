var IMP = window.IMP; // 생략 가능
IMP.init("imp55124420"); // 예: imp00000000
function requestPay() {
    {
        //IMP.request_pay(param, callback) //결제창 호출#}
        IMP.request_pay({ // param
            pg: "html5_inicis", //PG사
            pay_method: "card", //결제 수단
            merchant_uid: "2334534534", //주문번호
            name: "노르웨이 회전 의자",//상품명
            amount: 100, //가격
            buyer_email: "gildong@gmail.com", //이메일
            buyer_name: "홍길동", //이름
            buyer_tel: "010-4242-4242", //전화번호
            buyer_addr: "서울특별시 강남구 신사동", //주소
            buyer_postcode: "01181" //우편번호
        }, function (rsp) { // callback
            if (rsp.success) {
                console.log("성공");
                console.log(rsp.imp_uid,);
                console.log(rsp.merchant_uid);
                $.ajax({
                    url: "/checkout/complete",
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    data: {
                        imp_uid: rsp.imp_uid,
                        merchant_uid: rsp.merchant_uid
                    }
                })

            } else {
                var msg = '결제에 실패하였습니다.';
                msg += '에러내용 : ' + rsp.error_msg;
            }
            alert(msg);
        });
    }
}

function getToken() {
    $.ajax({
        url: "https://api.iamport.kr/users/getToken",
        method: "POST",
        headers: {"Content-Type": "application/json"},
        data: {
            imp_key: "5711640649645563",
            imp_secret: "gnHzb19tGKkTetldbEl0IaQR8CsirIoH55gh7qLNa5Hpz2CKGXKo8AghcJzErXlx3CPa2AXcGECfHfZn"
        }
    });
}