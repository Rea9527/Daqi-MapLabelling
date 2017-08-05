window.onload = function() {

    console.log(imageData);

    isStart = false;
    mode = 0;
    
    DRAW_POINT = 0;
    DRAW_REGION = 1;
    
    currentState = [];
    all_rgbs = [];

    regionMap = {
        '香洲': {id: 'G3800', 'longitude': '113.5667', 'latitude': '22.275'},
        '保税区': {id: 'G3850', 'longitude': '113.4943', 'latitude': '22.1769'},
        '翠微': {id: 'G3852', 'longitude': '113.5112', 'latitude': '22.2661'},
        '界涌': {id: 'G3853', 'longitude': '113.4934', 'latitude': '22.3174'},
        '珠海港': {id: 'G3856', 'longitude': '113.184', 'latitude': '21.97'},
        '斗门镇': {id: 'G3858', 'longitude': '113.183', 'latitude': '22.233'},
        '香洲港': {id: 'G3859', 'longitude': '113.579', 'latitude': '22.292'},
        '香灶镇': {id: 'G3860', 'longitude': '113.348', 'latitude': '22.049'},
        '高栏西': {id: 'G3862', 'longitude': '113.227', 'latitude': '21.928'},
        '湾仔': {id: 'G1221', 'longitude': '113.525', 'latitude': '22.204'},
        '横琴桥': {id: 'G1226', 'longitude': '113.513', 'latitude': '22.163'},
        '淇澳桥': {id: 'G1227', 'longitude': '113.611', 'latitude': '22.388'},
        '情侣北': {id: 'G1229', 'longitude': '113.616', 'latitude': '22.35'},
        '保税区新站': {id: 'G1230', 'longitude': '113.4943', 'latitude': '22.1769'},
        '港珠澳大桥': {id: 'G1231', 'longitude': '113.6407', 'latitude': '22.2461'},
        '井岸': {id: 'G1250', 'longitude': '113.283', 'latitude': '22.217'},
        '灯笼': {id: 'G1252', 'longitude': '113.372', 'latitude': '22.203'},
        '新乡村': {id: 'G1253', 'longitude': '113.167', 'latitude': '22.26'},
        '大赤坎': {id: 'G1255', 'longitude': '113.235', 'latitude': '22.278'},
        '白藤大闸': {id: 'G1256', 'longitude': '113.362', 'latitude': '22.163'},
        '白藤湖': {id: 'G1258', 'longitude': '113.32', 'latitude': '22.188'},
        '白蕉': {id: 'G1259', 'longitude': '113.332', 'latitude': '22.258'},
        '竹洲': {id: 'G1262', 'longitude': '113.267', 'latitude': '22.367'},
        '斗门大桥': {id: 'G1265', 'longitude': '113.352', 'latitude': '22.27'}
    }

    colorMap = [
        {r: 255, g: 0, b: 0},
        {r: 255, g: 128, b: 0},
        {r: 255, g: 255, b: 64},
        {r: 64, g: 255, b: 32},
        {r: 0, g: 128, b: 255}
    ]
    
    $('select').material_select();

    // register();
    load_map();
    
    $('#evaluate_btn').on('click', evaluation);
    $('#reset_btn').on('click', reset);
    $('#map_switcher').on('change', switch_mode);

}

function load_map() {
    var c = document.getElementById('zhuhaiMap');
    var iakImg = document.getElementById('img')
    var ctx = c.getContext('2d');
    $caman = new Image();
    $caman.src = iakImg.src;
    $caman.setAttribute('crossOrigin', '');
    $caman.crossOrigin = "Anonymous";
    ctx.drawImage(iakImg, 0, 0);
    a = imageData;
    // console.log(a);

    var color = ['#FF0000', '#FF8000', '#FFFF40', '#40FF20', '#0080FF'];
    // band
    var grd = ctx.createLinearGradient(730, 150, 730, 400);
    grd.addColorStop(0, color[4]);
    grd.addColorStop(0.25, color[3]);
    grd.addColorStop(0.5, color[2]);
    grd.addColorStop(0.75, color[1]);
    grd.addColorStop(1, color[0]);
    ctx.fillStyle = grd;
    ctx.fillRect(730, 150, 30, 250);

    //font
    ctx.font = "15px Courier New";
    ctx.fillStyle = "black";
    ctx.fillText("优", 765, 150);
    ctx.fillText("良", 765, 210);
    ctx.fillText("中", 765, 280);
    ctx.fillText("差", 765, 340);
    ctx.fillText("恶劣", 765, 400);

}

