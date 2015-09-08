// Made with Plotly's postMessage API
// https://github.com/plotly/postMessage-API

var average = false;
var plot = document.getElementById('plot').contentWindow;
var X, Y, vis;

var d3_numeric = function(x) {
    return !isNaN(x);
}

var d3sum = function(array, f) {
  var s = 0,
      n = array.length,
      a,
      i = -1;
  if (arguments.length === 1) {
     // zero and null are equivalent
    while (++i < n) if (d3_numeric(a = +array[i])) s += a; 
  } else {
    while (++i < n) if (d3_numeric(a = +f.call(array, array[i], i))) s += a;
  }
  return s;
};

var movingWindowAvg = function (arr, step) {  
    return arr.map(function (_, idx) { 
        var wnd = arr.slice(idx - step, idx + step + 1); 
        var result = d3sum(wnd) / wnd.length; if (isNaN(result)) { result = _; }
        return result; 
    });
};

function applyAvg(index){
    // get current x, y data
    if( index===undefined ){ 
        index=0;
    }
    index=index.toString();
    plot.postMessage({
         task: 'getAttributes',
         attributes: [ 'data['+index+'].x', 'data['+index+'].y' ] },
         'https://plot.ly/');   
}

window.addEventListener('message', function(e) {
        
    var message = e.data;

    if( 'data[1].visible' in message.response ){
        var vis = message.response['data[1].visible'];
        console.log('Average visible', vis);
        if( vis === undefined ){
                plot.postMessage({
                    task: 'getAttributes',
                    attributes: [ 'data[0].x', 'data[0].y' ] },
                    'https://plot.ly/');
        }
        else if( vis == true ){
            vis = false;    
        }
        else{
            vis = true;
        }
        
        plot.postMessage({
            task: 'restyle',
            update: { 'visible':vis },
            indices: [1]
        }, 'https://plot.ly'); 
    }
    else{
        var window = document.getElementById('myRange').value;
        document.getElementById('window').value = window;
        X = message.response['data[0].x'];
        Y = message.response['data[0].y'];  
        if( average ){
            var arr = movingWindowAvg( Y, Number(window) );     
            console.log('Recalculated average');
            plot.postMessage({
                task: 'restyle',
                update: { y: [arr], x: [X], 'visible':true },
                indices: [1]
            }, 'https://plot.ly');  
        }
        else{       
            avg = { y: [arr], x: [X], visible:true, 
                     mode:'line', marker:{color:'#444'} };
            console.log( 'Adding moving average', avg );
            plot.postMessage({
                task: 'addTraces',
                traces: [ avg ],
                newIndices: [1]
            }, 'https://plot.ly');  
            applyAvg();
            average = true;
        }
    }
});

function toggleAvg(){
    // get current x, y data
    plot.postMessage({
         task: 'getAttributes',
         attributes: [ 'data[1].visible' ] },
         'https://plot.ly/');
}

function newPlot(){
    var plotURL = document.getElementById('plotURL').value + '.embed';
    var iframe = document.getElementById('plot');
    iframe.src = plotURL;   
    average = false;
}