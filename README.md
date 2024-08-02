# Create Property Model

These scripts are used to create property models using png or jpeg images.

Quick Tutorial on How to Use This Program:

This program generates models, giving the user the choice to either convert an image into a model or create a parallel plane model.

To use it, configure the parameters in the ../parameters/parameters.txt file.

After configuring, run the main.py file by typing in the terminal: python3 main.py.

> About the Image to Model Area in parameters.txt:

Model parameters need to be the same size as the layers in your model.
Example:
A model with 3 layers needs to have parameters like this:
	VP_Velocity = [x, y, z]
	VS_Velocity = [x, y, z] *
	Rho_Value   = [x, y, z]

* If you turn on the "VS Velocity Approximation" option, you don't need to fill the VS_Velocity array.

> About Parallel Model Generation:

The same logic as explained above applies, but now you need to specify the Interfaces array.
You need to fill the array with the depths (in meters) where you want to place a layer.
Example:
If you need a model of 441x501 and want a layer at 250m, then:
	Interfaces = [250] *

Another example:
If you need a model of 1001x501 and want layers at 250m, 400m, and 500m, then:
	Interfaces = [250, 400, 500] *

* Remember, if you have n interfaces, you will have n+1 layers, so your other parameters need to be of size n+1.