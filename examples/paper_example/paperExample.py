import matplotlib.pyplot as plt
import pixel_cover as pc
import gudhi as gd
import filtration_tool as ft
import pandas as pd
import os
import shutil

gd.persistence_graphical_tools._gudhi_matplotlib_use_tex=False

outputPlotFolder_ = 'output/'

for filename in os.listdir(outputPlotFolder_):
    file_path = os.path.join(outputPlotFolder_, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



data_ = pd.read_csv('data/paperExample.csv', header= None)
data_ = data_.astype('str').values.tolist()
dataTemp_ = []

for point_ in data_:

    if point_[0] != "nan" and point_[1] != "nan":
      dataTemp_.append([float(point_[0]), float(point_[1])])

print(dataTemp_)

data_ = dataTemp_

###########################################################################
##################### VR vs Box Mapper Filtration #########################
###########################################################################

maxNumberExp_ = 30 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.5 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

################################################################
###################### Box Complex Filtration ##################
################################################################

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__,
                        kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
############################# Weighted Filtration #################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_, clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)

fileName_ = "output/bfPersistence.pdf"
ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

fileName_ = "output/dataPoints.pdf"
pc.draw2DPoints(data_, fileName_, 1, "or")

fileName_ = "output/2dBinDataPlot_filter_5_alpha_"+ str(expansionRate_)+".pdf"
pc.draw2DPartition(binning_.getCover(), 5, fileName_, 2, "b", "or")

fileName_ = "output/2dBinDataPlot_filter_6_alpha_" + str(expansionRate_)+".pdf"
pc.draw2DPartition(binning_.getCover(), 6, fileName_, 3, "b", "or")

fileName_ = "output/2dBinDataPlot_filter_11_alpha_" + str(expansionRate_)+".pdf"
pc.draw2DPartition(binning_.getCover(), 11, fileName_, 4, "b", "or")

fileName_ = "output/2dBinDataPlot_filter_12_alpha_" + str(expansionRate_)+".pdf"
pc.draw2DPartition(binning_.getCover(), 12, fileName_, 4, "b", "or")