// draw point on map
function drawPoint(x, y, rank) {
    // x 101-721
    // y 63-543
    var color = ['#FF0000', '#FF8000', '#FFFF40', '#40FF20', '#0080FF'];
    var startColor = color[rank];
    
    var c = document.getElementById("zhuhaiMap");
    var ctx = c.getContext('2d');
    var grd = ctx.createRadialGradient(x, y, 0.5, x, y, 6);
    grd.addColorStop(0,color[rank]);
    grd.addColorStop(1,(color[rank+1] ? color[rank+1] : color[rank]));
    
    ctx.fillStyle = color[rank];
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, 2*Math.PI);
    ctx.closePath();
    ctx.fill();
}

// draw point on map and interpolate
function drawRegion() {

    // 103-721, 63-540
    for (var x = 103; x < 721; x++) {
        for (var y = 63; y < 540; y++) {
            var pos = y * 800 * 4 + x * 4;

            if (a[pos] > 200 && a[pos+1] > 200 && a[pos+2] > 200) {

                var rgb = idw({x: x, y: y}, currentState, all_rgbs);
                var c = document.getElementById("zhuhaiMap");
                var ctx = c.getContext('2d');
                ctx.strokeStyle = 'rgb(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ')';
                ctx.beginPath();
                ctx.arc(x, y, 1, 0, 2*Math.PI);
                ctx.stroke();

            }
        }
    }
}

// idw interpolate
function idw(target_point, all_points, all_rgbs) {
    if (all_points.length == 1) {
        return all_rgbs[0];
    }
    var result = {r: 0, g: 0, b: 0};

    var arg_top = {r: 0, g: 0, b: 0}, arg_down = 0;
    for (var i = 0; i < all_points.length; i++) {
        var d2 = distance(target_point, all_points[i]);
        // arg down
        arg_down += 1 / d2;
        // arg top
        var rgb = all_rgbs[i];
        arg_top.r += rgb.r / d2;
        arg_top.g += rgb.g / d2;
        arg_top.b += rgb.b / d2;
    }
    arg_down *= 1.1;
    // console.log(arg_down, arg_top.r, arg_top.g, arg_top.b);

    result.r = Math.round(arg_top.r / arg_down);
    result.g = Math.round(arg_top.g / arg_down);
    result.b = Math.round(arg_top.b / arg_down);
    // console.log(result)

    return result;
}

function distance(p1, p2) {
    var result = (p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y);
    return result;
}

// switch button callback
function switch_mode() {

    if (!isStart) return;

    var ison = $('#map_switcher input:checked').val();

    var c = document.getElementById('zhuhaiMap');
    var iakImg = document.getElementById('img')
    var ctx = c.getContext('2d');
    $caman = new Image();
    $caman.src = iakImg.src;
    ctx.drawImage(iakImg, 0, 0);

    var color = ['#FF0000', '#FF8000', '#FFFF40', '#40FF20', '#0080FF'];

    var c = document.getElementById("zhuhaiMap");
    var ctx = c.getContext('2d');
    //band
    var grd = ctx.createLinearGradient(730, 150, 730, 400);
    grd.addColorStop(0, color[4]);
    grd.addColorStop(0.25, color[3]);
    grd.addColorStop(0.5, color[2]);
    grd.addColorStop(0.75, color[1]);
    grd.addColorStop(1, color[0]);
    
    ctx.fillStyle = grd;
    ctx.fillRect(730, 150, 30, 250);
    //font
    ctx.font = "15px Courier New";
    ctx.fillStyle = "black";
    ctx.fillText("优", 765, 150);
    ctx.fillText("良", 765, 210);
    ctx.fillText("中", 765, 280);
    ctx.fillText("差", 765, 340);
    ctx.fillText("恶劣", 765, 400);

        if (ison == undefined) {
            // draw point
            currentState.forEach(function(e) {
                drawPoint(e.x, e.y, e.rank);
            }, this);
            
        } else {
            // interpolation
            drawRegion();
            
        }
    // });
    
}

