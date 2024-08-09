# Create Property Model

This program generates models, giving the user the choice to either convert an image into a model or create a parallel plane model.

## Key Features

* Generate Property Models from Images
* Generate Parallel Plane Property Models
* Creates Binary File of the Models
* Visualiation of the Models

## Getting Started

Follow these instructions to get a copy of the project and used it at your will.

### Prerequisites

Type the following in terminal to clone the project.

```
$ git clone https://github.com/GISIS-UFF/CreatePropertyModels.git
```

Execute this command to install the required libraries necessary to run the program:

```
$ python3 -m pip install -r requirements.txt
```

## How to use it

To use it, configure the parameters in the `parameters.txt` file.

After configuring, run the `main.py` file by typing in the terminal: 

```
$ python3 main.py
```

### Model Dimentions

The model dimentions(Nx and Nz) are exactly the image dimentions. Example: in an image with the following dimentions

![image_dimentions](https://i.imgur.com/qQeSvcZ.png)

Have these parameters:

```
Nx = 1150 [m]
Nz = 648  [m]
```

### About the Image to Model Area in parameters.txt

Model parameters need to be the same size as the layers in your model. Example: A model with 3 layers needs to have parameters like this:

```
VP_Velocity = [x, y, z]
VS_Velocity = [x, y, z]
Rho_Value   = [x, y, z]
```

* If you turn on the "VS Velocity Approximation" option, you don't need to fill the VS_Velocity array.

### Parameter Priority

Parameter priority is set from top to bottom. Example: a 2-layer VP model with 2000 [m/s] and 4500 [m/s] respectively from top to bottom needs to have parameters like this:

```
VP_Velocity = [2000, 4500]
```

### About Parallel Model Generation

The same logic as explained above applies, but now you need to specify the Interfaces array. You need to fill the array with the depths (in meters) where you want to place a layer. Example: If you need a model of 441x501 and want a layer at 250 meters, then:

```
Interfaces = [250]
```

Another example: If you need a model of 1001x501 and want layers at 250 meters, 400 meters, and 500 meters, then:

```
Interfaces = [250, 400, 500]
```

* Remember, if you have n interfaces, you will have n+1 layers, so your other parameters need to be of size n+1.

## Running the tests

Here's some examples of the code running:

### Salt Model

Original image:

![salt_image](https://i.imgur.com/tQO4n0x.png)

Generated model:

![salt_model](https://i.imgur.com/Uu38uvU.png)

### Parallel Plane Generation

![parallel_plane](https://i.imgur.com/HlTEKAO.png)

### Fault Model

Original image:

![fault_image](https://i.imgur.com/wnOYqPs.png)

Generated model:

![fault_model](https://i.imgur.com/pFfuztO.png)

## Authors

* **Davi Melonio**
