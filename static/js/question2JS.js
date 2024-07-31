if (!localStorage.getItem("demographicsFilled")) {
  // If not, redirect to the demographics form
  window.location.href = "index.html"; // Replace 'index.html' with the actual path to your demographics form
}

// Call this function when you want to reset the form and local storage
function resetForm() {
  localStorage.removeItem("demographicsFilled"); // Clear the flag
  // Redirect to the demographics form
  window.location.href = "index.html";
}

// Call resetForm() where necessary

let currentQuestion = 0;
const questions = []; // Store questions here
const answers = []; // Store answers here

// Function to load questions
function loadQuestions() {
  fetch("/static/data/gform2.json")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((question) => {
        questions.push({
          text: question.text,
          options: question.options,
        });
      });
      showQuestion();
    })
    .catch((error) => console.error("Error fetching questions:", error));
}

// Function to display current question
function showQuestion() {
  const questionsContainer = document.querySelector(".question-container");
  const currentQuestionData = questions[currentQuestion];
  const optionsHtml = currentQuestionData.options
    .map(
      (option, index) => `
                <div class="answer-option">
                    <input type="radio" id="question_${
                      currentQuestion + 1
                    }_option_${index + 1}" name="question_${
        currentQuestion + 1
      }" value="${index}" onchange="saveAnswer(this)">
                    <label for="question_${currentQuestion + 1}_option_${
        index + 1
      }">
                        <div class="option-index">${index + 1}</div>
                        ${option}
                    </label>
                </div>

            `
    )
    .join("");

  questionsContainer.innerHTML = `
                <div class="question">
                    <div class="question-index-container">
                        <div class="question-index">Question ${
                          currentQuestion + 1
                        }/${questions.length}</div>
                    </div>
                    <div class="question-text-container">
                        <div class="ques-container">
                            <label for="question_${currentQuestion + 1}">${
    currentQuestionData.text
  }</label>
                        </div>
                        <div class="option-container">
                            ${optionsHtml}
                        </div>
                    </div>
                </div>
            `;

  // Check the saved answer for the current question
  const radioButtons = document.querySelectorAll(
    `input[name="question_${currentQuestion + 1}"]`
  );
  if (answers[currentQuestion] !== undefined) {
    radioButtons[answers[currentQuestion]].checked = true;
  }

  updateNavigationButtons();
}

// Function to save selected answer
function saveAnswer(element) {
  const questionIndex = parseInt(element.name.split("_")[1]) - 1;
  const answerValue = parseInt(element.value);
  answers[questionIndex] = answerValue;
}

// Function to show/hide navigation buttons based on current question
function updateNavigationButtons() {
  const prevButton = document.getElementById("prevButton");
  const nextButton = document.getElementById("nextButton");
  const submitButton = document.getElementById("submitButton");

  prevButton.style.display = currentQuestion === 0 ? "none" : "inline";
  nextButton.style.display =
    currentQuestion === questions.length - 1 ? "none" : "inline";
  submitButton.style.display =
    currentQuestion === questions.length - 1 ? "inline" : "none";
}

// Function to move to the previous question
function prevQuestion() {
  if (currentQuestion > 0) {
    currentQuestion--;
    showQuestion();
  }
}

// Function to move to the next question
function nextQuestion() {
  // Check if an answer is selected for the current question
  if (answers[currentQuestion] !== undefined) {
    if (currentQuestion < questions.length - 1) {
      currentQuestion++;
      showQuestion();
    }
  } else {
    // Show toast notification
    showToast(
      "Please select an answer before proceeding to the next question."
    );
  }
}

function submitQuiz() {
  // Store answers in a hidden input field before submission
  const form = document.querySelector("form");
  const answersField = document.createElement("input");
  answersField.type = "hidden";
  answersField.name = "answers";
  answersField.value = JSON.stringify(answers); // Convert answers array to JSON string
  form.appendChild(answersField);

  form.submit(); // Submit the form
  showToast("Quiz submitted!");
  localStorage.setItem("quizSubmitted", "true");
  setTimeout(() => {
    window.location.href = "result2.html";
  }, 2000);
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.innerText = message;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000); // Hide toast after 3 seconds
}

// Load questions when the page is loaded
window.onload = loadQuestions;
