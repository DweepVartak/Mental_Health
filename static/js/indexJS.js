
        document.getElementById('education').addEventListener('change', function() {
            toggleOtherInput(this, 'other-education');
        });
    
        document.getElementById('occupation').addEventListener('change', function() {
            toggleOtherInput(this, 'other-occu');
        });

        document.getElementById('history-trauma-abuse').addEventListener('change', function() {
            toggleOtherInput(this, 'other-history');
        });

        document.getElementById('personal-history').addEventListener('change', function() {
            toggleOtherInput(this, 'other-perhistory');
        });

        document.getElementById('family-history').addEventListener('change', function() {
            toggleOtherInput(this, 'other-famhistory');
        });

        document.getElementById('ethnicity').addEventListener('change', function() {
            toggleOtherInput(this, 'other-ethnicity');
        });
    
        function toggleOtherInput(selectElement, inputDivId) {
            var selectedOption = selectElement.value;
            var otherInputDiv = document.getElementById(inputDivId);
    
            if (selectedOption === 'other') {
                otherInputDiv.style.display = 'block'; // Show input field
            } else {
                otherInputDiv.style.display = 'none'; // Hide input field
            }
        }

        document.getElementById('demographicsForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            // You can process the form data here if needed
            // For example, you can save the data to local storage or send it to a server

            // Set a flag in local storage to indicate that the demographics form has been filled
            localStorage.setItem('demographicsFilled', 'true');

            // Redirect to the questions page
            window.location.href = 'question.html'; // Replace 'questions.html' with the actual path to your questions page

        });
