document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('csv-file');
    const uploadSection = document.getElementById('upload-section');
    const uploadContent = document.querySelector('.upload-content');
    const loadingState = document.getElementById('loading');
    const dashboard = document.getElementById('dashboard');

    let latestExcelUrl = null;

    // Handle File Selection
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Show Processing State
        uploadContent.classList.add('hidden');
        loadingState.classList.remove('hidden');
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const limitVal = document.getElementById('budget-limit').value;
            formData.append('budget_limit', limitVal);
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.success) {
                // Populate dashboard
                populateDashboard(data);
                
                // Show dashboard
                uploadSection.classList.add('hidden');
                dashboard.classList.remove('hidden');
                dashboard.classList.add('fade-in');
                
                // Show toast
                showToast(data.status_message);
                
                // Save excel url
                latestExcelUrl = data.excel_url;
            } else {
                alert("Error processing file: " + data.error);
                uploadContent.classList.remove('hidden');
                loadingState.classList.add('hidden');
            }
        } catch (err) {
            console.error(err);
            alert("Failed to connect to the backend server.");
            uploadContent.classList.remove('hidden');
            loadingState.classList.add('hidden');
        }
    });

    document.getElementById('download-excel-btn').addEventListener('click', () => {
        if (latestExcelUrl) {
            window.location.href = latestExcelUrl;
        } else {
            alert("Report not ready yet.");
        }
    });

    function showToast(message) {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');
        toastMessage.innerText = message;
        toast.classList.remove('hidden');
        toast.classList.add('show');
        
        // Hide after 6 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(()=> toast.classList.add('hidden'), 400);
        }, 6000);
    }

    const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(val);

    function populateDashboard(data) {
        // Update Stats
        const netValue = data.total_income - data.total_expense;
        document.querySelector('.stat-card:nth-child(1) .stat-value').innerText = formatCurrency(netValue);
        document.querySelector('.stat-card:nth-child(2) .stat-value').innerText = formatCurrency(data.total_income);
        document.querySelector('.stat-card:nth-child(3) .stat-value').innerText = formatCurrency(data.total_expense);

        // Update Recent Transactions
        const txList = document.querySelector('.transaction-list');
        txList.innerHTML = '';
        
        const typeEmojiMap = {
            'Food': '🍕', 'Travel': '🚕', 'Income': '💼', 'Subscriptions': '📺', 'Shopping': '🛍️', 'Bills': '🧾', 'Groceries': '🛒', 'Others': '📦'
        };

        const typeClassMap = {
            'Food': 'food', 'Travel': 'travel', 'Income': 'income', 'Subscriptions': 'sub', 'Shopping': 'food', 'Bills': 'travel', 'Groceries': 'food', 'Others': 'sub'
        };

        data.recent.reverse().forEach(tx => {
            const emoji = typeEmojiMap[tx.Category] || '🏷️';
            const catClass = typeClassMap[tx.Category] || 'sub';
            
            const isNegative = tx.Amount < 0;
            const amountClass = isNegative ? 'negative' : 'positive';
            const amountDisplay = isNegative ? formatCurrency(tx.Amount) : '+' + formatCurrency(tx.Amount);

            txList.innerHTML += `
                <li class="transaction-item">
                    <div class="tx-info">
                        <div class="tx-icon ${catClass}">${emoji}</div>
                        <div>
                            <h4 style="max-width: 150px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${tx.Description}">${tx.Description}</h4>
                            <p class="ml-cat">Categorized as ${tx.Category}</p>
                        </div>
                    </div>
                    <div class="tx-amount ${amountClass}">${amountDisplay}</div>
                </li>
            `;
        });

        initChart(data.summary);
    }

    let myChart = null;

    function initChart(summaryData) {
        if(myChart) myChart.destroy();
        const ctx = document.getElementById('categoryChart').getContext('2d');
        
        const labels = Object.keys(summaryData);
        const dataVals = Object.values(summaryData);

        const colors = [
            'rgba(139, 92, 246, 0.8)', // Purple
            'rgba(59, 130, 246, 0.8)', // Blue
            'rgba(16, 185, 129, 0.8)', // Green
            'rgba(244, 63, 94, 0.8)',  // Rose
            'rgba(245, 158, 11, 0.8)', // Amber
            'rgba(100, 116, 139, 0.8)' // Slate
        ];

        myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataVals,
                    backgroundColor: colors.slice(0, labels.length),
                    borderColor: colors.slice(0, labels.length).map(c => c.replace('0.8', '1.0')),
                    borderWidth: 1,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#e2e8f0', font: { family: "'Outfit', sans-serif", size: 14 }, padding: 20 }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(18, 18, 23, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#e2e8f0',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1, padding: 12, cornerRadius: 8, displayColors: true,
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) { label += ': '; }
                                if (context.parsed !== null) {
                                    label += new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(context.parsed);
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
});
