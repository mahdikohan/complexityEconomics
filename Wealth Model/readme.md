# Wealth Distribution
Sure, let's dive into the code and understand it step by step. The code is written in Python and uses the NetworkX library, which is a powerful tool for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

The first part of the code defines a function called `trade()`. This function takes two arguments: a graph and a number of steps. The purpose of this function is to simulate a series of trades between nodes in the graph. In each step, the function randomly selects an edge (i.e., a pair of connected nodes), and then randomly chooses a direction for the trade. If the node at the start of the trade has a 'wallet' value greater than 0, the function subtracts 1 from this node's 'wallet' and adds 1 to the other node's 'wallet'.

Next, the code initializes an empty list to store the graphs. It then enters a loop that runs 10 times, creating a new graph in each iteration. Each graph is a complete graph with 10 nodes, meaning that every node is connected to every other node. When a node is added to the graph, it is given a 'wallet' attribute with an initial value of 1.

After all the graphs have been created, the code performs a series of trades on each graph. The number of trading steps is set to 10. After the trades have been performed, the code collects the final 'wallet' values from all nodes in all graphs.

Finally, the code uses the matplotlib library to plot a histogram of the 'wallet' values. This gives a visual representation of the distribution of 'wallet' values across all nodes in all graphs after the trades have been performed. The size of each node in the plot is proportional to its 'wallet' value, so nodes with larger 'wallet' values appear larger in the plot.

This code provides a simple but powerful simulation of trading in a network. By adjusting the number of nodes, the number of graphs, and the number of trading steps, you can explore different scenarios and see how the distribution of 'wallet' values changes over time. The use of the NetworkX library makes it easy to create and manipulate the graphs, while the matplotlib library provides a convenient way to visualize the results.

In this figure you can see distribution of wealth which is result of histogram plot of wallets:
<p align="center">
  <img src="https://github.com/mahdikohan/complexityEconomics/blob/main/Wealth%20Model/images/Figure_1.png" alt="wealth distribution" width="600">
</p>
<p align="center">Figure 1: Histogram plot of wallets values in all nodes</p>

You can see each group as a graph in figure 2. I tried to relate graph node sizes with nodes wallet values
<p align="center">
  <img src="[https://github.com/mahdikohan/complexityEconomics/blob/main/Wealth%20Model/images/Figure_1.png](https://github.com/mahdikohan/complexityEconomics/blob/main/Wealth%20Model/images/Members_group_all.png)" alt="groups" width="600">
</p>
<p align="center">Figure 1: Histogram plot of wallets values in all nodes</p>

