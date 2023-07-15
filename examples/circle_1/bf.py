import matplotlib.pyplot as plt
import pixel_cover as pc
import gudhi as gd
import filtration_tool as ft
import pandas as pd
import os
import shutil
import utils
import json

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

data_ = pd.read_csv('data/noisyCircle.csv')
data_ = data_.astype('str').values.tolist()
dataTemp_ = []

for point_ in data_:

    if point_[0] != "nan" and point_[1] != "nan":
      dataTemp_.append([float(point_[0]), float(point_[1])])


data_ = dataTemp_
fileName_ = "output_bf/dataPoints.pdf"
pc.draw2DPoints(data_, fileName_, 1, "or")

################################################################
###################### Box Complex Filtration ##################
################################################################
persistenceEntropy={}
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.1 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################### Filtration ####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()


################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.2 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################## Filtration #####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()


################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.3 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################### Filtration ####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.4 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################### Filtration ####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.5 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
#################################### Filtration ###################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.6 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################## Filtration #####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.7 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################## Filtration #####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.8 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################### Filtration ####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()


################################################################
###################### Box Complex Filtration ##################
################################################################
maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.9 # It is \alpha constant in the paper

maxDimSimplex_ = 2
cutoffWeight_ = 0

########################################################################
############################# Covering #################################
########################################################################


clusteringAlgo__ = " No clustering "
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__, kOptimal_ = 2)
binning_.initial(data_)
binning_.initialCoverGen(data_, use_clustering = False)
binning_.initialCoverExpansion()


###################################################################################
################################## Filtration #####################################
###################################################################################

weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_,clusteringAlgo__,
                                                 expansionRate_, maxExtend_)

weightedFilteredComplex_.initial(write_visualize=False)
fileName_ = "output_bf/persistencewith_alpha_" + str(expansionRate_) + ".pdf"
diagram_bf = weightedFilteredComplex_.getPersistence()
persistenceEntropy.update({str(expansionRate_):utils.persistence_entropy(diagram_bf)})

ax = gd.plot_persistence_diagram(utils.homology_group(diagram_bf), legend=True)
ax.set_title("Persistence diagram with alpha = "+ str(expansionRate_))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

fileName_ = "output_bf/bfPersistenceEntropy.json"
with open(fileName_, 'w') as fp:
    json.dump(persistenceEntropy, fp)