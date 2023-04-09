import numpy as np
import itertools
import math
import copy
import pixel_cover as pc
from scipy.optimize import linprog
import cplex
from cplex.exceptions import CplexError
import sys
import time

class expansion:

    def __init__(self, bin_, maxNumbExp_, maxExtension_, expansionRate_, kOptimal_):

        self.maxNumberOfExpansion = maxNumbExp_ # maximum number of expansion of  the bin
        self.targetBin = bin_ # bin we want to expand.
        self.kOptimal = kOptimal_ # k number of iterations at each expansion step of linear program.
        # To find a solution close to largest optimal
        self.maxExtension = maxExtension_ # it is maximum expansion in a given direction .
        self.expansionBoxes = [self.targetBin.getCoordLimits()] # expansion box is size of the box in
        # which target bin is allowed to expand.
        self.expansionRate = expansionRate_ # Rate at which target bin should expand. It has value between 0 and 1
        self.expansionBins = [self.targetBin] # Bins after expanding using linear optimization models I and II.
        self.dataDim = len(bin_.getCoordLimits()) # Dimension of the data.

    def initExpansion(self, pixelDict_):

        self.genExpansionBoxes() # it will generate the list of neighborhood I am growing the balls [B(x, pi*j)] 0<j<maximum extension #
        self.genExpansionBins(pixelDict_) # it will generate the optimal bin expansion list based on the neighborhood list generated by #
        # genExpansionBoxes() #

    def genExpansionBoxes(self):

        boxTemp_ = self.targetBin.getCoordLimits()

        extendTemp_ = self.maxExtension

        for expNumber_ in range(self.maxNumberOfExpansion):

            boxTemp__ = []

            for coordLimit_ in boxTemp_:

                lowCoord_ = int(round(coordLimit_[0] - expNumber_ * extendTemp_))

                highCoord_ = int(round(coordLimit_[1] + expNumber_ * extendTemp_))

                newWidthTemp_ = [lowCoord_, highCoord_]

                boxTemp__.append(newWidthTemp_)


            self.expansionBoxes.append(boxTemp__)


    def genExpansionBins(self, pixelDict_):


        for index_ in range(len(self.expansionBoxes)):

            if index_ >= 1:

                oldBinTemp_ = self.expansionBins[index_ - 1] # Initial Bin used for the expansion #
                binWeWillAdd_ = None

                isInitialStep_ = True

                for index__ in range(self.kOptimal):


                    [newBinTemp_, newObjectiveCost_] = self.genNewBin(oldBinTemp_, self.expansionBoxes[index_], pixelDict_,
                                             isInitialStep_)
                    print("To Get solution close to largest optimal, we applied ", index__, "steps of optimization")

                    ### If new bin and  bin from previous step are  same  or last step then add new bin as expanded bin ###

                    if index__ > 0:

                        print("old objective Cost", oldObjectiveCost_)
                        print("new objective Cost", newObjectiveCost_)

                        print("oldBinTemp_", oldBinTemp_.getCoordLimits(), "newBinTemp_",
                              newBinTemp_.getCoordLimits())

                        if oldObjectiveCost_ < newObjectiveCost_:

                            binWeWillAdd_ = oldBinTemp_
                            break

                        else:

                            binWeWillAdd_ = newBinTemp_

                    else:

                        binWeWillAdd_ = newBinTemp_


                    oldBinTemp_ = newBinTemp_
                    oldObjectiveCost_ = newObjectiveCost_
                    isInitialStep_ = False


                self.expansionBins.append(binWeWillAdd_)

    def isSameBin(self, bin_, bin__):

        isSameBin_ = True

        for index_, coordLimit_ in enumerate(bin_):

            if coordLimit_[0]!= bin__[index_][0] or \
                    coordLimit_[1] != bin__[index_][1]:

                isSameBin_ = False

                break

        return isSameBin_




    def genNewBin(self, oldBin_, inputBox_, pixelDict_, isInitialStep_):

        coordIntervalsToCheck_ = []

        for index_, coordLimits_ in enumerate(inputBox_):

            ithCoordIntervalToCheck_ = []
            ithCoordIntervalToCheck_.append([coordLimits_[0], oldBin_.getCoordLimits()[index_][0]])
            ithCoordIntervalToCheck_.append([oldBin_.getCoordLimits()[index_][1], coordLimits_[1]])
            coordIntervalsToCheck_.append(ithCoordIntervalToCheck_)

        possibleNewFilledPixelsToPointDict_ = {}

        for pixelKey_, pixel_ in pixelDict_.items():

            isInCoordIntervals_ = False

            isInInputBox_ = True

            centroid_ = list(pixelKey_)

            for index_, coordLimits_ in enumerate(inputBox_):

                if centroid_[index_] > coordLimits_[1] or \
                        centroid_[index_] < coordLimits_[0]:

                    isInInputBox_ = False

                    break

            if isInInputBox_:

                for index_, coordIntervals_ in enumerate(coordIntervalsToCheck_):

                    for coordInterval_ in coordIntervals_:

                        if centroid_[index_] >= coordInterval_[0] and \
                            centroid_[index_] <= coordInterval_[1]:

                            isInCoordIntervals_ = True

                            break

            if isInCoordIntervals_:

                possibleNewFilledPixelsToPointDict_.update({pixelKey_: pixel_.getDataPoints()})


        print("possibleNewFilledPixelsToPointDict_", possibleNewFilledPixelsToPointDict_)


        newBin_, objectiveCost_ = self.modelConstrainAndSolveScipy(oldBin_, possibleNewFilledPixelsToPointDict_, pixelDict_, isInitialStep_)

        return [newBin_, objectiveCost_]

    # def modelConstrainAndSolveCplex(self, oldBin_, possibleNewFilledPixelsToPointDict_, pixelDict_, isInitialStep_):
    #
    #     # Ax less than or greater than equal to b
    #
    #     possibleNewFilledPixels_ = list(possibleNewFilledPixelsToPointDict_.keys())
    #
    #     numberOfVariables_ = 2 * self.dataDim + len(possibleNewFilledPixels_)  # Total number of variable in model
    #
    #     constrain ={"obj": [], "lb": [], "ub": None, "A": [], "b": [], "sense": []}
    #
    #     problem = cplex.Cplex()
    #     problem.objective.set_sense(problem.objective.sense.minimize)
    #
    #     # Objective Function
    #
    #     #pixelCost_ = lambda x : abs(math.exp(-(x - 1)) - 1) + 1
    #
    #     constrain["obj"] = np.zeros(numberOfVariables_)
    #
    #     for index_ in range(2 * self.dataDim):
    #
    #         if index_%2 == 0:
    #
    #             constrain["obj"][index_] = -(1 - self.expansionRate)
    #
    #         else:
    #
    #             constrain["obj"][index_] = (1 - self.expansionRate)
    #
    #     for index_, pixel_ in enumerate(possibleNewFilledPixels_):
    #
    #         index__ = index_ + 2 * self.dataDim
    #
    #         numberofPoints_ = len(possibleNewFilledPixelsToPointDict_[pixel_])
    #         # print("number of points in pixel", numberofPoints_)
    #         # print("pixel cost", pixelCost_(numberofPoints_))
    #
    #         #variableCost_ = -self.expansionRate * pixelCost_(numberofPoints_)
    #
    #         variableCost_ = -self.expansionRate * numberofPoints_
    #
    #         # print("variable cost", variableCost_)
    #         constrain["obj"][index__] = variableCost_
    #
    #     print("Objective Cofficient", constrain["obj"])
    #
    #     # Set Lower bounds of the variables #
    #     constrain["lb"] = [-cplex.infinity for index_ in range(numberOfVariables_)]
    #
    #
    #     problem.variables.add(obj=constrain["obj"], lb=constrain["lb"])
    #
    #     #print("problem.variables.get_lower_bounds()", problem.variables.get_lower_bounds())
    #     #print("problem.variables.get_upper_bounds()", problem.variables.get_upper_bounds())
    #
    #     #####################################################################################
    #     # Constrain Type 1
    #
    #     indexTemp_ = 0
    #
    #     totalWidth_ = 0
    #
    #     print("oldBin_.getCoordLimits() in constrain", oldBin_.getCoordLimits())
    #
    #     for coordLimit_ in oldBin_.getCoordLimits():
    #
    #         constrain["A"].append(cplex.SparsePair(ind=[indexTemp_], val=[1]))
    #         constrain["sense"].append("L")
    #         constrain["b"].append(coordLimit_[0])
    #
    #         indexTemp_ = indexTemp_  + 1
    #
    #         constrain["A"].append(cplex.SparsePair(ind=[indexTemp_], val=[1]))
    #         constrain["sense"].append("G")
    #         constrain["b"].append(coordLimit_[1])
    #
    #         indexTemp_ =  indexTemp_ + 1
    #
    #         totalWidth_ = totalWidth_ + coordLimit_[1] - coordLimit_[0]
    #
    #
    #     #########################################################################################
    #     # Constrain Type 2
    #
    #     for index_, pixel_ in enumerate(possibleNewFilledPixels_):
    #
    #         index__ = index_ + 2 * self.dataDim
    #
    #         for index___ in range(self.dataDim):
    #             sparseIndices_ = []
    #             sparseValues_ = []
    #             sparseIndices_.append(2 * index___)
    #             sparseValues_.append(1)
    #             sparseIndices_.append(index__)
    #             sparseValues_.append(1)
    #             constrain["A"].append(cplex.SparsePair(ind=sparseIndices_, val=sparseValues_))
    #             constrain["sense"].append("L")
    #             constrain["b"].append(pixel_[index___])
    #
    #
    #             sparseIndices_ = []
    #             sparseValues_ = []
    #             sparseIndices_.append(2 * index___ + 1)
    #             sparseValues_.append(-1)
    #             sparseIndices_.append(index__)
    #             sparseValues_.append(1)
    #             constrain["A"].append(cplex.SparsePair(ind=sparseIndices_, val=sparseValues_))
    #             constrain["sense"].append("L")
    #             constrain["b"].append(-pixel_[index___])
    #
    #         sparseIndices_ = []
    #         sparseValues_ = []
    #         sparseIndices_.append(index__)
    #         sparseValues_.append(1)
    #
    #         constrain["A"].append(cplex.SparsePair(ind=sparseIndices_, val=sparseValues_))
    #         constrain["sense"].append("L")
    #         constrain["b"].append(0.5)
    #
    #     ###################################################################################
    #
    #     # Constrains of Type 3
    #     # These constrains are added to find solution close to largest optimal solution #
    #
    #     if not isInitialStep_:
    #
    #         sparseValues_ = []
    #         sparseIndices_ = []# list(np.arange(2 * self.dataDim))
    #
    #         for index_ in range(2 * self.dataDim):
    #
    #             sparseIndices_.append(index_)
    #
    #             if index_%2 == 0:
    #
    #                 sparseValues_.append(-1)
    #
    #             else:
    #
    #                 sparseValues_.append(1)
    #
    #         constrain["A"].append(cplex.SparsePair(ind=sparseIndices_, val=sparseValues_))
    #         constrain["sense"].append("G")
    #         constrain["b"].append(totalWidth_ + 1)
    #
    #     ##############################################################################################################
    #
    #     problem.linear_constraints.add(lin_expr=constrain["A"], senses=constrain["sense"], rhs=constrain["b"])
    #
    #     print(" Started solving linear optimization ")
    #     t0 = time.clock();
    #     # Solve the problem
    #     problem.solve()
    #     # problem.register_callback(SolveCallback)
    #     t1 = time.clock();
    #
    #     print("Time taken to solve the problem", t1 - t0)
    #
    #     output = {"X": problem.solution.get_values(), "obj": problem.solution.get_objective_value(),
    #               "time_taken": t1 - t0}
    #
    #     print("possibleNewFilledPixels_ in constrain", possibleNewFilledPixels_)
    #     print("output of linear program", output["X"])
    #     print("Objective Value", output["obj"])
    #
    #     # Write a new bin and return it.
    #
    #     newBinCoordLimitTemp_ = []
    #
    #     # numericalError_ = 0.1
    #
    #     for index_ in range(self.dataDim):
    #
    #         index__ = 2 * index_
    #
    #         # We will use xsi_3 for rounding off for the optimal of the bin #
    #
    #         if output["X"][index__] % 1 >= 0.5 :
    #             l_ = math.ceil(output["X"][index__])
    #         else:
    #             l_ = math.floor(output["X"][index__])
    #
    #
    #         if output["X"][index__ + 1] % 1 >= 0.5 :
    #             u_ = math.ceil(output["X"][index__ + 1])
    #         else:
    #             u_ = math.floor(output["X"][index__+ 1])
    #
    #
    #         newBinCoordLimitTemp_.append([l_, u_])
    #
    #
    #     newBinPixelDict_ = copy.deepcopy(oldBin_.getBinPixelDict())
    #
    #     print(" possible Filled Pixel list ", possibleNewFilledPixels_)
    #
    #     for index_ in range(2 * self.dataDim, numberOfVariables_):
    #
    #         #if abs(output["X"][index_] - 0.5) <= 0.10:
    #
    #         if abs(output["X"][index_]) >= 0.000010:
    #             index__ = index_ - 2 * self.dataDim
    #
    #             # print (" index__ for pixel variable", index__)
    #             #
    #             # print(" new pixel in bin ", possibleNewFilledPixels_[index__])
    #
    #
    #             newBinPixelDict_.update({tuple(possibleNewFilledPixels_[index__]):\
    #                                          pixelDict_[tuple(possibleNewFilledPixels_[index__])]})
    #
    #
    #     newBin_ = pc.bin(newBinCoordLimitTemp_, newBinPixelDict_)
    #
    #
    #     newBin_.setBinCost(output["obj"]) # Add cost of Each Bin after linear optimization #
    #
    #     return [newBin_, output["obj"]]


    def modelConstrainAndSolveScipy(self, oldBin_, possibleNewFilledPixelsToPointDict_, pixelDict_, isInitialStep_):

        # Ax less than or greater than equal to b

        possibleNewFilledPixels_ = list(possibleNewFilledPixelsToPointDict_.keys())

        numberOfVariables_ = 2 * self.dataDim + len(possibleNewFilledPixels_)  # Total number of variable in model

        constrain ={"obj": [], "bound":[], "A": [], "b": [], "sense": []}

        # problem = cplex.Cplex()
        # problem.objective.set_sense(problem.objective.sense.minimize)

        # Objective Function

        #pixelCost_ = lambda x : abs(math.exp(-(x - 1)) - 1) + 1

        constrain["obj"] = np.zeros(numberOfVariables_)

        for index_ in range(2 * self.dataDim):

            if index_%2 == 0:

                constrain["obj"][index_] = -(1 - self.expansionRate)

            else:

                constrain["obj"][index_] = (1 - self.expansionRate)

        for index_, pixel_ in enumerate(possibleNewFilledPixels_):

            index__ = index_ + 2 * self.dataDim
            numberofPoints_ = len(possibleNewFilledPixelsToPointDict_[pixel_])

            # print("number of points in pixel", numberofPoints_)
            # print("pixel cost", pixelCost_(numberofPoints_))
            #variableCost_ = -self.expansionRate * pixelCost_(numberofPoints_)

            variableCost_ = -self.expansionRate * numberofPoints_

            # print("variable cost", variableCost_)
            constrain["obj"][index__] = variableCost_

        print("Objective Cofficient", constrain["obj"])

        # Set Lower bounds of the variables #
        constrain["bound"] = [(-math.inf, math.inf) for index_ in range(numberOfVariables_)]


        #problem.variables.add(obj=constrain["obj"], lb=constrain["lb"])
        #print("problem.variables.get_lower_bounds()", problem.variables.get_lower_bounds())
        #print("problem.variables.get_upper_bounds()", problem.variables.get_upper_bounds())

        #####################################################################################
        #                            Constrain Type 1                                       #
        #####################################################################################
        indexTemp_ = 0
        totalWidth_ = 0

        print("oldBin_.getCoordLimits() in constrain", oldBin_.getCoordLimits())

        for coordLimit_ in oldBin_.getCoordLimits():

            ARowTemp_ = np.zeros(numberOfVariables_)
            ARowTemp_[indexTemp_] = 1
            constrain["A"].append(ARowTemp_)
            constrain["sense"].append("L")
            constrain["b"].append(coordLimit_[0])

            indexTemp_ = indexTemp_  + 1
            ARowTemp_ = np.zeros(numberOfVariables_)
            ARowTemp_[indexTemp_] = -1
            constrain["A"].append(ARowTemp_)
            constrain["sense"].append("L")
            constrain["b"].append(-coordLimit_[1])

            indexTemp_ =  indexTemp_ + 1
            totalWidth_ = totalWidth_ + coordLimit_[1] - coordLimit_[0]


        #########################################################################################
        #                               Constrain Type 2                                        #
        #########################################################################################

        for index_, pixel_ in enumerate(possibleNewFilledPixels_):

            index__ = index_ + 2 * self.dataDim

            for index___ in range(self.dataDim):

                ARowTemp_ = np.zeros(numberOfVariables_)
                ARowTemp_[2 * index___] = 1
                ARowTemp_[index__] = 1
                constrain["A"].append(ARowTemp_)
                constrain["sense"].append("L")
                constrain["b"].append(pixel_[index___])

                ARowTemp_ = np.zeros(numberOfVariables_)
                ARowTemp_[2 * index___ + 1] = -1
                ARowTemp_[index__] = 1
                constrain["A"].append(ARowTemp_)
                constrain["sense"].append("L")
                constrain["b"].append(-pixel_[index___])


            ARowTemp_ = np.zeros(numberOfVariables_)
            ARowTemp_[index__] = 1
            constrain["A"].append(ARowTemp_)
            constrain["sense"].append("L")
            constrain["b"].append(0.5)

        ###################################################################################
        #                           Constrains of Type 3                                  #
        # These constrains are added to find solution close to largest optimal solution   #

        if not isInitialStep_:

            ARowTemp_ = np.zeros(numberOfVariables_)

            for index_ in range(2 * self.dataDim):

                if index_%2 == 0:

                    ARowTemp_[index_] = -1

                else:

                    ARowTemp_[index_] = 1


            constrain["A"].append(ARowTemp_)
            constrain["sense"].append("G")
            constrain["b"].append(totalWidth_ + 1)

        ##############################################################################################################

        print(" Started solving linear optimization ")
        t0 = time.clock();
        # Solve the problem

        opt = linprog(c=constrain["obj"], A_ub=constrain["A"], b_ub=constrain["b"], bounds = constrain["bound"],
                      method = "interior-point")

        t1 = time.clock();

        print("Time taken to solve the problem", t1 - t0)

        output = {"X": opt.x, "obj": opt.fun, "time_taken": t1 - t0}

        print("possibleNewFilledPixels_ in constrain", possibleNewFilledPixels_)
        print("output of linear program", output["X"])
        print("Objective Value", output["obj"])

        # Write a new bin and return it.

        newBinCoordLimitTemp_ = []

        # numericalError_ = 0.1

        for index_ in range(self.dataDim):

            index__ = 2 * index_

            # We will use xsi_3 for rounding off for the optimal of the bin #

            if output["X"][index__] % 1 >= 0.5 :
                l_ = math.ceil(output["X"][index__])
            else:
                l_ = math.floor(output["X"][index__])


            if output["X"][index__ + 1] % 1 >= 0.5 :
                u_ = math.ceil(output["X"][index__ + 1])
            else:
                u_ = math.floor(output["X"][index__+ 1])


            newBinCoordLimitTemp_.append([l_, u_])


        newBinPixelDict_ = copy.deepcopy(oldBin_.getBinPixelDict())

        print(" possible Filled Pixel list ", possibleNewFilledPixels_)

        for index_ in range(2 * self.dataDim, numberOfVariables_):

            #if abs(output["X"][index_] - 0.5) <= 0.10:

            if abs(output["X"][index_]) >= 0.000010:
                index__ = index_ - 2 * self.dataDim

                # print (" index__ for pixel variable", index__)
                #
                # print(" new pixel in bin ", possibleNewFilledPixels_[index__])


                newBinPixelDict_.update({tuple(possibleNewFilledPixels_[index__]):\
                                             pixelDict_[tuple(possibleNewFilledPixels_[index__])]})


        newBin_ = pc.bin(newBinCoordLimitTemp_, newBinPixelDict_)


        newBin_.setBinCost(output["obj"]) # Add cost of Each Bin after linear optimization #

        return [newBin_, output["obj"]]

    def genAllPixels(self, pixelCentroidCoordList_):

        pixelCentroidList_ = list(itertools.product(pixelCentroidCoordList_[0]))

        for index_ in range(len(pixelCentroidCoordList_)):

            if index_ < len(pixelCentroidCoordList_) - 1:

                pixelCentroidList_ = list(itertools.product(pixelCentroidList_, pixelCentroidCoordList_[index_ + 1]))
                pixelCentroidList_ = [tuple(list(x[0]) + [x[1]]) for x in pixelCentroidList_]

        pixelCentroidList_ = [list(x) for x in pixelCentroidList_]

        return pixelCentroidList_

    def getExpansionBins(self):

        return self.expansionBins

    def getExpansionBoxes(self):

        return self.expansionBoxes

