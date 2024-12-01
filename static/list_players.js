const playerList = [];

const addPlayer = () => {
    const playerInput = document.getElementById("playerInput");
    const listPlayer = {
        id: Date.now(),
        text: playerInput.value,
    };

    if (listPlayer.text.trim() !== "") {
        playerList.push(listPlayer);
        renderList();
        playerInput.value = "";
    };
};

const removePlayer = (id) => {
    const index = playerList.findIndex(item => item.id === id);
    if (index !== -1) {
        playerList.splice(index, 1);
        renderList();
    }
};

const renderList = () => {
    const playerListContainer = document.getElementById("playerList");
    playerListContainer.innerHTML = "";

    playerList.forEach(item =>{
        const li = document.createElement("li");
        li.textContent = item.text;
        li.setAttribute("class", "inline");

        const buttonContainer = document.createElement("div");
        buttonContainer.classList.add("button-container");

        const deleteButton = document.createElement("button");
        deleteButton.setAttribute("type", "button");
        deleteButton.setAttribute("class", "inline");
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", () => removePlayer(item.id));
        buttonContainer.appendChild(deleteButton);

        li.appendChild(buttonContainer);
        playerListContainer.appendChild(li);

        setTimeout(() => {
            li.classList.add("fade-in");
        }, 10)
    });
};

const submitGame = () => {
    fetch("/STARTGAME", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(playerList),  // Send the list as JSON
    })
}

document.getElementById("addPlayerButton").addEventListener("click", addPlayer);

