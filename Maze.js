let blacks = [];
let reds = [];
let row = [-1, 0, 0, 1];
let col = [0, -1, 1, 0];
let grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
];
let travel_bar = [];

$(".square").on("click", function(event) {
    event.preventDefault();
    var id = $(this).attr('id');
    var coords = id.split("-");
    coords[0] = parseInt(coords[0]);
    coords[1] = parseInt(coords[1]);
    if (blacks.includes(id)) {
        $("#" + id).css("background-color", "rgb(170, 170, 170)");
        blacks = blacks.filter(el => el != id);
        grid[coords[0]][coords[1]] = 1;
    } else {
        $("#" + id).css("background-color", "black");
        blacks.push(id);
        grid[coords[0]][coords[1]] = 0;
    }
})

$("#shortestpath").on("click", function(event) {
    event.preventDefault();
    var shortest_dist = findShortestPath(grid, [0, 0], [10, 10]);
    console.log(shortest_dist);
    $(".shortestdistance").text("Shortest Distance: " + shortest_dist);
})

$("#showpath").on("click", function(event) {
    event.preventDefault();
    for (var i = 0; i < reds.length; i++) {
        travel_bar.push(String($("#" + reds[i]).css("background-color")));
        $("#" + reds[i]).css("background-color", "red");
    }

    var background_color = "";
    for (var i = 0; i < travel_bar.length; i++) {
        if (i === travel_bar.length - 1) {
            background_color += travel_bar[i];
        } else {
            background_color += travel_bar[i] + ", ";
        }
    }
    console.log("linear-gradient(" + background_color + ")");
    $(".travelBar").css("background", "linear-gradient(90deg, " + background_color + ")");
})

$("#showdistances").on("click", function(event) {
    event.preventDefault();
    for (var i = 0; i < 11; i++) {
        for (var j = 0; j < 11; j++) {
            var distance = Math.sqrt((10-i)**2 + (10-j)**2);
            var red = 0;
            var green = 0;
            var blue = 0;

            if (distance <= 2.828) {
                red = 255;
                green = (distance/2.828) * 165;
                blue = 0;
            } else if (distance <= 5.656) {
                red = 255;
                green = 165 + ((distance-2.828)/2.828) * 90;
                blue = 0;
            } else if (distance <= 8.484) {
                red = 255 - ((distance-5.656)/2.828) * 255;
                green = 255 - ((distance-5.656)/2.828) * 127;
                blue = 0;
            } else if (distance <= 11.312) {
                red = 0;
                green = 128 - ((distance-8.484)/2.828) * 128;
                blue = ((distance-8.484)/2.828) * 255;
            } else {
                red = ((distance-11.312)/2.828) * 75;
                green = 0; 
                blue = 255 - ((distance-11.312)/2.828) * 125;
            }

            if (!blacks.includes(i + "-" + j)) {
                $("#" + i + "-" + j).css("background-color", "rgb(" + red + ", " + green + ", " + blue + ")");
            }
        }
    }
})

$("#randomblackout").on("click", function(event) {
    event.preventDefault();
    var random = $("#randomfillin").val();
    
    var i = 0;
    while (i < random) {
        var x = Math.floor(Math.random() * 11);
        var y = Math.floor(Math.random() * 11);
        var id = x.toString() + "-" + y.toString();
        if (!(blacks.includes(x.toString() + "-" + y.toString()))) {
            blacks.push(id);
            $("#" + id).css("background-color", "black");
            grid[x][y] = 0;
            i++;
        }
    }
})

function Queue() {
    this.queue = {};
    this.tail = 0;
    this.head = 0;
}

Queue.prototype.enqueue = function(element) {
    this.queue[this.tail++] = element;
}

Queue.prototype.dequeue = function() {
    if (this.tail === this.head) 
        return undefined

    var element = this.queue[this.head];
    delete element;
    this.head++;
    return element;
}

Queue.prototype.isEmpty = function() {
    return this.tail === this.head;
}

function isValid(mat, visited, row, col) {
    return (row >=0) && (row<mat.length) && (col >= 0) && (col < mat[0].length) && (mat[row][col] == 1) && (!(visited[row][col]));
}

function findShortestPath(mat, src, dest) {
    reds = [] 

    var i = parseInt(src[0]);
    var j = parseInt(src[1]);
    var x = parseInt(dest[0]);
    var y = parseInt(dest[1]);

    if (mat === null || mat.length === 0 || mat[i][j] === 0 || mat[x][y] === 0) {
        return -1;
    }

    var M = mat.length;
    var N = mat[0].length;
    var visited = [];
    for (var w = 0; w < M; w++) {
        visited[w] = [];
        for (var v = 0; v < N; v++) { 
            visited[w][v] = false;
        }
    }

    var q = new Queue();
    var b = new Queue();
    visited[i][j] = true;
    q.enqueue([i, j, 0]);

    var min_dist = Infinity;
    var last_dist = 0;

    var prev = [i, j, 0];
    while (!q.isEmpty()) {
        var node = q.dequeue();
        console.log(node);
        
        i = node[0];
        j = node[1];
        var dist = node[2];
        if (dist > last_dist) {
            last_dist = dist;
            b.enqueue(prev);
        }

        prev = node;

        if (i === x && j === y) {
            min_dist = dist;
            break;
        }

        for (var k = 0; k < 4; k++) {
            if (isValid(mat, visited, i + row[k], j + col[k])) {
                visited[i+row[k]][j+col[k]] = true;
                q.enqueue([i+row[k], j+col[k], dist+1]);
            }
        }
    }

    while (!b.isEmpty()) {
        var node = b.dequeue();
        reds.push(node[0].toString() + "-" + node[1].toString())
    }

    if (min_dist != Infinity) {
        return min_dist;
    }
    return -1;
}

