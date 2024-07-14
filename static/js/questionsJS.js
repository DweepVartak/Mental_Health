document.addEventListener('DOMContentLoaded', function() {
    if (!localStorage.getItem('demographicsFilled')) {
        window.location.href = indexUrl;
    }

    let currentQuestion = 0;
    const questions = [];
    const answers = [];

    function loadQuestions() {
        fetch(questionsUrl)
            .then(response => response.text())
            .then(data => {
                questions.push(...data.split('\n'));
                document.getElementById('totalQuestions').innerText = questions.length;
                showQuestion();
            })
            .catch(error => console.error('Error fetching questions:', error));
    }

    function showQuestion() {
        const questionsContainer = document.querySelector('.question-text-container');
        questionsContainer.innerHTML = `
            <div class="ques-container" style="height:40px">
                <label for="question_${currentQuestion + 1}">${questions[currentQuestion]}</label>
            </div>
            <div class="option-container">
                <div class="answer-option">
                    <input type="radio" id="question_${currentQuestion + 1}_option_1" name="question_${currentQuestion + 1}" value="0" onchange="saveAnswer(this)">
                    <label for="question_${currentQuestion + 1}_option_1">
                        <div class="option-index">1</div>
                        Never
                    </label>
                </div>
                <div class="answer-option">
                    <input type="radio" id="question_${currentQuestion + 1}_option_2" name="question_${currentQuestion + 1}" value="1" onchange="saveAnswer(this)">
                    <label for="question_${currentQuestion + 1}_option_2">
                        <div class="option-index">2</div>
                        Rarely
                    </label>
                </div>
                <div class="answer-option">
                    <input type="radio" id="question_${currentQuestion + 1}_option_3" name="question_${currentQuestion + 1}" value="2" onchange="saveAnswer(this)">
                    <label for="question_${currentQuestion + 1}_option_3">
                        <div class="option-index">3</div>
                        Moderately
                    </label>
                </div>
                <div class="answer-option">
                    <input type="radio" id="question_${currentQuestion + 1}_option_4" name="question_${currentQuestion + 1}" value="3" onchange="saveAnswer(this)">
                    <label for="question_${currentQuestion + 1}_option_4">
                        <div class="option-index">4</div>
                        Frequently
                    </label>
                </div>
                <div class="answer-option">
                    <input type="radio" id="question_${currentQuestion + 1}_option_5" name="question_${currentQuestion + 1}" value="4" onchange="saveAnswer(this)">
                    <label for="question_${currentQuestion + 1}_option_5">
                        <div class="option-index">5</div>
                        Extremely
                    </label>
                </div>
            </div>
        `;
         // Update the question index display
    document.getElementById('currentQuestionIndex').innerText = currentQuestion + 1;

    // Check if user has previously answered this question
    const radioButtons = document.querySelectorAll(`input[name="question_${currentQuestion + 1}"]`);
    if (answers[currentQuestion] !== undefined) {
        radioButtons[answers[currentQuestion]].checked = true;
    }
    updateNavigationButtons();
}

    window.saveAnswer = function(element) {
        const questionIndex = parseInt(element.name.split('_')[1]) - 1;
        const answerValue = parseInt(element.value);
        answers[questionIndex] = answerValue;

        const existingInput = document.querySelector(`input[name="question_${questionIndex + 1}"]`);
        if (existingInput) {
            existingInput.value = answerValue;
        } else {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = `question_${questionIndex + 1}`;
            input.value = answerValue;
            document.querySelector('form').appendChild(input);
        }
    };

    function updateNavigationButtons() {
        const prevButton = document.getElementById('prevButton');
        const nextButton = document.getElementById('nextButton');
        const submitButton = document.getElementById('submitButton');

        prevButton.style.display = currentQuestion === 0 ? 'none' : 'inline';
        nextButton.style.display = currentQuestion === questions.length - 1 ? 'none' : 'inline';
        submitButton.style.display = currentQuestion === questions.length - 1 ? 'inline' : 'none';
    }

    document.getElementById('prevButton').addEventListener('click', function() {
        if (currentQuestion > 0) {
            currentQuestion--;
            showQuestion();
        }
    });

    document.getElementById('nextButton').addEventListener('click', function() {
        if (answers[currentQuestion] !== undefined) {
            if (currentQuestion < questions.length - 1) {
                currentQuestion++;
                showQuestion();
            }
        } else {
            showToast('Please select an answer before proceeding to the next question.');
        }
    });

    document.getElementById('submitButton').addEventListener('click', function() {
        const form = document.querySelector('form');
        
        answers.forEach((answer, index) => {
            const existingInput = document.querySelector(`input[name="question_${index + 1}"]`);
            if (!existingInput) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = `question_${index + 1}`;
                input.value = answer;
                form.appendChild(input);
            }
        });

        form.submit();
        showToast('Quiz submitted!');
        localStorage.setItem('quizSubmitted', 'true');
        setTimeout(() => {
            window.location.href = 'result';
        }, 2000);
    });

    function showToast(message) {
        const toast = document.getElementById('toast');
        toast.innerText = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }

    window.onload = loadQuestions;
});
