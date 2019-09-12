$(function() {
    // 新建项目验证

    $(".btn_sub").click(function () {

        $.ajax({
            url: "/add_project/",
            type: "post",
            data: {
                prj_name: $("#prj_name").val(),
                type: $("*[name='type']:checked").val(),
                prj_desc: $("#prj_desc").val(),
                testers: $("#testers").val(),
                developer: $("#developer").val(),
                version: $("#version").val(),
                status: $("*[name='status']:checked").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                console.log(data);


                if (data.status == 0) {
                    // alert(111)
                    toastr.success(data.msg);
                    if (location.search) {
                        location.href = location.search.slice(6)
                    } else {
                        setTimeout(function () {
                            location.href = "/project/"
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
    });

    //编辑项目
    $("#edit_prj").click(function(){

                var count=0;
                var env_value;
                var env=new Array();
                var elements=$(".ipt");
                var url = null;
                $("#table").find(":checkbox:checked").each(function(){
                    env_value=$(this).parent()
                    for (var i=0;i<elements.length;i++){
                        env_value=env_value.next()

                        env[i]=env_value.text();


                    }
                    count++;
                });
                alert(count)
                if (count==1)
                {
                    alert(env);

                    for (var i=0;i<env.length;i++){
                        $(elements[i]).val(env[i]);
                    }

                    $('#editMyModal').modal("show");
                    if(env>0){
                        location.href = url;
                    }
                }
                else if(count==0){
                    toastr.error("请至少选择一个选项!")
                }
                else{
                    toastr.error("编辑只能选择一个选项!");
                }
            });

        //编辑提交信息
        $(".edit_prj_sub").click(function () {

                $.ajax({
                    url: "/edit_project/",
                    type: "post",
                    data: {
                        prj_id: $("#id").val(),
                        prj_name: $("#edit_prj_name").val(),
                        type: $("*[name='type']:checked").val(),
                        testers: $("#edit_testers").val(),
                        developer: $("#edit_developer").val(),
                        prj_desc: $("#edit_prj_desc").val(),
                        version: $("#edit_version").val(),
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
                                    location.href = "/project/"
                                }, 2000)

                            }

                        }
                        else {

                            toastr.error(data.msg);

                            setTimeout(function () {
                                $(".error").text("");

                            }, 5000)
                        }



                    }

                })
        });

     // 删除项目
    $("#btn_delete").click(function () {
            var env_ids=new Array();

                var count=0;

                var i=0;
                 var row = $(this).parent().parent();
                var pathname = window.location.pathname;
                var url = null;
                $("#table").find(":checkbox:checked").each(function() {

                    env_id = $(this).parent().next().text();


                    if (env_id != "") {

                        env_ids[i++] = env_id;


                    }

                    count++;

                });

            alert(count)
            if(count>0){
                url = /project/+env_id+pathname.replace('/project/', '/delete/')
                 // 删除插件的应用
            swal({

                title: "确定要删除吗？",
                type: "warning",
                showCancelButton: true,
                confirmButtonClass: "btn-danger",
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                closeOnConfirm: true

            },

            function () {
                $.ajax({

                    url: url,
                    type: 'post',
                    data:{
                        delete_id: env_id,

                    },

                    success:function (ret) {
                        var data = JSON.parse(ret);
                        if(data.status == 0){
                            row.remove();

                            toastr.success(data.msg);
                            setTimeout(function () {
                            location.href = "/project/"
                        }, 2000)


                        }else{
                            toastr.error(data.msg);
                            setTimeout(function () {
                            location.href = "/project/"
                        }, 2000)
                        }


                    }
                });

            });
            }
            else {
                toastr.error("请至少选择一项")
            }

    });

       //查看项目概述

            $("#prj_details").click(function(){
                var env_ids=new Array();
               var count=0;
                var i=0;
                var pathname = window.location.pathname;
                alert(pathname)
                var url = null;
                $("#table").find(":checkbox:checked").each(function() {

                    env_id = $(this).parent().next().text();

                    if (env_id != "") {

                        env_ids[i++] = env_id;

                    }

                    count++;

                });

                //alert(count)
                if (count==1) {
                    //alert(plan);
                    url = "/project/project=" + env_id + "";


                        $.ajax({

                            url: url,
                            type: 'get',
                            data: {


                            },
                        })
                    location.href = url;
                    }

                else if(count==0){
                    toastr.error("请至少选择一个选项!")
                }
                else{
                    toastr.error("编辑只能选择一个选项!");
                }
            });

     // 定义一个被选中的全局变量
    var checked_env_ids="{{ checked_env_ids }}";
    // 根据返回值去勾选对应列
    function check() {
        // 当前页的列id
        $("#table").find(":checkbox").each(function () {
            env_id = $(this).parent().next().text();
            if (env_id != ""){
                if(checked_env_ids.includes(String(env_id))){
                    $(this).attr("checked", true);
                }
            }

        });

    }
    // 根据当前页的勾选变化改变checked_env_ids值
    function change_checked_env_ids() {
        $("#table").find(":checkbox").each(function () {
            env_id=$(this).parent().next().text();
            if(env_id !=""){

                // 选中则判断数组是否存在，不存在则入栈
                if($(this).is(":checked")){
                    if(!checked_env_ids.includes(String(env_id))){
                        checked_env_ids.push(String(env_id));
                    }
                }
                // 未选中则判断数组是否存在，存在则出栈
                else{
                    if(checked_env_ids.includes(String(env_id))){
                        checked_env_ids = $.grep(checked_env_ids, function (value) {
                            return value != String(env_id);

                        });
                    }
                }
            }

        });
        alert(checked_env_ids)

    }
});
