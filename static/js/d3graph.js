/*
How to use:
- make div element with id networkmap
- make a function ongraphclick(d) after loading the script
      use d.name,d.password,d.ip
      function ongraphclick(d) {
          if (d3.event.defaultPrevented) return; // ignore drag
          alert(d.name);
      }
*/

//var graphdata;

function creategraph(graphdata,selector){
     //Constants for the SVG
    var width = 500,
        height = 500;

    //Set up the colour scale
    var color = d3.scale.category20();

    //Set up the force layout
    var force = d3.layout.force()
        .charge(-600)
        .linkDistance(80)
        .size([width, height]);

    //Append a SVG to the body of the html page. Assign this SVG as an object to svg
    var svg = d3.select(selector).append("svg")
        .attr("width", width)
        .attr("height", height);

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
        return  d.name +"</br>"+d.password+"</br>"+ d.ip + "</span>";
    })
    svg.call(tip);

    //Creates the graph data structure out of the json data
    force.nodes(graphdata.nodes)
        .links(graphdata.links)
        .start();

    //Create all the line svgs but without locations yet
    var link = svg.selectAll(".link")
        .data(graphdata.links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke-width", function (d) {
        return Math.sqrt(d.value);
    });

    //Do the same with the circles for the nodes - no 
    //Changed
    var node = svg.selectAll(".node")
        .data(graphdata.nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(force.drag)
        .on("click", ongraphclick)
        .on('mouseover', tip.show) 
        .on('mouseout', tip.hide);

    node.append("circle")
        .attr("r", 12)
        .style("fill", function (d) {
        return color(d.group);
    })

    node.append("text")
          .attr("dx", 10)
          .attr("dy", ".35em")
          .text(function(d) { return d.name });
    //End changed


    //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
    force.on("tick", function () {
        link.attr("x1", function (d) {
            return d.source.x;
        })
            .attr("y1", function (d) {
            return d.source.y;
        })
            .attr("x2", function (d) {
            return d.target.x;
        })
            .attr("y2", function (d) {
            return d.target.y;
        });

        //Changed

        d3.selectAll("circle").attr("cx", function (d) {
            return d.x;
        })
            .attr("cy", function (d) {
            return d.y;
        });

        d3.selectAll("text").attr("x", function (d) {
            return d.x;
        })
            .attr("y", function (d) {
            return d.y;
        });

        //End Changed

    });
}
