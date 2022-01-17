$(document).ready(function () {
    show_ranking();
});

function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href = '/login'
}

// 랭킹 보여주는 함수
function show_ranking() {
    $.ajax({
        type: 'GET',
        url: '/api/result',
        data: {},
        success: function (response) {
            let rows = response['ranking']
            rows.sort(function (a,b){
                return b.score - a.score
            });


            // 1등 아이디, 점수
            let first_id = rows[0]['id'];
            let first_score = rows[0]['score'];
            let temp_html1 = `<h3>1등</h3>
                            <h4>${first_id}</h4>
                            <h6>${first_score}점</h6>`
                $('#first').append(temp_html1)

            // 2등 아이디, 점수
            let second_id = rows[1]['id'];
            let second_score = rows[1]['score'];
            let temp_html2 = `<h3>2등</h3>
                            <h4>${second_id}</h4>
                            <h6>${second_score}점</h6>`
                $('#second').append(temp_html2)

            // 3등 아이디, 점수
            let third_id = rows[2]['id'];
            let third_score = rows[2]['score'];
            let temp_html3 = `<h3>3등</h3>
                            <h4>${third_id}</h4>
                            <h6>${third_score}점</h6>`
                $('#third').append(temp_html3)


            for (let i = 3; i < 6; i++) {
                let id = rows[i]['id'];
                let score = rows[i]['score'];
                let temp_html = `<tr>
                                    <td>${id}</td>
                                    <td>${score}점</td>
                                </tr>`
                $('#rank').append(temp_html)
            }

        }

    });
}
