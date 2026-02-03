document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('intake-form');
    const input = document.getElementById('patient-input');
    const fileInput = document.getElementById('file-input');
    const fileTriggerBtn = document.getElementById('file-trigger-btn');
    const clearFileBtn = document.getElementById('clear-file-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorContainer = document.getElementById('error-container');
    const resultsContainer = document.getElementById('results-container');

    // Result elements
    const resultIntake = document.getElementById('result-intake');
    const resultValidationBadge = document.getElementById('result-validation-badge');
    const resultReasoning = document.getElementById('result-reasoning');
    const resultActions = document.getElementById('result-actions');
    const resultAudit = document.getElementById('result-audit');

    // File Upload Handling
    fileTriggerBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (fileInput.files && fileInput.files[0]) {
            const file = fileInput.files[0];
            fileTriggerBtn.textContent = `📎 ${file.name}`;
            clearFileBtn.classList.remove('hidden');
        }
    });

    clearFileBtn.addEventListener('click', () => {
        fileInput.value = '';
        fileTriggerBtn.textContent = '📎 Attach Report (PDF/Image)';
        clearFileBtn.classList.add('hidden');
    });

    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset state
        errorContainer.classList.add('hidden');
        errorContainer.textContent = '';
        resultsContainer.classList.add('hidden');
        setLoading(true);

        const formData = new FormData();
        formData.append('raw_input', input.value);
        if (fileInput.files && fileInput.files[0]) {
            formData.append('file', fileInput.files[0]);
        }

        try {
            // Determine API URL (relative path since served from same origin)
            const apiUrl = '/invoke';

            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            displayResults(data);

        } catch (err) {
            console.error(err);
            errorContainer.textContent = err.message || 'An error occurred during analysis.';
            errorContainer.classList.remove('hidden');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<span class="loader"></span> Processing...';
            loadingIndicator.classList.remove('hidden');
        } else {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Case';
            loadingIndicator.classList.add('hidden');
        }
    }

    function displayResults(data) {
        // Intake
        resultIntake.textContent = JSON.stringify(data.structured_data, null, 2);

        // Validation
        resultValidationBadge.className = 'status-badge ' + (data.validated ? 'success' : 'warning');
        resultValidationBadge.textContent = data.validated ? 'Valid' : 'Issues Found';

        // Reasoning
        resultReasoning.textContent = data.decision;

        // Actions
        resultActions.innerHTML = '';
        if (data.actions && Array.isArray(data.actions)) {
            data.actions.forEach(action => {
                const li = document.createElement('li');
                li.textContent = action;
                resultActions.appendChild(li);
            });
        }

        // Audit
        if (data.audit_log && data.audit_log.length > 0) {
            const latestLog = data.audit_log[data.audit_log.length - 1];
            resultAudit.textContent = JSON.stringify(latestLog, null, 2);
        } else {
            resultAudit.textContent = 'No audit log available';
        }

        resultsContainer.classList.remove('hidden');
    }
});
