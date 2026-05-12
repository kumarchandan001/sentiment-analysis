// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    // --- Element References ---
    const reviewTextArea = document.getElementById('reviewText');
    const analyzeButton = document.getElementById('analyzeBtn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const resultDiv = document.getElementById('result');
    const predictionResultH2 = document.getElementById('predictionResult');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');
    const wordCountSpan = document.getElementById('wordCount');
    const exampleButtons = document.querySelectorAll('.example-btn');

    // --- Functions ---
    const setLoadingState = (isLoading) => {
        if (isLoading) {
            btnText.style.display = 'none';
            loader.style.display = 'block';
            analyzeButton.disabled = true;
        } else {
            btnText.style.display = 'block';
            loader.style.display = 'none';
            analyzeButton.disabled = false;
        }
    };

    const updateTextMetrics = () => {
        const text = reviewTextArea.value;
        const wordCount = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        wordCountSpan.textContent = wordCount;
    };

    const displayResult = (prediction, confidence) => {
        const sentimentClass = prediction.toLowerCase();
        
        predictionResultH2.textContent = `${prediction}`;
        predictionResultH2.className = sentimentClass;
        
        confidenceBar.style.width = `${confidence}%`;
        confidenceBar.className = `confidence-bar ${sentimentClass}`;

        confidenceText.textContent = `Confidence: ${confidence}%`;
        
        resultDiv.style.display = 'block';
        setTimeout(() => resultDiv.classList.add('visible'), 10);
    };

    const analyzeSentiment = async () => {
        const reviewText = reviewTextArea.value;

        if (reviewText.trim() === '') {
            alert('Please enter a review.');
            return;
        }

        setLoadingState(true);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ review_text: reviewText }),
            });
            const data = await response.json();
            displayResult(data.prediction, data.confidence);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        } finally {
            setLoadingState(false);
        }
    };

    // --- Event Listeners ---
    analyzeButton.addEventListener('click', analyzeSentiment);
    
    reviewTextArea.addEventListener('input', updateTextMetrics);

    exampleButtons.forEach(button => {
        button.addEventListener('click', () => {
            reviewTextArea.value = button.dataset.text;
            updateTextMetrics();
            resultDiv.style.display = 'none';
            resultDiv.classList.remove('visible');
        });
    });
    // Call this once on load to set initial state
    updateTextMetrics();

    // Place this function inside your DOMContentLoaded event listener in script.js
    const loadDashboardStats = async () => {
        try {
            const response = await fetch('/stats');
            const data = await response.json();

            const positiveCount = data.Positive || 0;
            const negativeCount = data.Negative || 0;
            const totalCount = positiveCount + negativeCount;
            const positivePercentage = totalCount > 0 ? ((positiveCount / totalCount) * 100).toFixed(1) : 0;

            // Populate stat boxes
            document.querySelector('#totalReviewsStat .stat-info p').textContent = totalCount;
            document.querySelector('#positivePercentageStat .stat-info p').textContent = `${positivePercentage}%`;
            
            // Get CSS variables for colors
            const style = getComputedStyle(document.body);
            const positiveColor = style.getPropertyValue('--positive-sentiment-color').trim();
            const negativeColor = style.getPropertyValue('--negative-sentiment-color').trim();

            // Render Chart
            const ctx = document.getElementById('sentimentChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut', // Doughnut is a nice alternative to pie
                data: {
                    labels: ['Positive', 'Negative'],
                    datasets: [{
                        data: [positiveCount, negativeCount],
                        backgroundColor: [positiveColor, negativeColor],
                        borderWidth: 2
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });
        } catch (error) {
            console.error('Error loading dashboard stats:', error);
        }
    };

    // Call the function when the page loads
    loadDashboardStats();
});