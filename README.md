# Box-Filteration #
Topolgical data analysis is used for complex data analysis. In general, we grow balls to understand topology of point cloud. We came up with a new technique where 
instead of growing balls we grow hypercubes with directional control over its expansion. 
# Installation #
1. conda env create --prefix ./env -f .\environment.yml
2. conda activate ./env
3. Run the scripts in each of the examples
## Box Cover ##
Following example shows a toy problem of 3 points to demonstrate expansion of boxes and their corresponding nerves. 
For details checkout **examples/paper_example**.

<img src="images/paperExample/alpha_0d6/2dBinDataPlot_filter_5_alpha_0d6.JPG" width="22%" height="22%" title="cover"/> <img src="images/paperExample/alpha_0d6/2dBinDataPlot_filter_6_alpha_0d6.JPG" width="22%" height="22%" title="cover"/> <img src="images/paperExample/alpha_0d6/2dBinDataPlot_filter_11_alpha_0d6.JPG" width="22%" height="22%" title="cover"/> <img src="images/paperExample/alpha_0d6/2dBinDataPlot_filter_12_alpha_0d6.JPG" width="22%" height="22%" title="cover"/> <br />
<img src="images/paperExample/alpha_0d6/nerve_5.JPG" width="22%" title="nerve_5"/> <img src="images/paperExample/alpha_0d6/nerve_6.JPG" width="22%" title="nerve_6"/> <img src="images/paperExample/alpha_0d6/nerve_11.JPG" width="22%" title="nerve_11"/> <img src="images/paperExample/alpha_0d6/nerve_12.JPG" width="22%" title="nerve_12"/> <br />

## Persistence ##
Persistence diagram for box filteration with various values of parameter alpha = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] for a given 2d point cloud. For details checkout **examples/circle_2**. Other examples 
with various data distribution of circles are shown in **examples/circle_1,examples/circle_3, examples/circle_4**.  


<img src="images/circle/circle.JPG" width="22%" title="circle"/> <img src="images/circle/circle_alpha_0.1.JPG" width="22%" title="alpha_0d1"/> <img src="images/circle/circle_alpha_0.2.JPG" width="22%" title="alpha_0d2"/> <img src="images/circle/circle_alpha_0.3.JPG" width="22%" title="alpha_0d3"/> <img src="images/circle/circle_alpha_0.4.JPG" width="22%" title="alpha_0d4"/> <img src="images/circle/circle_alpha_0.5.JPG" width="22%" title="alpha_0d5"/> <img src="images/circle/circle_alpha_0.6.JPG" width="22%" title="alpha_0d6"/> <img src="images/circle/circle_alpha_0.7.JPG" width="22%" title="alpha_0d7"/> <img src="images/circle/circle_alpha_0.8.JPG" width="22%" title="alpha_0d8"/> <img src="images/circle/circle_alpha_0.9.JPG" width="22%" title="alpha_0d9"/> <br />

## Mapper ##
Implemntation of mapper for various data distribution is shown down below. For details check out **examples/flamingo, examples/elephant, examples/lion, examples/cat, examples/camel, examples/horse**.
Mapper images down below are linked to their detailed *html* file.     
<img src="images/animals/catPointCloud.JPG" width="25%" height="25%" title="cat"/> [<img src="images/animals/catMapper.jpg" width="20.5%" title="mapper"/>](https://pragup.github.io/Box-Filteration/examples/cat/output_bf/filterMapper/mapper_filter_3) <img src="images/animals/lionPointCloud.JPG" width="25%" height="25%" title="lion"/> [<img src="images/animals/lionMapper.jpg" width="17.0%" title="mapper"/>](https://pragup.github.io/Box-Filteration/examples/lion/output_bf/filterMapper/mapper_filter_3) <br />
<img src="images/animals/flamingoPointCloud.JPG" width="25%" height="25%" title="flamingo"/> [<img src="images/animals/flamingoMapper.jpg" width="20.5%" title="mapper"/>](https://pragup.github.io/Box-Filteration/examples/flamingo/output_bf/filterMapper/mapper_filter_3) <img src="images/animals/horsePointCloud.JPG" width="25%" height="25%" title="horse"/> [<img src="images/animals/horseMapper.jpg" width="17.0%" title="mapper"/>](https://pragup.github.io/Box-Filteration/examples/horse/output_bf/filterMapper/mapper_filter_3) <br />
<img src="images/animals/elephantPointCloud.JPG" width="25%" height="25%" title="elephant"/> [<img src="images/animals/elephantMapper.jpg" width="20.5%" title="mapper"/>](https://pragup.github.io/Box-Filteration/examples/elephant/output_bf/filterMapper/mapper_filter_3) <img src="images/animals/camelPointCloud.JPG" width="25%" height="25%" title="camel"/> [<img src="images/animals/camelMapper.jpg" width="17.0%" title="mapper"/>](https://pragup.github.io/Box-Filteration/examples/camel/output_bf/filterMapper/mapper_filter_3) <br />