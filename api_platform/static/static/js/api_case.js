    // 新建用例验证
$(function() {
    $("button#add_case_sub").click(function () {

        $.ajax({
            url: "/add_case/",
            type: "post",
            data: {
                case_name: $("#case_name").val(),
                modules_id: $("#modules_id").val(),
                project_id: $("#project_id").val(),
                api: $("#api").val(),
                version: $("#version").val(),
                case_desc: $("#case_desc").val(),
                status: $("*[name='status']:checked").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {

                if (data.status == 0) {
                    // alert(111)
                    toastr.success(data.msg);
                    if (location.search) {
                        location.href = location.search.slice(6)
                    } else {
                        setTimeout(function () {
                            location.href = "/api_case/"
                        }, 2000)

                    }

                } else {


                    $(".error").text(data.msg);
                    setTimeout(function () {
                        $(".error").text("");

                    }, 5000)
                }


            }

        })
    })
});