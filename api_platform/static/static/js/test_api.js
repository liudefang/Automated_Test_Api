  // 新建用例验证

function add_case_sub() {
    var paras = getParaTable();

    $.ajax({
        url: "/add_api_case/",
        type: "post",
        data: {
            case_name: $("#case_name").val(),
            modules_id: $("#modules_id").val(),
            project_id: $("#project_id").val(),
            api: $("#api").val(),
            paras: paras,
            case_desc: $("#case_desc").val(),
            status: $("*[name='status']:checked").val(),
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
        },
        success: function (data) {

            if (data.status== 0) {
                // alert(111)
                toastr.success(data.msg);
                if (location.search){
                        location.href = location.search.slice(6)
                }
                else {
                    setTimeout(function () {
                        location.href = "/api_case/"
                    }, 2000)

                }

            }
            else {


                $(".error").text(data.msg);
                setTimeout(function () {
                    $(".error").text("");

                }, 5000)
            }



        }

    })
};

function getParaTable(){
    var tbodies= $("#para_table");
    var para_name_list = document.getElementsByClassName('para_name');
    var para_value_list = document.getElementsByClassName('para_value');
    var isParamized_list = document.getElementsByClassName('isParamized');
    var paramized_value_list = document.getElementsByClassName('paramized_value');

    var paras = {};
    for (var i=0;i< para_name_list.length;i++){
        console.log(para_name_list[i].text+para_value_list[i].text+isParamized_list[i].checked+paramized_value_list[i].value);
        if (isParamized_list[i].checked){
            paras[para_name_list[i].text]=paramized_value_list[i].value;
        }else{
            paras[para_name_list[i].text]=para_value_list[i].text;
        }
    }
    console.log(paras);
    var jsonString = JSON.stringify(paras);
        console.log(jsonString);
    return jsonString;
}