import gudhi as gd
from collections import defaultdict
import numpy as np
import json
from io import StringIO

class filtration:

    def __init__(self, cover_, maxNumberExp_, maxDimSimplex_, clusteringAlgo_, expansionRate_, maxExtend_,
                 filePrefix_=None):

        self.cover = cover_
        self.maxNumberExp = maxNumberExp_ # Maximum number of filtrations are self.maxNumberExp + 1
        self.maxDimSimplex = maxDimSimplex_
        self.simplicialComplex = gd.SimplexTree()
        self.filePrefix = filePrefix_ # Location of directory to store weighted filtration #
        self.clusteringAlgo = clusteringAlgo_  # Clustering algorithm to build initial cover
        self.expansionRate = expansionRate_  # Rate we expand the bin. Denoted as \alpha in the paper
        self.maxExtend = maxExtend_  # Maximum extension of any bin in any direction. Denoted as \pi in the paper.

    def initial(self, write_visualize=True):

        self.addZeroSimplices()
        self.addOneSimplices()
        self.addHigherThanOneSimplices(write_visualize=write_visualize)

    def addZeroSimplices(self):

        for key_ in self.cover:

            self.simplicialComplex.insert([key_])

    def addOneSimplices(self):

        lenOfCover_ = len(self.cover.keys())

        for index_ in range(1, self.maxNumberExp + 1): # Maximum number of filtrations are self.maxNumberExp + 1 #

            filterTime_ = index_

            for index__ in range(lenOfCover_):

                binTemp_ = self.cover[index__].getExpansionBins()[index_]

                for index___ in range(index__ + 1, lenOfCover_):

                    binTemp__ =  self.cover[index___].getExpansionBins()[index_]

                    if self.isBinIntersection(binTemp_, binTemp__):

                        if not self.simplicialComplex.find([index__, index___]):

                            self.simplicialComplex.insert([index__, index___], filtration = filterTime_)

    def addHigherThanOneSimplices(self, write_visualize=True):

        # It add all the simplices of dimension higher than one #

        connectGraphTemp_ = defaultdict(list)

        filterOneSimplices_ = defaultdict(list)

        for sk_value in self.simplicialComplex.get_skeleton(1):

            print("sk_value", sk_value)

            if len(sk_value[0])== 2:

                filterOneSimplices_[sk_value[1]].append(sk_value[0])


        for filter_ in range(self.maxNumberExp + 1): # Maximum number of filtrations are self.maxNumberExp + 1 #

            for simplex_ in filterOneSimplices_[filter_]:

                print("simplex", simplex_)

                connectGraphTemp_[simplex_[0]].append(simplex_[1])

                connectGraphTemp_[simplex_[1]].append(simplex_[0])


            self.addThreeSimplicesForConnectedGraph(connectGraphTemp_, filter_)

            ####################
            # Save Filter Mesh #
            ####################

            # buf = StringIO()
            # buf.write("%s_filter_%d.msh" % (self.filePrefix, int(filter_)))
            # fileName__ = buf.getvalue()
            #
            # self.saveMesh(fileName__)

            ######################
            # Save Filter Mapper #
            ######################

            complex_ = self.complexForVisualization(connectGraphTemp_, filter_)
            if write_visualize:
                buf = StringIO()
                buf.write("%s_filter_%d.html" % (self.filePrefix, int(filter_)))
                fileName__ = buf.getvalue()

                buf = StringIO()
                buf.write("Filter_%d" % (int(filter_)))
                titleName__ = buf.getvalue()

                self.visualize_(complex_, path_html= fileName__, title= titleName__)


    def complexForVisualization(self, connectGraph_, filter_):

        links_ = connectGraph_
        nodes_ = {}

        for binIndex_, bin_ in self.cover.items():

            pixelListTemp_ =[ x for x in bin_.getExpansionBins()[filter_].getBinPixelDict() ]

            nodes_.update({binIndex_: pixelListTemp_})


        complex_ = {"nodes" : nodes_, "links": links_, "meta": ""}

        return complex_

    def addThreeSimplicesForConnectedGraph(self, connectGraph_, filter_):

        for node_, nodeList_ in connectGraph_.items():

            for node__ in nodeList_:

                nodeList__= connectGraph_[node__]

                commonNodes_ = list(set(nodeList_).intersection(nodeList__))

                for commonNode_ in commonNodes_:

                    simplex_ = [node_, node__, commonNode_]

                    if not self.simplicialComplex.find(simplex_):

                        self.simplicialComplex.insert(simplex_, filtration = filter_)



    def isBinIntersection(self, bin_, bin__):

        isBinsIntersects_ = True

        for index_, coordLimit_ in enumerate(bin_.getCoordLimits()):

            coordLimit__ = bin__.getCoordLimits()[index_]

            if not (coordLimit__[0] >= coordLimit_[0] and coordLimit__[0] <= coordLimit_[1]) and \
                    not (coordLimit__[1] >= coordLimit_[0] and coordLimit__[1] <= coordLimit_[1]):

                isBinsIntersects_ = False
                break


        # Comment for the test #

        # if isBinsIntersects_:
        #     # Include points for the intersection of bin_ and bin__ to be True #
        #     list1_ = list(bin_.getBinPixelDict().keys())
        #     list2_ = list(bin__.getBinPixelDict().keys())
        #
        #     if len(list1_) + len(list2_) == len(set(list1_ + list2_)):
        #
        #         isBinsIntersects_ = False

        return isBinsIntersects_

    def visualize_(self, complex, path_html= "mapper_visualization_output.html", title="My Data", graph_link_distance=30,
                  graph_gravity=0.1, graph_charge=-120, custom_tooltips=None, width_html=0, height_html=0,
                  show_tooltips=True, show_title=True, show_meta=True):
        # Turns the dictionary 'complex' in a html file with d3.js

        # print("title.split(_)[1]", title.split("_")[1])
        # title_ = copy.deepcopy(title)

        # Format JSON
        json_s = {}
        json_s["nodes"] = []
        json_s["links"] = []
        k2e = {}  # a key to incremental int dict, used for id's when linking

        for e, k in enumerate(complex["nodes"]):
            # Tooltip formatting
            if custom_tooltips != None:
                tooltip_s = "<h2>Cluster %s</h2>" % k + " ".join([str(f) for f in custom_tooltips[complex["nodes"][k]]])
                if self.color_function == "average_signal_cluster":
                    tooltip_i = int(((sum([f for f in custom_tooltips[complex["nodes"][k]]]) / len(
                        custom_tooltips[complex["nodes"][k]])) * 30))
                    json_s["nodes"].append(
                        {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                         "color": str(tooltip_i)})
                else:
                    # json_s["nodes"].append(
                    #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                    #      "color": str(k.split("_")[0])})

                    # kSplitFix_ = self.cover[k].getCoordLimits()[0][0]
                    #
                    # json_s["nodes"].append(
                    #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                    #      "color": str(kSplitFix_)})

                    pass
            else:
                # tooltip_s = "<h2>Cluster %s</h2>Contains %s members." % (k, len(complex["nodes"][k]))
                # json_s["nodes"].append(
                #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                #      "color": str(k.split("_")[0])})

                kSplitFix_ = 100
                tooltip_s = "<h2>Cluster %s</h2>Contains %s members." % (k, len(complex["nodes"][k]))
                json_s["nodes"].append(
                    {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
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
        <b>Clusterer</b><br>%s<br><br>
        <b>Alpha</b><br>%s<br><br>
        <b>Search Neighborhood</b><br>%s<br><br>
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
            len(self.cover.keys()), False, "distance_origin", complex["meta"], str(self.clusteringAlgo),
            self.expansionRate, self.maxExtend*int(title.split("_")[-1]), width_js, height_js, graph_charge, graph_link_distance, graph_gravity,
            json.dumps(json_s))
            # % (
            # title, width_css, height_css, title_display, meta_display, tooltips_display, title, complex["meta"],
            # self.nr_cubes, self.overlap_perc * 100, self.link_local, self.color_function, complex["meta"],
            # str(self.clf), str(self.scaler), width_js, height_js, graph_charge, graph_link_distance, graph_gravity,
            # json.dumps(json_s))
            outfile.write(html.encode("utf-8"))
        # if self.verbose > 0:
        print("\nWrote d3.js graph to '%s'" % path_html)

    def visualize(self, complex, path_html= "mapper_visualization_output.html", title="My Data", graph_link_distance=30,
                  graph_gravity=0.1, graph_charge=-120, custom_tooltips=None, width_html=0, height_html=0,
                  show_tooltips=True, show_title=True, show_meta=True):
        # Turns the dictionary 'complex' in a html file with d3.js

        # print("title.split(_)[1]", title.split("_")[1])
        # title_ = copy.deepcopy(title)

        # Format JSON
        json_s = {}
        json_s["nodes"] = []
        json_s["links"] = []
        k2e = {}  # a key to incremental int dict, used for id's when linking

        for e, k in enumerate(complex["nodes"]):
            # Tooltip formatting
            if custom_tooltips != None:
                tooltip_s = "<h2>Cluster %s</h2>" % k + " ".join([str(f) for f in custom_tooltips[complex["nodes"][k]]])
                if self.color_function == "average_signal_cluster":
                    tooltip_i = int(((sum([f for f in custom_tooltips[complex["nodes"][k]]]) / len(
                        custom_tooltips[complex["nodes"][k]])) * 30))
                    json_s["nodes"].append(
                        {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                         "color": str(tooltip_i)})
                else:
                    # json_s["nodes"].append(
                    #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                    #      "color": str(k.split("_")[0])})

                    kSplitFix_ = self.cover[k].getCoordLimits()[0][0]

                    json_s["nodes"].append(
                        {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                         "color": str(kSplitFix_)})
            else:
                # tooltip_s = "<h2>Cluster %s</h2>Contains %s members." % (k, len(complex["nodes"][k]))
                # json_s["nodes"].append(
                #     {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
                #      "color": str(k.split("_")[0])})

                kSplitFix_ = self.cover[k].getCoordLimits()[0][0]
                tooltip_s = "<h2>Cluster %s</h2>Contains %s members." % (k, len(complex["nodes"][k]))
                json_s["nodes"].append(
                    {"name": str(k), "tooltip": tooltip_s, "group": 2 * int(np.log(len(complex["nodes"][k]))),
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
        <b>Clusterer</b><br>%s<br><br>
        <b>Alpha</b><br>%s<br><br>
        <b>Search Neighborhood</b><br>%s<br><br>
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
            len(self.cover.keys()), False, "distance_origin", complex["meta"], str(self.clusteringAlgo),
            self.expansionRate, self.maxExtend*int(title.split("_")[-1]), width_js, height_js, graph_charge, graph_link_distance, graph_gravity,
            json.dumps(json_s))
            # % (
            # title, width_css, height_css, title_display, meta_display, tooltips_display, title, complex["meta"],
            # self.nr_cubes, self.overlap_perc * 100, self.link_local, self.color_function, complex["meta"],
            # str(self.clf), str(self.scaler), width_js, height_js, graph_charge, graph_link_distance, graph_gravity,
            # json.dumps(json_s))
            outfile.write(html.encode("utf-8"))
        # if self.verbose > 0:
        print("\nWrote d3.js graph to '%s'" % path_html)

    def getComplex(self):

        return self.simplicialComplex



class weightedFiltration(filtration):

    def __init__(self, cover_, maxNumberExp_, maxDimSimplex_, clusteringAlgo_, expansionRate_, maxExtend_,
                 filePrefix_=None, weightedFilePrefix_=None):

        filtration.__init__(self, cover_, maxNumberExp_, maxDimSimplex_, clusteringAlgo_, expansionRate_,
                            maxExtend_, filePrefix_=filePrefix_)

        self.simplexWeightDict = {} # add weight to the intersection of the bins and individual bins #
        # weight of each bin is optimization cost after optimization
        # weight of each intersection is from steinhaus distance as mentioned in the paper
        self.weightedSimplicialComplex = gd.SimplexTree() # It is the complex where any simplex has weight more than cut off #
        self.weightedFilePrefix = weightedFilePrefix_ # Location of directory to store weighted filtration #
        self.maxBinCost = None

    def findMaxBinCost(self):

        maxCost_ = -10000000000.00

        for binIndex_, bin_ in self.cover.items():

            for bin__ in bin_.getExpansionBins():

                binCost_ = bin__.getBinCost()

                if binCost_ > maxCost_:

                    maxCost_ = binCost_

        self.maxBinCost = maxCost_

    def addWeightToSimplicialComplex(self):

        # Add weight to simplicial Complex #

        for sk_value in self.simplicialComplex.get_skeleton(self.maxDimSimplex):

            if len(sk_value[0])>1:

                filter_ = sk_value[1]

                binsPixelList_ = []

                for binIndex_ in sk_value[0]:

                    print("self.cover[binIndex_]", self.cover[binIndex_])

                    list_ = list(self.cover[binIndex_].getExpansionBins()[int(filter_)].getBinPixelDict().keys())

                    binsPixelList_ = binsPixelList_ + list_

                uniqueBinsPixelList_ = list(set(binsPixelList_))

                length1_ = len(binsPixelList_)
                length2_ = len(uniqueBinsPixelList_)
                simplexWeight_ =  1 - (length1_ - length2_) / length1_ # steinhaus distance

                print("sk_value[0]", sk_value[0])

                key_ = sk_value[0]
                key_.sort()
                print("key", key_)

                self.simplexWeightDict.update({tuple(key_): simplexWeight_})

    def weightCutOffSimplicialComplex(self, cutOffWeight_= 0.9, write_visualize=True):

        # It add all the simplices of dimension higher than one #


        for sk_value in self.simplicialComplex.get_skeleton(self.maxDimSimplex):


            if len(sk_value[0]) > 1:

                key_ = sk_value[0]
                key_.sort()
                if self.simplexWeightDict[tuple(key_)] <= cutOffWeight_ :

                    self.weightedSimplicialComplex.insert(sk_value[0], filtration = sk_value[1])

        # Save filtered complexes of the weighted simplicial complex #


        connectGraphTemp_ = defaultdict(list)

        filterSimplices_ = defaultdict(list)

        for sk_value in self.weightedSimplicialComplex.get_skeleton(self.maxDimSimplex):

            if len(sk_value[0]) >= 2:

                filterSimplices_[sk_value[1]].append(sk_value[0])


        for filter_ in range(self.maxNumberExp + 1): # Maximum number of filtrations are self.maxNumberExp + 1 #

            for simplex_ in filterSimplices_[filter_]:

                print("weighted simplex", simplex_)

                for index_, vertex_ in enumerate(simplex_):

                    for vertex__ in simplex_[index_:]:

                        connectGraphTemp_[vertex_].append(vertex__)

                        connectGraphTemp_[vertex__].append(vertex_)


            ######################
            # Save Filter Mapper #
            ######################

            complex_ = self.complexForVisualization(connectGraphTemp_, filter_)

            if write_visualize:
                buf = StringIO()
                buf.write("%s_filter_%d.html" % (self.weightedFilePrefix, int(filter_)))
                fileName__ = buf.getvalue()

                buf = StringIO()
                buf.write("Weighted_Filter_%d" % (int(filter_)))
                titleName__ = buf.getvalue()

                self.visualize_(complex_, path_html= fileName__, title= titleName__)

    def getWeightedPersistence(self):

        simplicialComplex_ = gd.SimplexTree()

        for sk_value in self.weightedSimplicialComplex.get_skeleton(self.maxDimSimplex):
            # This is a fix since Gudhi use diameter for time stamping in filtration

            simplicialComplex_.insert(sk_value[0], filtration=int(2 * sk_value[1]))

        return simplicialComplex_.persistence()


    def getPersistence(self):

        simplicialComplex_ = gd.SimplexTree()

        for sk_value in self.simplicialComplex.get_skeleton(self.maxDimSimplex):

            # This is a fix since Gudhi use diameter for time stamping in filtration

            simplicialComplex_.insert(sk_value[0], filtration = int(2 * sk_value[1]))


        return simplicialComplex_.persistence()
