//전화번호 정수만 입력했는지 확인
function maxLengthCheck(object) {
    object.value = object.value.replace(/[^0-9]/gi, '');
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength)
    }
}

//다음(카카오) 주소 api
$('.address_kakao').click(function () {
    new daum.Postcode({
        oncomplete: function (data) { //선택시 입력값 세팅
            document.getElementById("address_kakao").value = data.address; // 주소 넣기
            document.getElementById("post_kakao").value = data.zonecode; // 우편 번호 넣기
            document.querySelector("input[name=recipent_address2]").focus(); //상세입력 포커싱
        }
    }).open();
});