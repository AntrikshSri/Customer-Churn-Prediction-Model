document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const modal = document.getElementById('result-modal');
    const closeModal = document.getElementById('close-modal');
    const resetBtn = document.getElementById('reset-btn');
    
    const loadingState = document.getElementById('loading-state');
    const resultState = document.getElementById('result-state');
    
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    const confidenceFill = document.getElementById('confidence-fill');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show Modal in Loading State
        modal.classList.add('active');
        loadingState.classList.remove('hidden');
        resultState.classList.add('hidden');

        // Gather Data
        const formData = new FormData(form);
        const data = { input: {} };
        
        for (let [key, value] of formData.entries()) {
            // Convert numerical strings back to numbers if needed (though the API expects raw types mostly, we parse numbers)
            if (key === 'tenure' || key === 'seniorcitizen') {
                data.input[key] = parseInt(value, 10);
            } else if (key === 'monthlycharges' || key === 'totalcharges') {
                data.input[key] = parseFloat(value);
            } else {
                data.input[key] = value;
            }
        }

        try {
            // Simulated delay for dramatic effect
            await new Promise(r => setTimeout(r, 1200));

            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Prediction failed');
            
            const result = await response.json();
            showResult(result.prediction);

        } catch (error) {
            console.error(error);
            showError();
        }
    });

    function showResult(prediction) {
        loadingState.classList.add('hidden');
        resultState.classList.remove('hidden');

        if (prediction === 1) {
            // Churn
            resultIcon.className = 'result-icon danger';
            resultIcon.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
            resultTitle.textContent = 'High Churn Risk';
            resultMessage.textContent = 'This customer exhibits patterns strongly associated with account cancellation.';
            confidenceFill.style.background = 'var(--danger)';
            
            // Animate progress bar to high percentage
            setTimeout(() => {
                confidenceFill.style.width = (80 + Math.random() * 15) + '%';
            }, 100);
            
        } else {
            // Safe
            resultIcon.className = 'result-icon safe';
            resultIcon.innerHTML = '<i class="fa-solid fa-check"></i>';
            resultTitle.textContent = 'Customer Retained';
            resultMessage.textContent = 'This customer has a stable profile and is likely to stay.';
            confidenceFill.style.background = 'var(--success)';
            
            // Animate progress bar to low percentage
            setTimeout(() => {
                confidenceFill.style.width = (10 + Math.random() * 15) + '%';
            }, 100);
        }
    }

    function showError() {
        loadingState.classList.add('hidden');
        resultState.classList.remove('hidden');
        
        resultIcon.className = 'result-icon';
        resultIcon.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>';
        resultTitle.textContent = 'System Error';
        resultMessage.textContent = 'Failed to analyze customer. Please check the data and try again.';
        confidenceFill.style.width = '0%';
    }

    const closeAll = () => {
        modal.classList.remove('active');
        setTimeout(() => {
            confidenceFill.style.width = '0%'; // Reset for next time
        }, 400);
    };

    closeModal.addEventListener('click', closeAll);
    resetBtn.addEventListener('click', () => {
        closeAll();
        // Optional: form.reset();
    });
});
