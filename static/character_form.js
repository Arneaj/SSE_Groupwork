// List of unique numbers
const uniqueNumbers = [8, 10, 12, 13, 14, 15];

// Function to populate the dropdowns with numbers
function populateDropdowns() {
    for (let i = 1; i <= 6; i++) {
        const selectElement = document.getElementById(`ability${i}`);
        
        // Add a default option with no value
        const defaultOption = document.createElement('option');
        defaultOption.value = ''; // No value
        defaultOption.textContent = 'select an ability score'; // Placeholder text
        selectElement.appendChild(defaultOption);
        
        // Add the unique number options
        uniqueNumbers.forEach(number => {
            const option = document.createElement('option');
            option.value = number;
            option.textContent = number;
            selectElement.appendChild(option);
        });
    }
}

// Function to update the dropdowns after a selection is made
function updateDropdowns() {
    const selectedNumbers = [];
    // Collect all selected values from the dropdowns
    for (let i = 1; i <= 6; i++) {
        const selectElement = document.getElementById(`ability${i}`);
        const selectedValue = selectElement.value;
        if (selectedValue !== '') {
            selectedNumbers.push(Number(selectedValue));
        }
    }

    // Update the options in each dropdown
    for (let i = 1; i <= 6; i++) {
        const selectElement = document.getElementById(`ability${i}`);
        const options = selectElement.querySelectorAll('option');

        // Enable and show all options
        options.forEach(option => {
            option.disabled = false;
            option.style.display = 'block';
        });

        // Disable selected numbers in this dropdown
        options.forEach(option => {
            if (selectedNumbers.includes(Number(option.value)) && option.value !== '') {
                option.disabled = true;
                option.style.display = 'none'; // Hide the option
            }
        });
    }
}

// Call the function to populate the dropdowns when the page loads
populateDropdowns();