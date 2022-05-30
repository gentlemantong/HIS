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
            {field: 'name', title: '姓名', align: 'left'},
            {field: 'id_no', title: '身份证号', align: 'left', minWidth: 200},
            {field: 'phone', title: '联系方式', align: 'left'},
            {field: 'town', title: '镇/街道', align: 'left'},
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
 * 监听行操作
 */
function onToolbarAct(table, layer) {
    table.on('tool(data_list)', function (obj) {
        const data = obj.data;
        if (obj.event === 'detail') {
            var index = layer.open({
                type: 2,
                title: '个人档案',
                anim: 1,
                content: '/archive/' + data['id'],
                area: ['900px', '99%'],
                maxmin: true
            });
            layer.full(index);
        }
    });
}

/**
 * 初始化详情页数据
 */
function initData(layer, table, myChart) {
    const dataId = $('#dataId').text();

    // 初始化基本信息
    initPatientDetail(dataId);

    // 初始化核酸检测信息
    initNatList(table, dataId, myChart);

    // 初始化核酸检测数据折线图
    initNatChart(myChart, dataId);

    // 初始化治疗信息
    initMonitorList(table, dataId);
}


function initMonitorList(table, dataId) {
    table.render({
        method: 'post',
        limits: [5,10,20],
        limit: 10,
        elem: '#monitor_list',
        url: '/monitor/searchByPid',
        where: {'pid': dataId},
        cols: [[
            {title: '序号', width: 60, align: 'center', templet: function (res) {return res.LAY_INDEX}},
            {field: 'submit_date', title: '上报日期', align: 'left'},
            {field: 'health_condition', title: '健康状况', align: 'left'},
            {field: 'out_status', title: '是否出县', align: 'left'},
            {field: 'disposal_result', title: '处置结果', align: 'left'}
        ]],
        page: true,
        done: function (res, curr, count) {
            // 设置表头样式
            $('th').css({'background-color': '#5792c6', 'color': '#fff', 'font-weight': 'bold'});
        }
    });
}


/**
 * 初始化核酸检测数据
 */
function initNatList(table, dataId) {
    table.render({
        method: 'post',
        limits: [5,10,20],
        limit: 10,
        elem: '#testing_list',
        url: '/nat/searchByPid',
        where: {'pid': dataId},
        cols: [[
            {title: '序号', width: 60, align: 'center', templet: function (res) {return res.LAY_INDEX}},
            {field: 'testing_date', title: '检测日期', align: 'left'},
            {field: 'orf', title: 'CT值：O', align: 'left'},
            {field: 'n', title: 'CT值：N', align: 'left'},
            {field: 'treatment', title: '医疗救治', align: 'left'}
        ]],
        page: true,
        done: function (res, curr, count) {
            // 设置表头样式
            $('th').css({'background-color': '#5792c6', 'color': '#fff', 'font-weight': 'bold'});
        }
    });
}

/**
 * 初始化折线图
 */
function initNatChart(myChart, dataId) {
    $.post('/nat/chart', {'pid': dataId}, function (data) {
        if (data.code == 0) {
            var r = data.data;
            // 指定图表的配置项和数据
            var option = {
                toolbox: {
                    right: '30',
					feature: {
						saveAsImage: {name: $('#name').text() + '核酸折线图'}
					}
				},
				legend: {
				    orient: 'vertical',
				},
				tooltip: {
				    trigger: 'item',
				    triggerOn: 'click',
				    formatter: '【{b}】{c}'
				},
                xAxis: {
                    data: r.xAxis
                },
                yAxis: {
                    type: 'value',
                    scale: true
                },
                series: [
                    {
                        name: 'CT值：O',
                        type: 'line',
                        data: r.ct_o,
                        smooth: true,
                        label: { show: true, position: 'bottom' },
                        markPoint: {data: [{type: 'max', name: '最大值'}, {type: 'min', name: '最小值'}]},
                        markLine: {data: [{type: 'average', name: '平均值'}]}
                    }, {
                        name: 'CT值：N',
                        type: 'line',
                        data: r.ct_n,
                        smooth: true,
                        label: { show: true, position: 'bottom' },
                        markPoint: {data: [{type: 'max', name: '最大值'}, {type: 'min', name: '最小值'}]},
                        markLine: {data: [{type: 'average', name: '平均值'}]}
                    }
                ]
            };
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
            myChart.resize();
        }
        return false;
    });
}

/**
 * 初始化人员基本信息
 */
function initPatientDetail(dataId) {
    $.post('/patient/detail', {'data_id': dataId}, function (data) {
        if (data['code'] === 0) {
            res = data['data']
            $('#name').html(res['name']);
            $('#age').html('【' + res['age'] + '岁】');
            $('#id_no').html(res['id_no']);
            $('#phone').html(res['phone']);
            $('#address').html('【' + res['town'] + '】' + res['address']);
            $('#occupation').html(res['occupation']);
            $('#work_unit').html(res['work_unit']);
            $('#basic_disease').html(res['basic_disease']);
            $('#out_treatment').html(res['out_treatment']);
            $('#first_positive_date').html(res['first_positive_date']);
            $('#last_positive_date').html(res['last_positive_date']);
            $('#source').html('<span class="layui-badge">' + res['source'] + '</span>');

            // 格式化同住人信息
            var roommateStr = '';
            var roommates = res['roommates'];
            var size = roommates.length;
            for (var i=0; i<size; i++) {
                roommateStr += '<span class="layui-badge layui-bg-orange">' + roommates[i]['name'] + '  '
                 + roommates[i]['id_no'] + '</span>&nbsp;&nbsp;'
            }
            $('#roommates').html(roommateStr);
        }
        return false;
    });
}

var dataUri2Blob = function (imgName, dataUri, callback) {
    var binStr = atob(dataUri.split(',')[1]);
    var len = binStr.length;
    var arr = new Uint8Array(len);

    for (var i = 0; i < len; i++) {
        arr[i] = binStr.charCodeAt(i);
    }

    callback(imgName, new Blob([arr]));
}

var callback = function (imgName, blob) {
    var triggerDownload = $('<a>').attr('href', URL.createObjectURL(blob)).attr(
    'download', imgName).appendTo('body').on('click', function () {
        if (navigator.msSaveBlob) {
            return navigator.msSaveBlob(blob, imgName);
        }
    });

    triggerDownload[0].click();
    triggerDownload.remove();
}

/**
 * 截图生成图片
 */
function createImg() {
    var imgName = $('#name').text() + '.png';
    var shareContent = document.getElementById('capture');
    var copyDom = shareContent.cloneNode(true);
    copyDom.style.width = shareContent.scrollWidth + 'px';
    copyDom.style.height = shareContent.scrollHeight + 'px';
    document.querySelector('body').appendChild(copyDom);
    // 调用html2canvas截图
    html2canvas(copyDom).then(function (canvas) {
        const context = canvas.getContext('2d');
        context.webkitImageSmoothingEnabled = false;
        context.mozImageSmoothingEnabled = false;
        context.msImageSmoothingEnabled = false;
        context.imageSmoothingEnabled = false;
        context.imageSmoothingQuality = 'HIGH';
        let imgUrl = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
        dataUri2Blob(imgName, imgUrl, callback);
        copyDom.remove();
    });
}
