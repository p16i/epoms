function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

var diameter = 850;

var tree = d3.layout.tree()
    .size([360, diameter / 2 - 120])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

var diagonal = d3.svg.diagonal.radial()
    .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

var svg = d3.select("#graph").append("svg:svg")
    .attr("width", diameter)
    .attr("height", diameter)
  .append("g")
    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

filename =  getParameterByName('name');
d3.json( '/data/'+filename + ".json", function(error, root) {
  if (error) throw error;

  var nodes = tree.nodes(root),
      links = tree.links(nodes);


    var scale = d3.scale.linear()
        .domain([ root.min_rank, root.max_rank])
        .range([ 5, 10 ]);


  var link = svg.selectAll(".link")
      .data(links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

  var node = svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

  node.append("circle")
      .attr("r", function(d) {
          return scale(d.rank)
      })
      .append("svg:title")
      .text(function(d){
          return "PageRank : " +d.rank;
      });

  node.append("text")
      .attr("dy", ".31em")
      .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .attr("transform", function(d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
      .text(function(d) { return d.name.replace(/_/g, ' '); });
});

d3.select(self.frameElement).style("height", diameter - 100 + "px");

$(document).ready(function(){
    $("#selector").change(function(){
        newPath = window.location + "";
        newPath = newPath.replace(/(name=)(.+)/g,'$1'+$(this).val() );
        window.location = newPath;
    });

    $("#selector option").filter(function() {
        return $(this).text() == getParameterByName('name');
    }).attr('selected', true);

});



