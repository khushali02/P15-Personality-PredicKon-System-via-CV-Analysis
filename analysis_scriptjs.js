// Simulate progress update
let progress = 0;
const progressBar = document.getElementById('progress');

function updateProgress() {
    progress += 10;
    if (progress > 100) {
        progress = 100;
        location.href = 'results.html';
    }
    progressBar.style.width = progress + '%';
}

setInterval(updateProgress, 1000);
