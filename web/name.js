function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

var width = 960;
var height = 500;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(100)
    .size([width, height]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

filename =  getParameterByName('file');

d3.json( filename + ".json", function(error, graph) {
    if (error) throw error;

    var ranks = [];

    for( var i = 0; i < graph.nodes.length; i++ ) {
        ranks.push( graph.nodes[i].rank )
    }

    var minRank = Math.min.apply( null, ranks );

    var linkNodes = [];

    graph.links.forEach(function(link) {
        linkNodes.push({
            source: graph.nodes[link.source],
            target: graph.nodes[link.target]
        });
    });
    var maxRank = Math.max.apply( null, ranks );

    var scale = d3.scale.linear()
    .domain([ minRank, maxRank])
    .range([ 5, 10 ]);

    force
    .nodes(graph.nodes)
    .links(graph.links)
    .start();

    var link = svg.selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = svg.selectAll(".node")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", function(d){
            return scale(d.rank)
            })
    .style("fill", function(d) {
        return color(d.depth);
    })
    .call(force.drag);

    node.append("title")
        .text(function(d) { return d.name; });

    text = svg.append("g").selectAll("text")
        .data(graph.nodes)
        .enter().append("text")
        .attr('class', 'text')
        .attr("x", function(d){
            return scale(d.rank) + 3
        })
        .attr("y", ".31em")
        .text(function(d) {
            if(1){
                return d.name;
            }
        });

    var linkNode = svg.selectAll(".link-node")
        .data(linkNodes)
        .enter().append("circle")
        .attr("class", "link-node")
        .attr("r", 1)
        .style("fill", "#ccc");


    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

        /*
           linkNode.attr("cx", function(d) { return d.x = (d.source.x + d.target.x) * 0.5; })
           .attr("cy", function(d) { return d.y = (d.source.y + d.target.y) * 0.5; });
           */

        text.attr("transform", transform);
    });

    function transform(d) {
        return "translate(" + d.x + "," + d.y + ")";
    }
});

