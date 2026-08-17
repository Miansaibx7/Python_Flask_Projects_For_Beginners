document.addEventListener('DOMContentLoaded', function () {
    const chartElement = document.getElementById('marksChart');
    if (!chartElement) return;  // safety if chart not on page

    // Get data from data attributes
    const labels = JSON.parse(chartElement.dataset.labels);
    const marks = JSON.parse(chartElement.dataset.marks);
    const maxValue = Math.max(...marks, 0) + 10;

    const ctx = chartElement.getContext('2d');
    // ✅ Capital 'Chart' (not 'chart')
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Marks',
                data: marks,
                backgroundColor: '#007bff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: maxValue
                }
            }
        }
    });
});