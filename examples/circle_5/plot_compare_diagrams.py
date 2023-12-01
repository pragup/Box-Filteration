from utils import plot_wasserstein_distance
import matplotlib.pyplot as plt
import numpy as np

filename1 = "../circle_2/output_bf/bfPersistenceDiagram.json"
filename2 = "output_bf/bfPersistenceDiagram.json"
y_name = "BF"
color = "b"
parameters = np.round(np.arange(0.1, 1, 0.1), 1)
plot_wasserstein_distance(plt, filename1, filename2, y_name, color, parameters=parameters, group=1)


filename1 = "../circle_2/output_dtm/dtmPersistenceDiagram.json"
filename2 = "output_dtm/dtmPersistenceDiagram.json"
y_name = "DTM"
color = "g"
parameters = np.round(1 - parameters, 1)
plot_wasserstein_distance(plt, filename1, filename2, y_name, color, parameters=parameters, group=1)

filename1 = "../circle_2/output_vr/vrPersistenceDiagram.json"
filename2 = "output_vr/vrPersistenceDiagram.json"
y_name = "VR"
color = "r"
parameters = []
plot_wasserstein_distance(plt, filename1, filename2, y_name, color, parameters = parameters, group=1)

plt.xlabel("alpha (BF), 1 - m (DTM)")
plt.ylabel("Wasserstein Distance")
plt.legend(loc="upper right", fontsize=8)

plt.savefig("plots/wasserstein_distance.pdf")
plt.show()


