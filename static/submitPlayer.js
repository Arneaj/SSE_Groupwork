document.getElementById('submitPlayer').addEventListener('click', () => {
    try {
        var playerName = document.getElementById('playerName').value;
        var playerRace = document.getElementById('playerRace').value;
        var playerClass = document.getElementById('playerClass').value;
        var playerBG = document.getElementById('playerBG').value;
        var playerAlignment = document.getElementById('playerAlignment').value;
        var strength = document.getElementById('ability1').value;
        var dexterity = document.getElementById('ability2').value;
        var constitution = document.getElementById('ability3').value;
        var intelligence = document.getElementById('ability4').value;
        var wisdom = document.getElementById('ability5').value;
        var charisma = document.getElementById('ability6').value;

        fetch(`/save_player`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                characterName: playerName,
                race: playerRace,
                class: playerClass,
                background: playerBG,
                alignment: playerAlignment,
                ability1: strength,
                ability2: dexterity,
                ability3: constitution,
                ability4: intelligence,
                ability5: wisdom,
                ability6: charisma
            })
        })
        
        window.location.href = `/game_creation`;

    } catch (error) {
        console.error('Error:', error);
    }
});
