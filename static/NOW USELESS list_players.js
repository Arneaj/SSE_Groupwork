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
        removeButton.setAttribute("style", "margin: 5px 0px 5px 50px;")
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



document.getElementById('submitGame').addEventListener('click', () => {
    try {
        var gameName = document.getElementById('gameName').value;

        if (!playerList || !Array.isArray(playerList)) {
            throw new Error('Player list is invalid or undefined');
        }

        // Send a POST request to the Flask function
        const response = fetch(`/process_new_game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gameName: gameName,
                playerList: playerList,
            }),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = response.json();
        const gameId = data.game_id;

        document.getElementById('submitGame').href = `/STARTGAME?game_id=${encodeURIComponent(gameId)}`;

    } catch (error) {
        console.error('Error:', error);
    }
});