// Chart.js Visualizations for Analytics Dashboard

document.addEventListener('DOMContentLoaded', () => {
    fetch('/analytics/api/data')
        .then(response => response.json())
        .then(data => {
            renderExpertiseChart(data.expertise_distribution);
            renderSkillsChart(data.top_skills);
            renderModelComparisonChart(data.model_performance);
            renderCareerTrendsChart(data.career_trends);
        })
        .catch(err => console.error("Error fetching analytics chart data:", err));
});

function renderExpertiseChart(data) {
    const ctx = document.getElementById('expertiseChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    '#3B82F6', '#8B5CF6', '#06B6D4', '#10B981', '#F59E0B', 
                    '#EC4899', '#6366F1', '#14B8A6', '#F97316', '#A855F7'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94A3B8', font: { family: 'Outfit' } } }
            }
        }
    });
}

function renderSkillsChart(data) {
    const ctx = document.getElementById('skillsChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'User Frequency',
                data: data.values,
                backgroundColor: 'rgba(59, 130, 246, 0.75)',
                borderColor: '#3B82F6',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                x: { ticks: { color: '#94A3B8' }, grid: { display: false } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderModelComparisonChart(data) {
    const ctx = document.getElementById('modelChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Accuracy (%)',
                    data: data.accuracy,
                    backgroundColor: '#10B981',
                    borderRadius: 6
                },
                {
                    label: 'F1 Score (%)',
                    data: data.f1_score,
                    backgroundColor: '#6366F1',
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { min: 60, max: 100, ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                x: { ticks: { color: '#94A3B8' }, grid: { display: false } }
            },
            plugins: {
                legend: { position: 'top', labels: { color: '#94A3B8' } }
            }
        }
    });
}

function renderCareerTrendsChart(data) {
    const ctx = document.getElementById('trendsChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    'rgba(59, 130, 246, 0.6)',
                    'rgba(139, 92, 246, 0.6)',
                    'rgba(6, 182, 212, 0.6)',
                    'rgba(16, 185, 129, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94A3B8' } }
            }
        }
    });
}
