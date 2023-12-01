import matplotlib.pyplot as plt
import pixel_cover as pc
import gudhi as gd
from gudhi.dtm_rips_complex import *
import pandas as pd
import os
import shutil
import utils
import json

gd.persistence_graphical_tools._gudhi_matplotlib_use_tex=False

outputFolder_ = 'output_dtm'

for filename in os.listdir(outputFolder_):
    file_path = os.path.join(outputFolder_, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

data_ = pd.read_csv('data/noisyCircleWithCentralCluster.csv')
data_ = data_.astype('str').values.tolist()
dataTemp_ = []

for point_ in data_:

    if point_[0] != "nan" and point_[1] != "nan":
      dataTemp_.append([float(point_[0]), float(point_[1])])


data_ = dataTemp_
fileName_ = "output_dtm/dataPoints.pdf"
pc.draw2DPoints(data_, fileName_, 1, "or")


##########################################################################
######################### DTM Filtration #################################
##########################################################################
persistenceEntropy = {}
persistenceDiagramDict = {}
m = 0.1               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.2               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.3               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()


m = 0.4               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.5               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()


m = 0.6               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.7               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.8               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.9               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.95               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

m = 0.99               # parameter of the DTM
N = len(data_)    # number of points
k = int(m*N)          # parameter of the DTMRipsComplex in gudhi
p = 1
fileName_ = "output_dtm/persistence_with_m_"+str(m)+".pdf"
dtm_rips = gd.dtm_rips_complex.DTMRipsComplex(points=data_, k=k)  # DTM-Filtration in gudhi
st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram
persistenceEntropy.update({str(m):utils.persistence_entropy(diagram_DTM)})
persistenceDiagramDict.update({str(m):utils.homology_group(diagram_DTM)})

# plot the persistence diagram
ax = gd.plot_persistence_diagram(utils.homology_group(diagram_DTM), legend = True)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
ax.set_title("Persistence diagram for dtm with m = " + str(m))
ax.set_aspect("equal")  # forces to be square shaped
plt.savefig(fileName_)
plt.close()

fileName_ = "output_dtm/dtmPersistenceEntropy.json"
with open(fileName_, 'w') as fp:
    json.dump(persistenceEntropy, fp)

fileName_ = "output_dtm/dtmPersistenceDiagram.json"
with open(fileName_, 'w') as fp:
    json.dump(persistenceDiagramDict, fp)
