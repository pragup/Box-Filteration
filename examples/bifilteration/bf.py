import matplotlib.pyplot as plt
import numpy as np

import pixel_cover as pc
import gudhi as gd
import filtration_tool as ft
import pandas as pd
import os
import shutil

gd.persistence_graphical_tools._gudhi_matplotlib_use_tex=False

outputFolder_ = 'output_bf'

for filename in os.listdir(outputFolder_):
    file_path = os.path.join(outputFolder_, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

data_ = pd.read_csv('data/points.txt')
data_ = data_.astype('str').values.tolist()
dataTemp_ = []

for point_ in data_:

    if point_[0] != "nan" and point_[1] != "nan":
      dataTemp_.append([float(point_[0]), float(point_[1])])


data_ = dataTemp_
# scale_= 1.00 # scale the data since make_circle has values between -1 and 1
# dataPoints_ = []
#
# for dataRow_ in data_:
#
#     dataPoints_.append([scale_ * (dataRow_[0] + 1), scale_ * (dataRow_[1] + 1)])
# data_ = dataPoints_
fileName_ = "output_bf/dataPoints.pdf"
pc.draw2DPoints(data_, fileName_, 1, "or")

################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 5 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.23 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################

cover_to_centroid_dict = {}
clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 4)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
# print(binning_.getPixelDict())
for key, value in binning_.getCover().items():
    cover_to_centroid_dict.update({key: list(value.getBinPixelDict().keys())[0]})
# print(cover_to_centroid_dict)
binning_.initialCoverExpansion()


###################################################################################
################################### Filtration ####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

##########################
# Plot the triangulation #
##########################
N = len(list(weightedFilteredComplex_.cover.keys()))
points_ = np.zeros((N, 2))
edges_ = []
for sk_value in weightedFilteredComplex_.simplicialComplex.get_skeleton(2):
    print(sk_value, cover_to_centroid_dict[sk_value[0][0]])
    if len(sk_value[0]) == 1:
        points_[sk_value[0][0], :] = np.array(cover_to_centroid_dict[sk_value[0][0]])
    elif len(sk_value[0]) == 2:
        edges_.append(sk_value[0])
        points_[sk_value[0][0], :] = np.array(cover_to_centroid_dict[sk_value[0][0]])
        points_[sk_value[0][1], :] = np.array(cover_to_centroid_dict[sk_value[0][1]])
    else:
        edges_.append([sk_value[0][0], sk_value[0][1]])
        edges_.append([sk_value[0][1], sk_value[0][2]])
        edges_.append([sk_value[0][0], sk_value[0][2]])
        points_[sk_value[0][0], :] = np.array(cover_to_centroid_dict[sk_value[0][0]])
        points_[sk_value[0][1], :] = np.array(cover_to_centroid_dict[sk_value[0][1]])
        points_[sk_value[0][2], :] = np.array(cover_to_centroid_dict[sk_value[0][2]])

for edge_ in edges_:
    plt.plot(points_[edge_, 0], points_[edge_, 1], color="b")
plt.scatter(points_[:, 0], points_[:, 1], marker="o", color="red")

plt.show()
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.2 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# ################################## Filtration #####################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()
#
#
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.3 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# ################################### Filtration ####################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()
#
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.4 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# ################################### Filtration ####################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()
#
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.5 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# #################################### Filtration ###################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()
#
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.6 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# ################################## Filtration #####################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()
#
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.7 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# ################################## Filtration #####################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()
#
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.8 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# ################################### Filtration ####################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()
#
#
# ################################################################
# ###################### Box Complex Filtration ##################
# ################################################################
# maxNumberExp_ = 20 # Maximum number of filterations
# maxExtend_ = 1  # It is \pi in the paper
# expansionRate_ = 0.9 # It is \alpha constant in the paper
#
# maxDimSimplex_ = 2
# cutoffWeight_ = 0
#
# ########################################################################
# ############################# Covering #################################
# ########################################################################
#
#
# clusteringAlgo__ = " No clustering "
# binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
# binning_.initial(data_)
# binning_.initialCoverGen(data_, use_clustering = False)
# binning_.initialCoverExpansion()
#
#
# ###################################################################################
# ################################## Filtration #####################################
# ###################################################################################
#
# weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
#                                                  expansionRate_, maxExtend_)
#
# weightedFilteredComplex_.initial(write_visualize=False)
# fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
# ax = gd.plot_persistence_diagram(weightedFilteredComplex_.getPersistence(), legend=True)
# ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
# ax.set_aspect("equal")  # forces to be square shaped
# plt.savefig(fileName_)
# plt.close()