function evaluation() {

    isStart = true;

    var region = $('#region-select').val();
    if (!regionMap[region]) {

    } else {
        pos = convert_to_pixel(regionMap[region]['longitude'], regionMap[region]['latitude']);
        
        //compute
        if (checkValid()) {
            var rank = compute();

            currentState.push({x: pos.x, y: pos.y, rank: rank});
            all_rgbs.push(colorMap[rank]);
            mode = $('#map_switcher input:checked').val();
            if (mode == undefined) drawPoint(pos.x, pos.y, rank);
            else drawRegion();
        }
    }
}

function checkValid() {
    var temperature = $('#temperature').val();
    var rain = $('#rain').val();
    var AQI = $('#AQI').val();
    var humidity = $('#humidity').val();
    var wind = $('#wind').val();
    var air = $('#air').val();

    if (!parseFloat(temperature)) {
        $('#temperature').attr("class", "invalid");
        return false;
    }
    else $('#temperature').attr("class", "");

    if (!parseFloat(rain)) {
        $('#rain').attr("class", "invalid");
        return false;
    }
    else $('#rain').attr("class", "");

    if (!parseFloat(AQI)) {
        $('#AQI').attr("class", "invalid");
        return false;
    }
    else $('#AQI').attr("class", "");
    
    if (!parseFloat(humidity)) {
        $('#humidity').attr("class", "invalid");
        return false;
    }
    else $('#humidity').attr("class", "");
    
    if (!parseFloat(wind)) {
        $('#wind').attr("class", "invalid");
        return false;
    }
    else $('#wind').attr("class", "");

    if (!$('#history:checked').val()) {
        if (!parseFloat(air)) {
        
            $('#air').attr("class", "invalid");
            return false;
        }
        else $('#air').attr("class", "");
    }
    

    return true;
}

function compute() {
    var currentMonth = $('#history:checked').val() ? false : true;

    var vals = get_values();

    var m = vals.month;
    var t = vals.temperature;
    var r = vals.rain;
    var p = vals.AQI;
    JA = [4051.9,5578.6,4590.6,4069.7,5569.6,6197.8,6660.4,5281.1,5981.5,6336.2,4666.0,4994.8,5578.6]
    if (currentMonth) var j = vals.air;
    else var j = JA[m-1];
    var h = vals.humidity;
    var v = vals.wind;

    // 标准化
    if (m == 1 || m == 3 || m == 5 || m == 7 || m == 8 || m == 10 || m == 12)
        rd = r/31;
    else if (m == 4 || m == 6 || m == 9 || m == 11)
        rd = r/30;
    else if (m == 13)
        rd = r/29;
    else
        rd = r/28;

    if (r<0 || p<0 || j<0 || h<0 || v<0)
        point.set('输入参数错误！')
    else {
        i = (1.8*t + 32) - 0.55*(1 - h/100)*(1.8*t - 26) - 3.2*Math.sqrt(v)
        jr = 3.1536*0.001*Math.sqrt(3.1415926)/2*j + 2.19*60*10*rd/(24*60*60)

        ta = [15.0,15.8,18.5,22.3,25.7,27.7,28.6,28.4,27.4,25.1,20.9,16.7,15.8]
        ra = [26.9,57.9,84.7,199.6,298.1,390.0,319.3,336.7,220.8,71.7,44.3,30.6,57.9]
        tt = (Math.abs(t-ta[m-1])-10)/(0-10)*100
        rr = (Math.sqrt(Math.abs(r-ra[m-1]))-37.42)/(0-37.42)*100
        pp = (p-100)/(15-100)*100
        jj = (jr-5)/(20-5)*100
        ii = (Math.abs(i-62.5)-22.5)/(0-22.5)*100

        // 超出范围的数进行处理
        if (tt>100)
            tt = 100.0
        else if (tt<0)
            tt = 0.0
        if (rr>100)
            rr = 100.0
        else if (rr<0)
            rr = 0.0
        if (pp>100)
            pp = 100.0
        else if (pp<0)
            pp = 0.0
        if (jj>100)
            jj = 100.0
        else if (jj<0)
            jj = 0.0
        if (ii>100)
            ii = 100.0
        else if (ii<0)
            ii = 0.0


        // 权重矩阵
        W = [[0.1391,0.1019,0.2673,0.2565,0.2353],
                [0.1304,0.0940,0.2488,0.3044,0.2223],
                [0.1355,0.0969,0.2576,0.2798,0.2302],
                [0.1610,0.1031,0.2662,0.2233,0.2463],
                [0.1458,0.1005,0.2668,0.2313,0.2556],
                [0.1356,0.0973,0.2566,0.2172,0.2934],
                [0.1511,0.1021,0.2692,0.2370,0.2405],
                [0.1476,0.0981,0.2566,0.2501,0.2475],
                [0.1330,0.0968,0.2548,0.2487,0.2668],
                [0.1335,0.0968,0.2540,0.2341,0.2815],
                [0.1540,0.0999,0.2634,0.2243,0.2584],
                [0.1355,0.0990,0.2736,0.2606,0.2313],
                [0.1304,0.0940,0.2488,0.3044,0.2223],]

        var point = W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii;

        $('#temperature-tr td:eq(1)').html(""+W[m-1][0]);
        $('#rain-tr td:eq(1)').html(""+W[m-1][1])
        $('#pollutant-tr td:eq(1)').html(""+W[m-1][2])
        $('#clean-tr td:eq(1)').html(""+W[m-1][3])
        $('#comfort-tr td:eq(1)').html(""+W[m-1][4])
        $('#temperature-tr td:eq(2)').html(""+Math.round(tt))
        $('#rain-tr td:eq(2)').html(""+Math.round(rr))
        $('#pollutant-tr td:eq(2)').html(""+Math.round(pp))
        $('#clean-tr td:eq(2)').html(""+Math.round(jj))
        $('#comfort-tr td:eq(2)').html(""+Math.round(ii))

        var rank;
        if (point<21) {
            $('#point td:eq(2)').html(Math.round(point) + ' - 恶劣');
            $('#point td:eq(2)').attr('class', 'font-wicked');
            rank = 0;
        }
            
        else if (point<41) {
            $('#point td:eq(2)').html(Math.round(point) + ' - 差')
            $('#point td:eq(2)').attr('class', 'font-bad');
            rank = 1;
        }
            
        else if (point<56) {
            $('#point td:eq(2)').html(Math.round(point) + ' - 中')
            $('#point td:eq(2)').attr('class', 'font-medium');
            rank = 2;
        }
            
        else if (point<70) {
            $('#point td:eq(2)').html(Math.round(point) + ' - 良')
            $('#point td:eq(2)').attr('class', 'font-good');
            rank = 3;
        }
            
        else {
            $('#point td:eq(2)').html(Math.round(point) + ' - 优')
            $('#point td:eq(2)').attr('class', 'font-great');
            rank = 4;
        }

        return rank;
    }
        
}

