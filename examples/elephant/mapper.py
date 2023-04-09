import numpy as np
import pixel_cover as pc
import filtration_tool as ft
import gudhi as gd
import sklearn.cluster as sc
import time
import os
import shutil

gd.persistence_graphical_tools._gudhi_matplotlib_use_tex=False

########################################################
########### Empty Output Directory #####################
########################################################

outputFilterMapperFolder_ = 'output_bf/filterMapper'

for filename in os.listdir(outputFilterMapperFolder_):
    file_path = os.path.join(outputFilterMapperFolder_, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

outputWeightedFilterMapperFolder_ = 'output_bf/weightedFilterMapper'

for filename in os.listdir(outputWeightedFilterMapperFolder_):
    file_path = os.path.join(outputWeightedFilterMapperFolder_, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

startTime = time.time()

data_ = np.genfromtxt('data/elephant-reference.csv', delimiter=',')
scale_= 100.00 # scale the data since make_circle has values between -1 and 1
dataPoints_ = []

for dataRow_ in data_:

    dataPoints_.append([scale_ * (dataRow_[0] + 1), scale_ * (dataRow_[1] + 1), scale_ * (dataRow_[2] + 1)])

########################################################################
############################# Covering #################################
########################################################################

maxNumberExp_ = 5 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
expansionRate_ = 0.1     # It is \alpha constant in the paper

clusteringAlgo__ = sc.KMeans(init="k-means++", n_clusters=80, n_init=4, random_state=0).fit(dataPoints_)
binning_= pc.pixelCover(maxNumberExp_, maxExtend_, expansionRate_, clusteringAlgo_= clusteringAlgo__,
                        kOptimal_ = 2)
binning_.initial(dataPoints_)
binning_.initialCoverGen(dataPoints_, use_clustering = True)
binning_.initialCoverExpansion()

###################################################################################
############################# Weighted Filtration #################################
###################################################################################

maxDimSimplex_ = 2
cutoffWeight_ = 0
filePrefix_ = "output_bf/filterMapper/mapper"
weightedFilePrefix_ = "output_bf/weightedFilterMapper/mapper"
weightedFilteredComplex_ = ft.weightedFiltration(binning_.getCover(), maxNumberExp_, maxDimSimplex_, clusteringAlgo__,
                                                 expansionRate_, maxExtend_, filePrefix_, weightedFilePrefix_)

weightedFilteredComplex_.initial()
weightedFilteredComplex_.addWeightToSimplicialComplex()
weightedFilteredComplex_.weightCutOffSimplicialComplex()

endTime = time.time()

for sk_value in  weightedFilteredComplex_.getComplex().get_skeleton(maxDimSimplex_):
    print(sk_value)

print("TOTAL RUN TIME in minutes", (endTime - startTime)/60.00)
