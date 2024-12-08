// Function to roll the selected dice
function rollDice(sides, resultElementId) {
    // Generate a random number between 1 and the number of sides
    let diceRoll = Math.floor(Math.random() * sides) + 1;

    // Update the specific dice result based on the dice type
    document.getElementById(resultElementId).textContent = diceRoll;
}

// Add click event listeners to each result div
document.querySelectorAll('.diceResult').forEach(function(dice) {
    dice.addEventListener('click', function() {
        // Get the number of sides for the clicked result dice (from the ID of the div)
        let sides = dice.getAttribute('data-sides');
        // Call the rollDice function to generate the result
        rollDice(Number(sides), dice.id);
    });
});