/**
 * Created by Administrator on 2017/4/7.
 */

function onQuery()
{
    var name = $('#txtName').val();
    var type = $('#slctType').val();

    var params = "type="+type;
    params += "&name="+name;
    window.location.href = "/document/?" + params;
}

function onDownload(id)
{
    window.location.href = "/download/document/?id=" + id;
}

function onAddDo()
{
    var name = $('#txtName').val();
    var author = $('#txtAuthor').val();
    var type = $('#slctType').val();
    var file_name = $('#txtFileName').val();
    var extension = $('#txtExtension').val();

        if (_checkStringLength(name,5,50) == false) {
            _alertDialog("提示","文档名称在5~50个字符之间");
            return;
        }

        if (_checkStringLength(author,2,10) == false) {
            _alertDialog("提示","作者姓名在2~10个字符之间");
            return;
        }

        if (type == "") {
            _alertDialog("提示","请选择类型");
            return;
        }

        if (file_name == "" || extension == "") {
            _alertDialog("提示","请上传文件");
            return;
        }

        $.post("/document/add/do/",
            {
                name: name,
                author: author,
                type: type,
                file_name: file_name,
                extension: extension
            },
            function (data, status) {
                if (data.code == 200) {
                    if (data.success) {
                        window.location.href = "/add/success/?op_url=/document/add/&return_url=/document/";
                    }
                    else {
                        _alertDialog("提示",data.message);
                    }
                }
            });
}

function onReturn()
{
    window.location.href = "/document/";
}
