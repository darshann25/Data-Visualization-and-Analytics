var w = 500;
var h = 300;
var padding = 30;
var dataset = [];
var numDataPoints = 100;
var upperDomain = 250;
var lowerDomain = 10;

function average(array) {
    var sum = 0;
    for( var i = 0; i < array.length; i++ ){
        sum += parseInt( array[i], 10 );
    }

    return sum/array.length;
    
}

for (var i = 0; i < numDataPoints; i++) {
    var newNumber1 = lowerDomain + Math.round(Math.random() * (upperDomain - lowerDomain));
    var newNumber2 = lowerDomain + Math.round(Math.random() * (upperDomain - lowerDomain));
    dataset.push([newNumber1, newNumber2]);
}

//Create scale functions
var oneScale = d3.scale.linear().domain([lowerDomain, upperDomain])
    .range([1,5]);

var xScale = d3.scale.linear()
    .domain([lowerDomain, upperDomain])
    .range([padding, w - padding * 2]);

var yScale = d3.scale.linear()
    .domain([lowerDomain, upperDomain])
    .range([h - padding, padding]);

// var rScale = d3.scale.linear()
//     .domain([lowerDomain, upperDomain])
//     .range([2, 5]);

//Define X axis
var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom");

//Define Y axis
var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");

//Create SVG element
var svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

var scaledXVals = []
var minYVal = upperDomain
var minYPoint = []

//Create circles
svg.selectAll("circle")
    .data(dataset)
    .enter()
    .append("circle")
    .attr("cx", function(d) {
        scaledXVals.push(xScale(d[0]))
        return xScale(d[0]);
    })
    .attr("cy", function(d) {
        if (minYVal > d[1]) {
            minYVal = d[1];
            minYPoint[0] = xScale(d[0]);
            minYPoint[1] = yScale(d[1]);
        }
        return yScale(d[1]);
    })
    .attr("r", function(d) {
        return Math.sqrt(Math.pow(oneScale(d[0]),2) + Math.pow(oneScale(d[1]),2));
    })
    .attr("stroke", function(d) {
        if (xScale(d[0]) > average(scaledXVals)) 
            return "blue"
        else 
            return "green";
    })
    .attr("fill","transparent");

//Create labels
svg.selectAll("text")
    .data(dataset)
    .enter()
    .append("text")
    .text("Min Y : " + minYVal)
    .attr("x", minYPoint[0])
    .attr("y", minYPoint[1])
    .attr("font-family", "sans-serif")
    .attr("font-size", "11px")
    .attr("fill", "black");

//Create X axis
svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + (h - padding) + ")")
    .call(xAxis);

//Create Y axis
svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(" + padding + ",0)")
    .call(yAxis);

//Add name
svg.append("text")
        .attr("x", w / 2)             
        .attr("y", padding / 2)
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .text("dpatel96");

