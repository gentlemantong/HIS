/**
 * 登录
 * @param field: 包含用户名和密码的json
 * @param layer: layer
 */
function login(field, layer) {
    $.post('/user/login', field, function (data) {
        if (data.code === 0) {
            layer.msg(data.msg, {icon: 5});
        } else {
            layer.msg(data.msg, {icon: 1});
            setTimeout(function() {
                window.location.href = '/';
            }, 500);
        }
    });
}

/**
 * 清洗数据
 * @param field: form表单数据
 * @return 清洗好的数据
 */
function cleanData(field) {
    field['oldPass'] = field['oldPass'].trim();
    field['newPass'] = field['newPass'].trim();
    field['newPass2'] = field['newPass2'].trim();
    return field;
}

/**
 * 执行修改密码
 * @param field: form表单数据
 */
function changePwd(field) {
    $.post('/user/changePass', field, function (data) {
        if (data.code === 0) {
            layer.msg(data.msg, {icon: 1});
        } else {
            layer.msg(data.msg, {icon: 5});
        }
        return;
    });
}