# Searching for the shortest route

Searching for the shortest road, which consist of a lot of defined by user cities. The order of vertices are not important, because it checks every combination. This program is based on Travelling Salesman Problem. It is possible to add a lot of cities and find the shortest road, which consists every city. To find distances between cities I used googlemaps library. To use this application, you have to generate your own api key. It is written using GUI kivy. There are three different types of calculating the route based on different algorithms. It is brute force method, which is exact, but it’s really slow for more than 8 vertices. Also, there is again exact algorithm – Held Karp algorithm. It is effective only for 13-15 vertices. The last one is the nearest neighbor algorithm. In most cases this algorithm can’t return the shortest route, but it’s really effective, because it calculates more than 150 vertices in less than few seconds.   

Screenshots:  

![alt text](https://github.com/dpalatynski/salesman/blob/master/salesman_main.png)  
![alt text](https://github.com/dpalatynski/salesman/blob/master/salesman_add_cities.png)  
![alt text](https://github.com/dpalatynski/salesman/blob/master/salesman_results.png)  
