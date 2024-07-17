const express = require('express');
const cors = require('cors');
const app = express();
const bodyParser = require('body-parser');

app.use(cors());  // Enable CORS for all routes
app.use(bodyParser.json());

let questions = [
    { id: 1, text: "You find it difficult to introduce yourself to other people.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 2, text: "You often get so lost in thoughts that you ignore or forget your surroundings.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 3, text: "You try to respond to your e-mails as soon as possible and cannot stand a messy inbox.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 4, text: "You find it easy to stay relaxed and focused even when there is some pressure.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 5, text: "You do not usually initiate conversations.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 6, text: "You rarely do something just out of sheer curiosity.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 7, text: "You feel superior to other people.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 8, text: "Being organized is more important to you than being adaptable.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 9, text: "You are usually highly motivated and energetic.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] },
    { id: 10, text: "Winning a debate matters less to you than making sure no one gets upset.", answers: ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"] }
];

app.get('/api/questions', (req, res) => {
    res.json(questions);
});

app.post('/api/save-answer', (req, res) => {
    const { questionId, answer } = req.body;
    console.log(`Question ID: ${questionId}, Answer: ${answer}`);
    res.sendStatus(200);
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
