document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('role-form');
    const jobTitleInput = document.getElementById('job-title-input');
    const resultsContainer = document.getElementById('results-container');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const jobTitle = jobTitleInput.value.trim();
        if (!jobTitle) {
            return;
        }

        // Show loading state
        resultsContainer.innerHTML = '<div class="loading">Analyzing your role...</div>';

        try {
            const response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ job_title: jobTitle }),
            });

            const data = await response.json();

            if (!response.ok) {
                // Handle errors from the API
                throw new Error(data.error || 'An unknown error occurred.');
            }

            renderResults(data);

        } catch (error) {
            renderError(error.message);
        }
    });

    function renderResults(data) {
        // Clear previous results
        resultsContainer.innerHTML = '';

        // --- Role Overview ---
        const overviewSection = document.createElement('div');
        overviewSection.className = 'result-section';
        overviewSection.innerHTML = `
            <h2>${data.role_title}</h2>
            <p>${data.description}</p>
            <span class="impact-level ${data.impact_level.split(' ')[0].toLowerCase()}">${data.impact_level}</span>
        `;
        resultsContainer.appendChild(overviewSection);

        // --- Skill Analysis ---
        const skillsSection = document.createElement('div');
        skillsSection.className = 'result-section';
        const requiredSkills = new Set(data.required_skills_for_role);
        const userSkills = new Set(data.user_skills);

        let skillsHtml = `
            <h2>Skill Analysis</h2>
            <p>Comparing your skills to those required for a ${data.role_title}.</p>
            <h4>Required Skills:</h4>
            <ul class="skills-list">
        `;
        requiredSkills.forEach(skill => {
            const hasSkill = userSkills.has(skill);
            // In the MVP, we can't highlight the gap visually this way,
            // but we can add a class if we wanted to. The backend determines the gap.
            skillsHtml += `<li>${skill}</li>`;
        });
        skillsHtml += '</ul>';

        skillsSection.innerHTML = skillsHtml;
        resultsContainer.appendChild(skillsSection);


        // --- Learning Plan ---
        const learningPlanSection = document.createElement('div');
        learningPlanSection.className = 'result-section';

        let learningPlanHtml = '<h2>Personalized Learning Plan</h2>';

        if (data.learning_plan && data.learning_plan.length > 0) {
            learningPlanHtml += '<p>To bridge your skill gap, we recommend focusing on the following areas:</p>';
            data.learning_plan.forEach(item => {
                learningPlanHtml += `
                    <h3>Learn: ${item.skill_to_learn}</h3>
                `;
                item.suggested_resources.forEach(resource => {
                    learningPlanHtml += `
                        <div class="resource">
                            <h4>${resource.title} (${resource.type})</h4>
                            <a href="${resource.url}" target="_blank" rel="noopener noreferrer">Go to resource &rarr;</a>
                        </div>
                    `;
                });
            });
        } else {
            learningPlanHtml += '<p>Congratulations! Based on our analysis, you possess all the key skills for this role.</p>';
        }

        learningPlanSection.innerHTML = learningPlanHtml;
        resultsContainer.appendChild(learningPlanSection);
    }

    function renderError(errorMessage) {
        resultsContainer.innerHTML = `<div class="error">${errorMessage}</div>`;
    }
});
