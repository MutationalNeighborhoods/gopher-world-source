## The Maze:
The maze is an 11x11 grid of cells with a starting cell and ending cell. The shortest path algorithm finds the shortest path from the start cell to the end. The user can obstruct cells in the grid, making them impassable. Obstructions might make the puzzle infeasible or increase the length of the shortest path (only if the obstruction lies on what would otherwise be the shortest path). 

## User Controls:
The user should start by pressing "Show True Distances." This will color each grid cell as a function of its distance from the end cell (using the distance formula and not the shortest path algorithm). The cells closer to the end cell will appear hotter (red being the hottest) and those farther from the end will appear cooler (violet being the coolest). 

Then the user should press "Run Shortest Path." The algorithm will find the shortest path and mark its total distance in the top left corner of the screen. If the puzzle is infeasible then the shortest distance will be reported as -1. Otherwise, the shortest distance represents the number of cells traveled where the only possible moves are up, down, left and right. 

The user can press "Show Shortest Path" and the app will highlight the path on the grid in red. Additionally, the travel bar in the top right will show the sequence of colors traveled through when following the shortest path from start to end. Notice that with no obstructions the travel bar looks like a backwards rainbow, starting at violet and ending at red with colors getting strictly warmer between. 

The user can click any cell to fill it in with black and then click it again to return it to its previous shade. A black cell is an obstruction that cannot be part of the shortest path. Alternatively, clicking "Random black cells" after entering a number n where 0 < n < 122 in the input box below the button will fill in a random n cells with black. 

We encourage users to try manually making obstructions to lengthen the shortest path and then using the random black feature. 


