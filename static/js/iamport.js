var IMP = window.IMP; // 생략 가능
IMP.init("imp55124420"); // 예: imp00000000
function requestPay() {
    {
        IMP.request_pay({ // param
            pg: "html5_inicis", //PG사
            pay_method: "card", //결제 수단#}
            merchant_uid: merchant_uid, //주문번호#}
            name: name,//상품명#}
            amount: amount, //가격#}
            buyer_email: buyer_email, //이메일#}
            buyer_name: buyer_name, //이름#}
            buyer_tel: buyer_tel, //전화번호#}
            buyer_addr: buyer_addr, //주소#}
            // {#buyer_postcode: buyer_postcode //우편번호#}
            // pg: "html5_inicis", //PG사
            // pay_method: "card", //결제 수단
            // merchant_uid: "ORD20180131-030003455054311", //주문번호
            // name: "노르웨이 회전 의자",//상품명
            // amount: 100, //가격
            // buyer_email: "gildong@gmail.com", //이메일
            // buyer_name: "홍길동", //이름
            // buyer_tel: "010-4242-4242", //전화번호
            // buyer_addr: "서울특별시 강남구 신사동", //주소
            // buyer_postcode: "01181" //우편번호
        }, function (rsp) { // callback
            if (rsp.success) {
                console.log("성공")
                rsp.imp_uid // 아임포트 고유 결제 번호
                rsp.merchant_uid //주문번호
                rsp.pay_method //결제수단
                var msg = '결제가 완료되었습니다.';
                msg += '고유ID : ' + rsp.imp_uid;
                msg += '상점 거래ID : ' + rsp.merchant_uid;
                msg += '결제 금액 : ' + rsp.paid_amount;
                msg += '카드 승인번호 : ' + rsp.apply_num;
            } else {
                var msg = '결제에 실패하였습니다.';
                msg += '에러내용 : ' + rsp.error_msg;
            }
            alert(msg);
        });
    }
}