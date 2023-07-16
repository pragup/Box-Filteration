from utils import plot_entropy
import numpy as np
import os
import shutil

outputFolder_ = 'plots'

for filename in os.listdir(outputFolder_):
    file_path = os.path.join(outputFolder_, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

params = np.round(np.arange(0.1, 1, 0.1), 1)

y_name = "entropy"
hgroup= 1
plt = plot_entropy(params, y_name, hgroup=hgroup)
filename = "plots/"+ y_name +"_" + "H_" + str(hgroup) + ".pdf"
plt.savefig(filename)
plt.close()

y_name = "max_life_prob"
hgroup= 1
plt = plot_entropy(params, y_name, hgroup=hgroup)
filename = "plots/"+ y_name +"_" + "H_" + str(hgroup) + ".pdf"
plt.savefig(filename)
plt.close()