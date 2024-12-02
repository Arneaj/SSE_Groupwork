// Array to store players
const playerList = [];
            
// Function to add player selected to list
function getPlayer() {
    // Get value of selected input
    const selectElement = document.querySelector('#select1');
    const selectedValue = selectElement.options[selectElement.selectedIndex].value;

    // Check if the selected value is already in the list
    if (!playerList.includes(selectedValue)) {
        playerList.push(selectedValue);
        renderPlayerList();
    }
}

// Function to remove player from the list
function removePlayer(player) {
    // Find the index of the player in the array
    const index = playerList.indexOf(player);
    if (index !== -1) {
        // Remove the player from the array
        playerList.splice(index, 1);
        renderPlayerList();
    }
}

// Function to render the player list
function renderPlayerList() {
    const playerListContainer = document.querySelector('#playerListContainer');
    playerListContainer.innerHTML = "";

    // Loop through the playerList and create a <li> for each item
    playerList.forEach(item => {
        const li = document.createElement("li");

        // Add the item text to the <li>
        li.textContent = item;

        // Create a "Remove player" button
        const removeButton = document.createElement("button");
        removeButton.setAttribute("type", "button")
        removeButton.textContent = "Remove";
        removeButton.onclick = function () {
            removePlayer(item);
        };

        // Append the remove button to the <li>
        li.appendChild(removeButton);

        // Append the <li> to the list container
        playerListContainer.appendChild(li);
    });
}