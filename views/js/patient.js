/**
 * 搜索
 */
function doSearch(table) {
    let name = $('#name').val().trim();
    let id_no = $('#id_no').val().trim();
    let phone = $('#phone').val().trim();
    // 渲染表格
    table.render({
        method: 'post',
        limits: [5,10,20],
        limit: 10,
        elem: '#data_list',
        url: '/patient/search',
        where: {'name': name, 'id_no': id_no, 'phone': phone},
        cols: [[
            {title: '序号', width: 70, align: 'center', templet: function (res) {return res.LAY_INDEX}},
            {field: 'name', title: '姓名', align: 'left', width: 95},
            {field: 'id_no', title: '身份证号', align: 'left', minWidth: 200},
            {field: 'phone', title: '联系方式', align: 'left'},
            {field: 'town', title: '镇/街道', width: 95, align: 'left'},
            {field: 'source', title: '来源', align: 'left'},
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
 * 新增弹窗
 */
function goAdd(layer) {
    layer.open({
        type: 2,
        title: '新增重点人员',
        shadeClose: false,
        shade: 0.5,
        anim: 0,
        area: ['99%', '99%'],
        content: '/patient/add'
    });
}

/**
 * 执行新增
 */
function doAdd(layer, data) {
    $.post('/patient/add', data, function (data) {
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
 * 监听行操作
 */
function onToolbarAct(table, layer) {
    table.on('tool(data_list)', function (obj) {
        const data = obj.data;
        if (obj.event === 'edit') {
            layer.open({
                type: 2,
                title: '修改人员信息',
                shadeClose: false,
                shade: 0.5,
                anim: 0,
                area: ['99%', '99%'],
                content: '/patient/edit/' + data['id']
            });
        }
    });
}

/**
 * 添加同住人
 */
function addRoommate() {
    $('#form_btn_box').before('<div class="layui-form-item" id="roommate' + window.roommateNumber + '">' +
            '<label class="layui-form-label"></label>' +
            '<div class="layui-inline">' +
                '<div class="layui-input-inline">' +
                    '<input type="text" name="roommate_name' + window.roommateNumber + '" placeholder="姓名" lay-verify="required" autocomplete="off" class="layui-input">' +
                '</div>' +
                '<div class="layui-input-inline">' +
                    '<input type="text" name="roommate_id_no' + window.roommateNumber + '" placeholder="身份证号" lay-verify="required|identity" autocomplete="off" class="layui-input">' +
                '</div>' +
                '<div class="layui-input-inline">' +
                    '<button type="button" class="layui-btn layui-btn-primary" onclick="removeRoommate(' + window.roommateNumber + ')">' +
                    '<i class="layui-icon layui-icon-subtraction"></i></button>' +
                '</div>' +
            '</div>' +
        '</div>');
    window.roommateBox.push(window.roommateNumber);
    window.roommateNumber += 1;
}

/**
 * 移除同住人
 */
function removeRoommate(number) {
    $('#roommate' + number).remove();
    window.roommateBox.forEach(function (item, index, arr) {
        if (item == number) {
            arr.splice(index, 1);
        }
    });
}

/**
 * 初始化重点人员数据
 */
function initPatientData(form, layer, laydate) {
    $.post('/patient/detail', {'data_id': $('#dataId').text()}, function (data) {
        if (data.code == 0) {
            param = data.data;
            $('#name').val(param['name']);
            $('#age').val(param['age']);
            $('#id_no').val(param['id_no']);
            $('#phone').val(param['phone']);
            $('#town').val(param['town']);
            $('#address').val(param['address']);
            $('#basic_disease').val(param['basic_disease']);
            $('#out_treatment').val(param['out_treatment']);
            laydate.render({elem: '#first_positive_date', value: param['first_positive_date']});
            laydate.render({elem: '#last_positive_date', value: param['first_positive_date']});
            $('#source').val(param['source']);
            $('#occupation').val(param['occupation']);
            $('#work_unit').val(param['work_unit']);
            form.render('select');
            var size = param['roommates'].length;
            for (var i=0; i<size; i++) {
                window.roommateNumber = i;
                window.roommateBox.push(i);
                $('#form_btn_box').before('<div class="layui-form-item" id="roommate' + i + '">' +
                    '<label class="layui-form-label"></label>' +
                    '<div class="layui-inline">' +
                        '<div class="layui-input-inline">' +
                            '<input type="text" id="roommate_name' + i + '" name="roommate_name' + i + '" placeholder="姓名" lay-verify="required" autocomplete="off" class="layui-input">' +
                        '</div>' +
                        '<div class="layui-input-inline">' +
                            '<input type="text" id="roommate_id_no' + i + '" name="roommate_id_no' + i + '" placeholder="身份证号" lay-verify="required|identity" autocomplete="off" class="layui-input">' +
                        '</div>' +
                        '<div class="layui-input-inline">' +
                            '<button type="button" class="layui-btn layui-btn-primary" onclick="removeRoommate(' + i + ')">' +
                            '<i class="layui-icon layui-icon-subtraction"></i></button>' +
                        '</div>' +
                    '</div>' +
                '</div>');
                $('#roommate_name' + i).val(param['roommates'][i]['name']);
                $('#roommate_id_no' + i).val(param['roommates'][i]['id_no']);
            }
            window.roommateNumber += 1;
        } else {
            layer.msg(data.msg, {icon: 5});
        }
        return false;
    });
}

/**
 * 执行编辑操作
 */
function doEdit(layer, data) {
    $.post('/patient/edit', data, function (data) {
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