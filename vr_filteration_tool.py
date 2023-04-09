# Write whole code into one function #
import gudhi as gd
import math
import json
import numpy as np
from collections import defaultdict
from io import StringIO

def vrFunction(data_, totalMaxExtend_, maxDimSimplex_, filePrefix_=None, write_visualize=True):

    ripsComplex_ = gd.RipsComplex(points= data_, max_edge_length= totalMaxExtend_)

    simplexTree_ = ripsComplex_.create_simplex_tree( max_dimension = maxDimSimplex_)

    simplexTree__ = gd.SimplexTree()

    for sk_value in simplexTree_.get_skeleton(maxDimSimplex_):

        circleRadius_ = math.ceil(sk_value[1] / 2)
        simplexTree__.insert(sk_value[0], filtration = math.ceil(circleRadius_))

    # Complex for visualization #

    filterOneSimplices_ = defaultdict(list)

    for sk_value in simplexTree__.get_skeleton(1):

        print("sk_value", sk_value)

        if len(sk_value[0]) == 2:
            filterOneSimplices_[sk_value[1]].append(sk_value[0])

    connectGraphTemp_ = defaultdict(list)

    for filter_ in range(totalMaxExtend_ + 1):  # Maximum number of filtrations are self.maxNumberExp + 1 #

        if filter_ in filterOneSimplices_:

            for simplex_ in filterOneSimplices_[filter_]:

                print("simplex", simplex_)

                connectGraphTemp_[simplex_[0]].append(simplex_[1])

                connectGraphTemp_[simplex_[1]].append(simplex_[0])

            links_ = connectGraphTemp_
            nodes_ = {}

            for node_ in connectGraphTemp_:

                nodes_.update({node_: [0] * int(filter_)})

            complex_ = {"nodes": nodes_, "links": links_, "meta": ""}

            if write_visualize:
                buf = StringIO()
                circleRadius_ = math.ceil(filter_ / 2)
                buf.write("%s_filter_%d.html" % (filePrefix_, int(filter_)))
                fileName__ = buf.getvalue()

                buf = StringIO()
                buf.write("Filter_%d" % (int(filter_)))
                titleName__ = buf.getvalue()
                visualize(complex_, int(filter_), path_html=fileName__, title=titleName__)

    return simplexTree_