function get_values() {
    var month = parseInt($('#month-select').val());
    var temperature = parseFloat($('#temperature').val());
    var rain = parseFloat($('#rain').val());
    var AQI = parseFloat($('#AQI').val());
    var humidity = parseFloat($('#humidity').val());
    var wind = parseFloat($('#wind').val());
    var air = parseFloat($('#air').val());

    return {month, temperature, rain, AQI, humidity, wind, air};
}

function reset() {
    $('#temperature').val("");
    $('#rain').val("");
    $('#AQI').val("");
    $('#humidity').val("");
    $('#wind').val("");
    $('#air').val("");

    $('#point td:eq(1)').html("")
    $('#point td:eq(2)').html("")
    $('#temperature-tr td:eq(1)').html("");
    $('#rain-tr td:eq(1)').html("")
    $('#pollutant-tr td:eq(1)').html("")
    $('#clean-tr td:eq(1)').html("")
    $('#comfort-tr td:eq(1)').html("")
    $('#temperature-tr td:eq(2)').html("")
    $('#rain-tr td:eq(2)').html("")
    $('#pollutant-tr td:eq(2)').html("")
    $('#clean-tr td:eq(2)').html("")
    $('#comfort-tr td:eq(2)').html("")

    load_map();
    currentState = [];
    all_rgbs = [];

    isStart = false;


}


function convert_to_pixel(longitude, latitude) {
    // x 113.102638 114.319862
    // y 21.7 22.6

    // x 101-721 = 620
    // y 63-543
    var xmin = 113.102638, xmax = 114.319862;
    var ymin = 21.7, ymax = 22.6;

    var x, y;
    x = ((longitude-xmin) / (xmax-xmin)) * 620 + 101;
    y = 543 - ((latitude-ymin) / (ymax-ymin)) * 480;
    
    return {x, y}
}