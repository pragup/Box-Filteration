import matplotlib.pyplot as plt
import pixel_cover as pc
import gudhi as gd
import vr_filteration_tool as vft
import pandas as pd
import os
import shutil
import json
import utils

gd.persistence_graphical_tools._gudhi_matplotlib_use_tex=False

outputFolder_ = 'output_vr'

for filename in os.listdir(outputFolder_):
    file_path = os.path.join(outputFolder_, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

data_ = pd.read_csv('data/thinNoisyCircle_45deg.csv')
data_ = data_.astype('str').values.tolist()
dataTemp_ = []

for point_ in data_:

    if point_[0] != "nan" and point_[1] != "nan":
      dataTemp_.append([float(point_[0]), float(point_[1])])


data_ = dataTemp_
fileName_ = "output_vr/dataPoints.pdf"
pc.draw2DPoints(data_, fileName_, 1, "or")

###########################################################################
############################ VR Filtration ################################
###########################################################################

maxNumberExp_ = 100 # Maximum number of filterations
maxExtend_ = 1  # It is \pi in the paper
maxDimSimplex_ = 2

fileName_ = "output_vr/persistence.pdf"
vrComplex_ = vft.vrFunction(data_, 2 * maxExtend_ * maxNumberExp_, maxDimSimplex_,write_visualize=False)

ax = gd.plot_persistence_diagram(utils.homology_group(vrComplex_.persistence()), legend = True)
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

fileName_ = "output_vr/vrPersistenceEntropy.json"
with open(fileName_, 'w') as fp:
    dict = utils.persistence_entropy(vrComplex_.persistence())
    json.dump(dict, fp)