def visualize(complex, totalExtend_,path_html= "mapper_visualization_output.html", title="My Data", graph_link_distance=30,
              graph_gravity=0.1, graph_charge=-120, custom_tooltips=None, width_html=0, height_html=0,
              show_tooltips=True, show_title=True, show_meta=True):
    # Turns the dictionary 'complex' in a html file with d3.js

    # print("title.split(_)[1]", title.split("_")[1])
    # title_ = copy.deepcopy(title)

    color_function_ = "average_signal_cluster"

    # Format JSON
    json_s = {}
    json_s["nodes"] = []
    json_s["links"] = []
    k2e = {}  # a key to incremental int dict, used for id's when linking

    for e, k in enumerate(complex["nodes"]):
        # Tooltip formatting
        if custom_tooltips != None:
            tooltip_s = "<h2>Cluster %s</h2>" % k + " ".join([str(f) for f in custom_tooltips[complex["nodes"][k]]])
            if color_function_ == "average_signal_cluster":
                tooltip_i = int(((sum([f for f in custom_tooltips[complex["nodes"][k]]]) / len(
                    custom_tooltips[complex["nodes"][k]])) * 30))
                json_s["nodes"].append(
                    {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                     "color": str(tooltip_i)})
            else:
                # json_s["nodes"].append(
                #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                #      "color": str(k.split("_")[0])})
                pass
                # kSplitFix_ = self.cover[k].getCoordLimits()[0][0]
                #
                # json_s["nodes"].append(
                #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                #      "color": str(kSplitFix_)})
        else:
            # tooltip_s = "<h2>Cluster %s</h2>Contains %s members." % (k, len(complex["nodes"][k]))
            # json_s["nodes"].append(
            #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
            #      "color": str(k.split("_")[0])})

            # kSplitFix_ = self.cover[k].getCoordLimits()[0][0]
            kSplitFix_ = 100
            tooltip_s = "<h2>Cluster %s</h2>Contains %s members." % (k, len(complex["nodes"][k]))
            bugFix_ = len(complex["nodes"][k])
            if bugFix_ == 0:
                bugFix_ = 1

            json_s["nodes"].append(
                {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(bugFix_)),
                 "color": str(kSplitFix_)})

        k2e[k] = e
    for k in complex["links"]:
        for link in complex["links"][k]:
            json_s["links"].append({"source": k2e[k], "target": k2e[link], "value": 1})

    # Width and height of graph in HTML output
    if width_html == 0:
        width_css = "100%"
        width_js = 'document.getElementById("holder").offsetWidth-20'
    else:
        width_css = "%spx" % width_html
        width_js = "%s" % width_html
    if height_html == 0:
        height_css = "100%"
        height_js = 'document.getElementById("holder").offsetHeight-20'
    else:
        height_css = "%spx" % height_html
        height_js = "%s" % height_html

    # Whether to show certain UI elements or not
    if show_tooltips == False:
        tooltips_display = "display: none;"
    else:
        tooltips_display = ""

    if show_meta == False:
        meta_display = "display: none;"
    else:
        meta_display = ""

    if show_title == False:
        title_display = "display: none;"
    else:
        title_display = ""

    with open(path_html, "wb") as outfile:
        html = """<!DOCTYPE html>
  <meta charset="utf-8">
  <meta name="generator" content="KeplerMapper">
  <title>%s | KeplerMapper</title>
  <link href='https://fonts.googleapis.com/css?family=Roboto:700,300' rel='stylesheet' type='text/css'>
  <style>
  * {margin: 0; padding: 0;}
  html { height: 100%%;}
  body {background: #111; height: 100%%; font: 100 16px Roboto, Sans-serif;}
  .link { stroke: #999; stroke-opacity: .333;  }
  .divs div { border-radius: 50%%; background: red; position: absolute; }
  .divs { position: absolute; top: 0; left: 0; }
  #holder { position: relative; width: %s; height: %s; background: #111; display: block;}
  h1 { %s padding: 20px; color: #fafafa; text-shadow: 0px 1px #000,0px -1px #000; position: absolute; font: 300 30px Roboto, Sans-serif;}
  h2 { text-shadow: 0px 1px #000,0px -1px #000; font: 700 16px Roboto, Sans-serif;}
  .meta {  position: absolute; opacity: 0.9; width: 220px; top: 80px; left: 20px; display: block; %s background: #000; line-height: 25px; color: #fafafa; border: 20px solid #000; font: 100 16px Roboto, Sans-serif;}
  div.tooltip { position: absolute; width: 380px; display: block; %s padding: 20px; background: #000; border: 0px; border-radius: 3px; pointer-events: none; z-index: 999; color: #FAFAFA;}
  }
  </style>
  <body>
  <div id="holder">
    <h1>%s</h1>
    <p class="meta">
    <b>Number of Elements in Cover</b><br>%s<br><br>
    <!-- <b>Linking locally</b><br>%s<br><br> -->
    <b>Color Function</b><br>%s( %s )<br><br>
    <b>Balls Radius</b><br>%s<br><br>
    </p>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script>
  <script>
  var width = %s,
    height = %s;
  var color = d3.scale.ordinal()
    .domain(["0","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"])
    .range(["#FF0000","#FF1400","#FF2800","#FF3c00","#FF5000","#FF6400","#FF7800","#FF8c00","#FFa000","#FFb400","#FFc800","#FFdc00","#FFf000","#fdff00","#b0ff00","#65ff00","#17ff00","#00ff36","#00ff83","#00ffd0","#00e4ff","#00c4ff","#00a4ff","#00a4ff","#0084ff","#0064ff","#0044ff","#0022ff","#0002ff","#0100ff","#0300ff","#0500ff"]);
  var force = d3.layout.force()
    .charge(%s)
    .linkDistance(%s)
    .gravity(%s)
    .size([width, height]);
  var svg = d3.select("#holder").append("svg")
    .attr("width", width)
    .attr("height", height);

  var div = d3.select("#holder").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0.0);

  var divs = d3.select('#holder').append('div')
    .attr('class', 'divs')
    .attr('style', function(d) { return 'overflow: hidden; width: ' + width + 'px; height: ' + height + 'px;'; });  

    graph = %s;
    force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();
    var link = svg.selectAll(".link")
      .data(graph.links)
      .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });
    var node = divs.selectAll('div')
    .data(graph.nodes)
      .enter().append('div')
      .on("mouseover", function(d) {      
        div.transition()        
          .duration(200)      
          .style("opacity", .9);
        div .html(d.tooltip + "<br/>")  
          .style("left", (d3.event.pageX + 100) + "px")     
          .style("top", (d3.event.pageY - 28) + "px");    
        })                  
      .on("mouseout", function(d) {       
        div.transition()        
          .duration(500)      
          .style("opacity", 0);   
      })
      .call(force.drag);

    node.append("title")
      .text(function(d) { return d.name; });
    force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });
    node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .attr('style', function(d) { return 'width: ' + (d.group * 2) + 'px; height: ' + (d.group * 2) + 'px; ' + 'left: '+(d.x-(d.group))+'px; ' + 'top: '+(d.y-(d.group))+'px; background: '+color(d.color)+'; box-shadow: 0px 0px 3px #111; box-shadow: 0px 0px 33px '+color(d.color)+', inset 0px 0px 5px rgba(0, 0, 0, 0.2);'})
      ;
    });
  </script>""" % (
        title, width_css, height_css, title_display, meta_display, tooltips_display, title,
        len(complex["nodes"].keys()), False, "distance_origin", complex["meta"],
        totalExtend_, width_js, height_js, graph_charge, graph_link_distance, graph_gravity,
        json.dumps(json_s))
        # % (
        # title, width_css, height_css, title_display, meta_display, tooltips_display, title, complex["meta"],
        # self.nr_cubes, self.overlap_perc * 100, self.link_local, self.color_function, complex["meta"],
        # str(self.clf), str(self.scaler), width_js, height_js, graph_charge, graph_link_distance, graph_gravity,
        # json.dumps(json_s))
        outfile.write(html.encode("utf-8"))
    # if self.verbose > 0:
    print("\nWrote d3.js graph to '%s'" % path_html)

