from django.test import TestCase

# Create your tests here.

def edit_article(request, pid, option):
    """
    后台文件的管理（删除，编辑）
    :param request:
    :param option:
    :param pid:
    :return:
    """
    article_obj = models.Article.objects.filter(pk=pid).first()
    print("article_obj:", article_obj)
    if article_obj and option == "delete":
        try:
            article_obj.delete()
            reg = {'status': 0, 'msg': '删除成功!'}
        except Exception as e:
            reg = {'status': 1, 'msg': '删除失败'}

        return HttpResponse(json.dumps(reg))

    elif article_obj and option == "edit":
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")

            # 防止xss攻击，过滤scrip标签
            soup = BeautifulSoup(content, "html.parser")
            for tag in soup.find_all():

                if tag.name == "script":
                    tag.decompose()

            # 构建摘要数据，获取标签字符串的文本前150个字符
            desc = soup.text[0:150]+"...."

            if len(title) != 0:
                models.Article.objects.filter(nid=pid).update(title=title, desc=desc, content=str(soup), user=request.user)
                return redirect("/cn_backend")
            else:
                return render(request, "backend/edit_article.html",  {"error_msg": "文章标题不能为空!"})

        return render(request, "backend/edit_article.html", {"article_obj": article_obj})
    else:
        return render(request, "not_found.html")





{% block script %}
    <script type="text/javascript">
        $(".btn_delete").click(function () {
            var delete_id = $(this).parent().siblings('td').eq(0).text();
            var row = $(this).parent().parent();
            var pathname = window.location.pathname;
            var url = null;

            if(pathname.indexOf("cn_backend/")>0){
                url = /article/+delete_id+pathname.replace('/cn_backend/', '/delete/')
            }


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
                        delete_id: delete_id,

                    },
                    success:function (ret) {
                        var data = JSON.parse(ret);
                        if(data.status == 0){
                            row.remove();
                            swal(data.msg);
                        }else{
                            swal(data.msg)
                        }


                    }
                });

            });

        });
    </script>
{% endblock %}



re_path(r'article/(\d+)/(delete|edit)', views.edit_article),
