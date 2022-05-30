1.	Inputs Provided
We are provided with a terrain map of size 395*500 (“terrain.png”), text file containing elevation points and another text file having a list of control point values (“red.txt”). The given elevation file (“mpp.txt”) consists of 500 lines of 400 double values of the form (x, y). This is to indicate the sequence of points that we need to visit before reaching the final destination. We have also been given the information about the different types of terrains, the terrain colors and its hex and RGB pixel values.

2.	Output Required
Using the given input values, we need to generate an optimal path from the starting point, in the file containing the control points, to the last point. We also need to plot the final optimal path on the terrain map provided to us by passing through the provided list of points and also calculate the total optimal distance from the initial to the final node.

3.	Basic Idea
In order to obtain the optimal path between two given points we use the A* algorithm in this case. Here we need to compute 3 values, i.e.) 			
h(n) = heuristic function – estimated cost between the current node and destination node
g(n) = cost function – the cost between the source node and current node
f(n) = h(n) + g(n)



We start out by selecting the first 2 nodes from the control points text file. The first point is the starting node. We need to find all the possible neighbors of this node. Once we get all the nodes, we compute the f(n) values for each of the neighboring nodes and select the one that has the lowest value of f(n). We keep repeating this process until we reach the second node. 
We repeat the entire process then to reach till the destination node in the file provided to us.

4.	Assumptions considered
To generate the g(n) and h(n) values we need a terrain modifier value which is multiplied with the euclidean distance. We have hard coded certain values for the terrain modifier based on the type of terrain and the ease of travelling through that terrain.

Open land – 5
Rough meadow – 1.5
Easy movement land – 2.5
Slow run forest – 1.75
Walk forest – 2
Impassable vegetation – 0
Lake – 0 
Paved Road – 5
Footpath – 3 
Out of bounds – 0



Here the values are the highest for Open land and Paved road because the there are no obstacles in such areas and there is no issue with the ease of movement. We can also observe that the terrain modifier is 0 for certain terrains since we cannot cross through these areas.
We use these values of terrain modifier to further compute the h(n) and g(n). Since h(n) is considered to be the best cost, we always take the best possible terrain factor from the assumed list of terrain factors, i.e.) 5.
In order to find the g(n) and h(n) values, we have used the formula,
g(n) = euclidean distance(parent node, current node) * T
h(n) = euclidean distance(current node, destination node) * Tbest
where T = Terrain modifier and Tbest is the best terrain modifier.
Euclidean distance = √ (7.55*(x2 -x1)2) + (10.29*(y2 -y1)2) + (z2 -z1)2)

5.	Calculating the value of h(n) – heuristic function
For each neighbor of the current node, we use the formula for h(n) in order to get the heuristic value. This is used to compute the f(n) value. 
Here while computing the value of h(n) we take into account the best value of the terrain modifier, hence obtaining the best value for the f(n) value. 

6.	Calculating the value of g(n) – cost function
The g(n) value is also computed for each of the neighbor that we consider from the current node. 
We need to ensure that the nodes we are considering are not in an impassable region. If yes, then we do not consider that neighbor of the node.




7.	Python Implementation
We have used certain python in-built libraries such as PIL, numpy, colormap, sys and math.
Global values: Height and width values are considered to be 500 and 395 respectively, which is used in the code. Tbest value is also considered to be a constant value of 5.
Terrain: dictionary containing the hex values of the terrains and the terrain types
TERRAIN_MODIFIER: the constant values considered for cost function calculation.
