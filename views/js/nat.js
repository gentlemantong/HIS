/**
 * 搜索
 */
function doSearch(table) {
    let name = $('#name').val().trim();
    let id_no = $('#id_no').val().trim();
    // 渲染表格
    table.render({
        method: 'post',
        limits: [5,10,20],
        limit: 10,
        elem: '#data_list',
        url: '/nat/search',
        where: {'name': name, 'id_no': id_no},
        cols: [[
            {title: '序号', width: 70, align: 'center', templet: function (res) {return res.LAY_INDEX}},
            {field: 'name', title: '姓名', align: 'left', width: 95},
            {field: 'id_no', title: '身份证号', align: 'left', minWidth: 200},
            {field: 'orf', title: 'CT值：O', width: 95, align: 'left'},
            {field: 'n', title: 'CT值：N', width: 95, align: 'left'},
            {field: 'testing_date', title: '检测日期', width: 120, align: 'left'},
            {field: 'treatment', title: '医疗救治', align: 'left'},
            {fixed: 'right', title:'操作', toolbar: '#toolbar', align: 'center', width: 100}
        ]],
        page: true,
        done: function (res, curr, count) {
            // 设置表头样式
            $('th').css({'background-color': '#5792c6', 'color': '#fff', 'font-weight': 'bold'});
        }
    });
}

/**
 * 监听行操作
 */
function onToolbarAct(table, layer) {
    table.on('tool(data_list)', function (obj) {
        const data = obj.data;
        if (obj.event === 'edit') {
            layer.open({
                type: 2,
                title: '查看/修改',
                shadeClose: false,
                shade: 0.5,
                anim: 0,
                area: ['500px', '550px'],
                content: '/nat/edit/' + data['id']
            });
        }
    });
}

/**
 * 初始化核酸检测数据
 */
function initNatData(form, layer, laydate) {
    $.post('/nat/detail', {'id': $('#dataId').text()}, function (data) {
        if (data.code == 0) {
            param = data.data;
            $('#name').text(param['name']);
            $('#id_no').text(param['id_no']);
            $('#orf').val(param['orf']);
            $('#n').val(param['n']);
            laydate.render({elem: '#testing_date', value: param['testing_date']});
            $('#treatment').val(param['treatment']);
        } else {
            layer.msg(data.msg, {icon: 5});
        }
        return false;
    });
}

/**
 * 清洗数据
 */
function cleanData(data) {
    for (var k in data) {
        if (typeof(data[k]) == 'string') {
            data[k] = data[k].trim();
        }
    }
    return data;
}

/**
 * 执行更新
 */
function doEdit(layer, data) {
    $.post('/nat/edit', data, function (data) {
        if (data.code === 0) {
            layer.msg(data.msg, {icon: 1});
            // 延时1.5秒关闭弹窗
            setTimeout(function () {
                parent.layer.close(parent.layer.getFrameIndex(window.name));
            }, 1500);
        } else {
            layer.msg(data.msg, {icon: 5});
        }
        return false;
    });
}
