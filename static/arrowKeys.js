const grid = [];

window.onload = (event) => {
    const cols = document.querySelectorAll(".data");
    let b = "0";
    let temp = []
    for (let i = 0; i < cols.length; i++) {
        if (cols[i].id.split("_")[1] !== b) {
            b = cols[i].id.split("_")[1];
            grid.push(temp);
            temp = [];
        }
        temp.push(cols[i].id);
    }
    grid.push(temp);
};

document.onkeydown = function (event) {
    const current = document.getElementById(document.activeElement.id);
    const text = Number.parseInt(current.getAttribute("data-x"));
    const digit = Number.parseInt(current.getAttribute("data-y"));

    switch (event.key) {
        case "Enter":
            event.preventDefault();
            if (text !== grid[0].length - 1) {
                document.getElementById(grid[digit + 1][text]).focus();
                break;
            }

            break;
        case "ArrowLeft":

            if (text !== 0) {
                document.getElementById(grid[digit][text - 1]).focus();
                break;
            }

            break;

        case "ArrowUp":

            if (digit !== 0) {
                document.getElementById(grid[digit - 1][text]).focus();
                break;
            }

            break;

        case "ArrowRight":
            if (text !== grid[0].length - 1) {
                document.getElementById(grid[digit][text + 1]).focus();
                break;
            }

            break;
        case "ArrowDown":
            if (digit !== grid.length - 1) {
                document.getElementById(grid[digit + 1][text]).focus();
                break;
            }

            break;
    }
};

