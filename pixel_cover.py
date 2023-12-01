from collections import defaultdict
import math
import numpy as np
import matplotlib.pyplot as plt
import bin_expansion as be
import sklearn.cluster as sc

class pixel:

    def __init__(self, centroid_, datapoints_):

        self.centroid = centroid_ # It is the centroid of the pixel.
        self.dataPoints = datapoints_ # Points inside the pixel

    def addDataPoint(self, dataPoint_):
        # Currently not using this function #
        self.dataPoints.append(dataPoint_)


    def getDataPoints(self):

        return self.dataPoints

    def getCentroid(self):

        return self.centroid


class bin:

    def __init__(self, coordLimits_, pixelsDict_={}):

        self.coordLimits = coordLimits_ # Coordinate Limits for Hyper-rectangular bin
        self.binPixelsDict = pixelsDict_ # Pixels contained in this bin
        self.expansionBins = [] # It is a list of bins after expansion of current bin. It is empty if we are not
        self.binCost = 0.0 # It is the cost of the bin after expansion (objective function value in linear optimization)
        # , Initial bin have cost zero.

    def setExpansionBins(self, binList_):

        self.expansionBins = binList_
    def setBinCost(self, value_):

        self.binCost = value_
    def getBinCost(self):

        return self.binCost

    def getExpansionBins(self):

        return self.expansionBins

    def getCoordLimits(self):

        return self.coordLimits

    def getBinPixelDict(self):

        return self.binPixelsDict

class pixelCover:

    def __init__(self, maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= sc.DBSCAN(eps=7, min_samples=2),
                 kOptimal_=2):

        self.maxNumberOfExpansion = maxNumberExp_ # Maximum number of expansions of each bin in initial cover
        self.maxExtend = maxExtend_  # Maximum extension of any bin in any direction. Denoted as \pi in the paper.
        # Will be used in linear programming
        self.kOptimal = kOptimal_ # Number of times to run the linear program to get a solution to the largest
        # same as in paper
        self.pixelDict = {}  # It is a dictionary with pixel centroid as key and it contains pixel object
        self.expansionRate = expansionRate_ # Rate we expand the bin. Denoted as \alpha in the paper
        self.cover = {} # It is the cover of the point cloud
        self.clusteringAlgo = clusteringAlgo_ # Clustering algorithm to build initial cover
        self.pointToPixelCentroidDict = {} # Dict that contains pixel for a given point

    def initial(self, dataPoints_):

        self.genPixelDict(dataPoints_)

    def genPixelDict(self, dataPoints_):

        pixelToPointsDict_ = defaultdict(list)
        pointToPixelCentroidDict_ = {}
        for point_ in dataPoints_:

            centroid_ = []
            isIntergerCoord = False

            for coord_ in point_:

                if not coord_.is_integer():

                    coordTemp_ = round(0.5 *(math.floor(coord_) + math.ceil(coord_)), 1)
                    centroid_.append(coordTemp_)

                else:

                    isIntergerCoord = True
                    break

            if isIntergerCoord:
                print("Point has integer coordinate Ignore it")
            else:
                pixelToPointsDict_[tuple(centroid_)].append(point_)
                pointToPixelCentroidDict_.update({tuple(point_) : centroid_})

        self.pointToPixelCentroidDict = pointToPixelCentroidDict_

        for pixelKey_, dataPoints__ in pixelToPointsDict_.items():

            pixelTemp_ = pixel(list(pixelKey_), dataPoints__)

            self.pixelDict.update({pixelKey_: pixelTemp_})

        # print("self.pixelDict", self.pixelDict)

        # for key_, pixel_ in self.pixelDict.items():
        #
        #     print("pixel centroid", key_)
        #     print("pixel datapoints", pixel_.dataPoints)

    def initialCoverGen(self, dataPoints_, use_clustering = False):

        binIndex_ = 0

        if not use_clustering:

            for pixelKey_, pixel_ in self.pixelDict.items():

                coordLimits_ = []

                for centroidCoord_ in list(pixelKey_):

                    coordLimits_.append([round(centroidCoord_ - 0.5, 0), round(centroidCoord_ + 0.5, 0)])

                self.cover.update({binIndex_: bin(coordLimits_, {pixelKey_: pixel_})})

                binIndex_ = binIndex_ + 1

            # print(" Total Number of cover elements", binIndex_)

        else:

            # generate clusters

            clustering_ = self.clusteringAlgo.fit(dataPoints_)

            labelToPoint_ = defaultdict(list)

            for index_, label_ in enumerate(clustering_.labels_):

                labelToPoint_[label_].append(dataPoints_[index_])


            coverCount_ = 0

            for label_, pointList_ in labelToPoint_.items():

                binPixelDict_ = {}

                for point_ in pointList_:

                    centroid_ = []

                    for coord_ in point_:

                        coordTemp_ = round(0.5 * (math.floor(coord_) + math.ceil(coord_)), 1)
                        centroid_.append(coordTemp_)

                    try:

                        pixel_ = self.pixelDict[tuple(centroid_)]
                        pixelKey_ = tuple(centroid_)

                        binPixelDict_.update({pixelKey_: pixel_})

                    except:
                        print(" Warning: It is an integer point ")


                if len(binPixelDict_.keys()) > 0 and label_ != -1 :

                    listTemp_ = list(binPixelDict_.keys())

                    coordLimits_ = [[round(min(idx_) - 0.5, 0), round(max(idx_) + 0.5, 0)]
                                    for idx_ in zip(*listTemp_)] # maximum and minimum value in each direction

                    self.cover.update({coverCount_: bin(coordLimits_, binPixelDict_)})

                    coverCount_ = coverCount_ + 1

                ######### Adding outliers to the cover ###########

                if len(binPixelDict_.keys()) > 0 and label_ == -1:

                    for pixelKey_, pixel_ in binPixelDict_.items():

                        coordLimits_ = []

                        for centroidCoord_ in list(pixelKey_):
                            coordLimits_.append([round(centroidCoord_ - 0.5, 0), round(centroidCoord_ + 0.5, 0)])

                        self.cover.update({coverCount_: bin(coordLimits_, {pixelKey_: pixel_})})

                        coverCount_ = coverCount_ + 1

            # print(" Total Number of cover elements", coverCount_)
            # print("Clustering ON: ", use_clustering)

            n_clusters_ = len(set(clustering_.labels_)) - (1 if -1 in clustering_.labels_ else 0)

            # print("Number of clusters", n_clusters_)

            # print("Number of outliers", coverCount_ - n_clusters_)

    def initialCoverExpansion(self):

        for binIndex_, bin_ in self.cover.items():

            binExpansionTemp_ = be.expansion(bin_, self.maxNumberOfExpansion, self.maxExtend,
                                            self.expansionRate, self.kOptimal)

            binExpansionTemp_.initExpansion(self.pixelDict)

            self.cover[binIndex_].setExpansionBins(binExpansionTemp_.getExpansionBins())

            # print("linearExpansion_.getExpansionBoxes()", binExpansionTemp_.getExpansionBoxes())

            # for bin_ in binExpansionTemp_.getExpansionBins():
            #
            #     print("expanded bin tight CoordLimit", bin_.getCoordLimits())


    def getPixelDict(self):

        return self.pixelDict

    def getCover(self):

        return self.cover

