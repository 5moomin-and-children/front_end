let score = 0; // 점수

function loadFile(waste) {
    let form = document.form;
    let formData = new FormData(form);

    let wasteFile = document.getElementById(waste);

    console.log(wasteFile)

    formData.append('waste', waste)
    formData.append('waste_img', wasteFile.files[0]);

    $.ajax({
        url: "/api/recycle_check",
        type: "POST",
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        data: formData,

        success: function (response) {
            wasteFile.value = '';

            if (response['result'] == 'true') {
                score++;
                alert('올바른 분리수거군,, 자네 상점을 주겠네')
            } else {
                score--;
                alert('분리수거도 못해? 사형이다.')
            }

        }
    });
}

function submit() {
    let webcam_score = localStorage.getItem("score");
    console.log(webcam_score)
    let total_score = Number(webcam_score) + score;
    $.ajax({
        url: "/api/submit",
        type: "POST",
        data: {
            score: total_score // 최종 점수 제출
        },
        success: function (response) {
            msg = '분리수거 종료 ( 분리수거 점수 : ' + total_score + ' )'
            alert(msg)
            window.location.href = '/result'
        }
    });
}

function popup(a) {
    let url = "/webcam?" + a;
    let name = "camera popup";
    let option = "width = 500, height = 500, top = 100,scrollbars = yes, left = 200, location = no";

    window.open(url, name, option);
}


let myVideoStream = document.getElementById('myVideo')     // make it a global variable
let myStoredInterval = 0

let temp = location.href.split('?');

let data = temp[1];


function getVideo() {
    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.getMedia({video: true, audio: false},

        function (stream) {
            myVideoStream.srcObject = stream
            myVideoStream.play();
        },

        function (error) {
            alert('카메라 안되니까 쓰지마!');
        });
}

function takeSnapshot() {
    let myCanvasElement = document.getElementById('myCanvas');
    let myCTX = myCanvasElement.getContext('2d');
    myCTX.drawImage(myVideoStream, 0, 0, myCanvasElement.width, myCanvasElement.height);
    let imgBase64 = myCanvasElement.toDataURL('image/jpeg', 'image/octet-stream');
    let decodImg = atob(imgBase64.split(',')[1]);

    let array = [];
    for (let i = 0; i < decodImg.length; i++) {
        array.push(decodImg.charCodeAt(i));
    }


    let wasteFile = new File([new Uint8Array(array)], 'image.jpg', {type: 'image/jpeg'});
    let waste = data
    let formData = new FormData();
    formData.append('waste', waste)
    formData.append('waste_img', wasteFile);

    $.ajax({
        url: "/api/recycle_check",
        type: "POST",
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        data: formData,

        success: function (response) {
            wasteFile.value = '';

            if (response['result'] == 'true') {

                score++;
                alert('올바른 분리수거군,, 자네 상점을 주겠네')
                localStorage.setItem("score", score);
                window.close()

            } else {
                score--;
                alert('분리수거도 못해? 사형이다.')
                localStorage.setItem("score", score);
                window.close()
            }

        }
    });
};

function popup_show1() {
    if ($("#popup1").css("display") == "block") {
        $("#popup1").hide();
    } else {
        $("#popup1").show();
    }
}
function popup_show2() {
    if ($("#popup2").css("display") == "block") {
        $("#popup2").hide();
    } else {
        $("#popup2").show();
    }
}
function popup_show3() {
    if ($("#popup3").css("display") == "block") {
        $("#popup3").hide();
    } else {
        $("#popup3").show();
    }
}
function popup_show4() {
    if ($("#popup4").css("display") == "block") {
        $("#popup4").hide();
    } else {
        $("#popup4").show();
    }
}
function popup_show5() {
    if ($("#popup5").css("display") == "block") {
        $("#popup5").hide();
    } else {
        $("#popup5").show();
    }
}
