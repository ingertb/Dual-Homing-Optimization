# Dual Homing Optimization

The aim of this problem was to optimize fps for GPU with use of dual-homing. We take a minimal level of fps as 30 and we look for minimal cost. Also optimize the number of servers and their position. We include the cost as infrastructure and data transfer.

The problem was solved by presenting two solutions:

- one in the form of an exact solution using a software GMPL (CBC/CLP) and the appropriate mathematical model.  

- The second method was presented in language python using the library Networkx. At the same time this code in python helped us to generate random  networks for the testing scenario, also it gave us the possibility of drawing the results with the python library ‘matplotlib’.