def draw2DPoints(dataPoints_, fileName_, figureIndex_, pointColor_):

    fig_ = plt.figure(figureIndex_)

    plt.margins(0.5)

    for point_ in dataPoints_:

        plt.plot([point_[0]], [point_[1]], pointColor_, markersize=3.00)

    plt.axis('scaled')

    dataPoints_ = np.array(dataPoints_)
    plt.xlim([min(dataPoints_[:, 0])-4, max(dataPoints_[:, 0])+4])
    plt.ylim([min(dataPoints_[:, 1])-4, max(dataPoints_[:, 1])+4])
    fig_.savefig(fileName_, format="pdf", bbox_inches='tight', pad_inches=0.01)
    plt.close(fig_)



def draw2DPartition(cover_, binPositionInCover_, fileName_, figureIndex_, binColor_, pointColor_):

    # binPositionInCOver is position of expansion of each initial bin in the cover

    fig_ = plt.figure(figureIndex_)

    for index_, bin_ in cover_.items():

        bin__ = bin_.getExpansionBins()[binPositionInCover_]

        xCoords_ = bin__.getCoordLimits()[0]
        yCoords_  = bin__.getCoordLimits()[1]

        xList_ = [xCoords_[0], xCoords_[1], xCoords_[1], xCoords_[0], xCoords_[0]]
        yList_ = [yCoords_[0], yCoords_[0], yCoords_[1], yCoords_[1], yCoords_[0]]

        plt.plot(xList_, yList_, binColor_, linewidth=0.5)

        for index__, pixel_ in bin__.getBinPixelDict().items():

            for point_ in pixel_.getDataPoints():

                plt.plot([point_[0]], [point_[1]], pointColor_, markersize=3.00)


    # for point_ in dataPoints_:
    #
    #     plt.plot([point_[0]], [point_[1]], pointColor_, markersize=0.25)

    fig_.savefig(fileName_, format="pdf", bbox_inches='tight', pad_inches=0.01)

    plt.close(fig_)