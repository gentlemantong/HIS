/**
 * 修改密码
 */
function changePass() {
    layer.open({
        type: 2,
        title: '修改密码',
        shadeClose: false,
        shade: 0.5,
        anim: 0,
        area: ['400px', '350px'],
        content: '/user/changePass'
    });
}

/**
 * 跳转至档案内容
 */
function jumpTo(uri) {
    $('#stage').attr('src', uri);
}