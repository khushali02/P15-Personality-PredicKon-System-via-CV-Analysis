document.addEventListener('DOMContentLoaded', () => {
    const questionContainer = document.getElementById('question-container');
    const nextButton = document.getElementById('next-button');

    fetch('http://localhost:3000/api/questions')
        .then(response => response.json())
        .then(questions => {
            let currentQuestionIndex = 0;
            showQuestion(questions[currentQuestionIndex]);

            nextButton.addEventListener('click', () => {
                const selectedAnswer = document.querySelector('input[name="answer"]:checked');
                if (selectedAnswer) {
                    const answer = selectedAnswer.value;
                    const questionId = questions[currentQuestionIndex].id;

                    fetch('http://localhost:3000/api/save-answer', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ questionId, answer })
                    });

                    currentQuestionIndex++;
                    if (currentQuestionIndex < questions.length) {
                        showQuestion(questions[currentQuestionIndex]);
                    } else {
                        alert('Assessment complete');
                    }
                } else {
                    alert('Please select an answer');
                }
            });

            function showQuestion(question) {
                questionContainer.innerHTML = `
                    <p>${question.text}</p>
                    ${question.answers.map(answer => `
                        <label>
                            <input type="radio" name="answer" value="${answer}">
                            ${answer}
                        </label>
                    `).join('')}
                `;
            }
        });
});
