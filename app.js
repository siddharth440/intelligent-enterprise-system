/**
 * INTELLIGENT ENTERPRISE SYSTEM - APPLICATION CORE (ES6 Vanilla JS)
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // 2. Application State Management
    const defaultState = {
        theme: localStorage.getItem('nexus_theme') || 'dark',
        activeTab: 'dashboard',
        telemetry: {
            arr: 24.85,
            efficiency: 94.8,
            workflows: 1482,
            riskScore: 0.04
        },
        erpAssets: [
            { id: 'SKU-9021', name: 'Quantum Cluster Node Alpha', dept: 'Infrastructure', location: 'US-East-1', qty: '120 Nodes', status: 'Optimal', lastAudit: '2026-08-01' },
            { id: 'SKU-4810', name: 'APAC Edge Logistics Server', dept: 'Logistics', location: 'SG-Central', qty: '45 Units', status: 'Warning', lastAudit: '2026-08-03' },
            { id: 'SKU-1120', name: 'GPU Acceleration Matrix', dept: 'Hardware', location: 'EU-West-2', qty: '80 Units', status: 'Optimal', lastAudit: '2026-07-28' },
            { id: 'SKU-7734', name: 'Fiber Optical Gateway B', dept: 'Infrastructure', location: 'US-West-2', qty: '200 Units', status: 'Critical', lastAudit: '2026-08-04' },
            { id: 'SKU-3391', name: 'Automated Warehouse Rover', dept: 'Procurement', location: 'Tokyo-Node', qty: '15 Units', status: 'Optimal', lastAudit: '2026-08-02' }
        ],
        crmDeals: [
            { id: 1, client: 'Apex Global Energy', value: 450000, stage: 'proposal', score: 92, owner: 'Alex Rivera' },
            { id: 2, client: 'Vanguard Aerospace', value: 1200000, stage: 'negotiation', score: 88, owner: 'Sarah Chen' },
            { id: 3, client: 'BioHealth Dynamics', value: 280000, stage: 'qualification', score: 74, owner: 'Marcus Brody' },
            { id: 4, client: 'Horizon Financial Corp', value: 640000, stage: 'lead', score: 65, owner: 'Eleanor Vance' },
            { id: 5, client: 'CyberGrid Logistics', value: 310000, stage: 'closed-won', score: 96, owner: 'Sarah Chen' }
        ],
        anomalies: [
            { id: 1, text: 'Logistics Latency Spike in SG-Central (+14%)', time: '17:28:12', level: 'warning' },
            { id: 2, text: 'GPU Node #04 Thermal Deviation Corrected', time: '17:15:00', level: 'info' },
            { id: 3, text: 'Automated Fraud Defense Triggered (Blocked IP)', time: '16:54:20', level: 'success' }
        ]
    };

    let appState = JSON.parse(localStorage.getItem('nexus_app_state')) || defaultState;

    function saveState() {
        localStorage.setItem('nexus_app_state', JSON.stringify(appState));
    }

    // 3. Theme Toggle Setup
    const themeToggleBtn = document.getElementById('theme-toggle');
    const setDarkBtn = document.getElementById('set-dark-mode');
    const setLightBtn = document.getElementById('set-light-mode');

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        appState.theme = theme;
        localStorage.setItem('nexus_theme', theme);
        saveState();
    }

    applyTheme(appState.theme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const newTheme = appState.theme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }

    if (setDarkBtn) setDarkBtn.addEventListener('click', () => applyTheme('dark'));
    if (setLightBtn) setLightBtn.addEventListener('click', () => applyTheme('light'));

    // 4. Tab View Switcher Navigation
    const navButtons = document.querySelectorAll('.nav-item[data-tab]');
    const tabViews = document.querySelectorAll('.tab-view');

    function switchTab(tabId) {
        navButtons.forEach(btn => {
            if (btn.getAttribute('data-tab') === tabId) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        tabViews.forEach(view => {
            if (view.id === `view-${tabId}`) {
                view.classList.add('active');
            } else {
                view.classList.remove('active');
            }
        });

        appState.activeTab = tabId;
        saveState();
    }

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            switchTab(btn.getAttribute('data-tab'));
        });
    });

    // 5. Live Clock Update
    function updateClock() {
        const liveClockEl = document.getElementById('live-time');
        if (liveClockEl) {
            const now = new Date();
            liveClockEl.textContent = now.toUTCString().split(' ')[4] + ' UTC';
        }
    }
    setInterval(updateClock, 1000);
    updateClock();

    // 6. Chart.js Visualizations
    let revenueChart, radarChart, cashflowChart, expenseChart;

    function initCharts() {
        const isDark = appState.theme === 'dark';
        const textColor = isDark ? '#9CA3AF' : '#4B5563';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';

        // Chart 1: Revenue Forecast Line Chart
        const revCtx = document.getElementById('revenueForecastChart')?.getContext('2d');
        if (revCtx) {
            if (revenueChart) revenueChart.destroy();
            revenueChart = new Chart(revCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul (AI)', 'Aug (AI)', 'Sep (AI)'],
                    datasets: [
                        {
                            label: 'Actual Revenue ($M)',
                            data: [18.2, 19.5, 21.0, 22.4, 23.8, 24.85, null, null, null],
                            borderColor: '#00F2FE',
                            backgroundColor: 'rgba(0, 242, 254, 0.1)',
                            fill: true,
                            tension: 0.4,
                            borderWidth: 3
                        },
                        {
                            label: 'AI Forecast Projections ($M)',
                            data: [null, null, null, null, null, 24.85, 26.2, 27.9, 29.5],
                            borderColor: '#7F00FF',
                            borderDash: [5, 5],
                            backgroundColor: 'rgba(127, 0, 255, 0.05)',
                            fill: true,
                            tension: 0.4,
                            borderWidth: 3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: textColor, font: { family: 'Plus Jakarta Sans' } } }
                    },
                    scales: {
                        x: { grid: { color: gridColor }, ticks: { color: textColor } },
                        y: { grid: { color: gridColor }, ticks: { color: textColor } }
                    }
                }
            });
        }

        // Chart 2: Resource Distribution Radar
        const radarCtx = document.getElementById('resourceRadarChart')?.getContext('2d');
        if (radarCtx) {
            if (radarChart) radarChart.destroy();
            radarChart = new Chart(radarCtx, {
                type: 'radar',
                data: {
                    labels: ['Cloud Compute', 'Logistics Nodes', 'Security AI', 'R&D Innovation', 'Sales Automation', 'Customer Care'],
                    datasets: [{
                        label: 'Capacity Index (%)',
                        data: [95, 88, 98, 90, 85, 92],
                        backgroundColor: 'rgba(0, 242, 254, 0.25)',
                        borderColor: '#00F2FE',
                        pointBackgroundColor: '#7F00FF'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        r: {
                            angleLines: { color: gridColor },
                            grid: { color: gridColor },
                            pointLabels: { color: textColor, font: { size: 10 } },
                            ticks: { display: false }
                        }
                    }
                }
            });
        }

        // Chart 3: Financial Cashflow Bar
        const cashCtx = document.getElementById('cashflowChart')?.getContext('2d');
        if (cashCtx) {
            if (cashflowChart) cashflowChart.destroy();
            cashflowChart = new Chart(cashCtx, {
                type: 'bar',
                data: {
                    labels: ['Q1', 'Q2', 'Q3 (Est)', 'Q4 (Est)'],
                    datasets: [
                        { label: 'Gross Revenue', data: [68.4, 72.1, 78.5, 84.0], backgroundColor: '#00F2FE' },
                        { label: 'OPEX Expenses', data: [42.1, 44.0, 46.2, 48.0], backgroundColor: '#7F00FF' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: textColor } } },
                    scales: {
                        x: { grid: { color: gridColor }, ticks: { color: textColor } },
                        y: { grid: { color: gridColor }, ticks: { color: textColor } }
                    }
                }
            });
        }

        // Chart 4: Expense Donut
        const expCtx = document.getElementById('expenseDonutChart')?.getContext('2d');
        if (expCtx) {
            if (expenseChart) expenseChart.destroy();
            expenseChart = new Chart(expCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Infrastructure', 'Payroll', 'R&D', 'Marketing', 'Logistics'],
                    datasets: [{
                        data: [35, 25, 20, 12, 8],
                        backgroundColor: ['#00F2FE', '#7F00FF', '#10B981', '#F59E0B', '#F43F5E'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { color: textColor, font: { size: 11 } } } }
                }
            });
        }
    }

    setTimeout(initCharts, 100);

    // 7. Dynamic Anomaly Feed Generator
    function renderAnomalyFeed() {
        const feedContainer = document.getElementById('anomaly-feed-list');
        if (!feedContainer) return;

        feedContainer.innerHTML = appState.anomalies.map(item => `
            <div class="feed-item">
                <div class="feed-left">
                    <span class="dot ${item.level === 'warning' ? 'amber' : item.level === 'success' ? 'green' : 'blue'}"></span>
                    <span class="feed-text">${item.text}</span>
                </div>
                <span class="feed-time">${item.time}</span>
            </div>
        `).join('');
    }
    renderAnomalyFeed();

    // 8. AI Co-Pilot Chat Engine
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send-btn');
    const chatMessages = document.getElementById('chat-messages');

    function appendMessage(text, sender = 'bot') {
        if (!chatMessages) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender === 'user' ? 'user-msg' : 'system-msg'}`;
        
        const avatar = sender === 'user' 
            ? `<div class="msg-avatar"><i data-lucide="user"></i></div>`
            : `<div class="msg-avatar"><i data-lucide="cpu"></i></div>`;
            
        msgDiv.innerHTML = `${avatar}<div class="msg-body"><p>${text}</p></div>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        if (window.lucide) lucide.createIcons();
    }

    function processAiQuery(query) {
        appendMessage(query, 'user');

        // Simulate intelligent LLM processing delay
        setTimeout(() => {
            let response = "I have analyzed your query against live enterprise telemetry.";
            const q = query.toLowerCase();

            if (q.includes('revenue') || q.includes('q3')) {
                response = "<strong>Q3 Revenue Synthesis:</strong> Annual Recurring Revenue is currently tracking at <strong>$24.85M (+14.2% YoY)</strong>. Key growth drivers include AI Workflow Automation deployment (+28%) and APAC Logistics node expansion.";
            } else if (q.includes('lead') || q.includes('crm') || q.includes('risk')) {
                response = "<strong>CRM Pipeline Risk Analysis:</strong> 2 high-value opportunities (Apex Global Energy - $450k & Vanguard Aerospace - $1.2M) have AI Win Scores exceeding <strong>88%</strong>. Recommend closing proposal phase by Aug 10.";
            } else if (q.includes('cost') || q.includes('cloud') || q.includes('simulate')) {
                response = "<strong>Cloud Cost Simulation Result:</strong> Reducing staging idle instances by 15% will yield an estimated <strong>$34,200/month</strong> net savings without impacting prod latency (current SLA: 99.99%).";
            } else {
                response = `<strong>Analytical Summary for "${query}":</strong> Operations across all 5 nodes (US-East, US-West, SG-Central, EU-West, Tokyo) are running at 94.8% efficiency. Zero critical security vulnerabilities flagged.`;
            }

            appendMessage(response, 'bot');
        }, 600);
    }

    if (chatSendBtn && chatInput) {
        chatSendBtn.addEventListener('click', () => {
            const val = chatInput.value.trim();
            if (val) {
                processAiQuery(val);
                chatInput.value = '';
            }
        });

        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const val = chatInput.value.trim();
                if (val) {
                    processAiQuery(val);
                    chatInput.value = '';
                }
            }
        });
    }

    // Suggested Pills Click Handler
    document.querySelectorAll('.query-pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const q = pill.getAttribute('data-query');
            processAiQuery(q);
        });
    });

    // 9. ERP Table Logic & Modals
    const erpTableBody = document.getElementById('erp-table-body');
    const erpSearch = document.getElementById('erp-search');
    const erpDeptFilter = document.getElementById('erp-dept-filter');
    const erpStatusFilter = document.getElementById('erp-status-filter');

    function renderErpTable() {
        if (!erpTableBody) return;

        const searchVal = (erpSearch?.value || '').toLowerCase();
        const deptVal = erpDeptFilter?.value || 'ALL';
        const statusVal = erpStatusFilter?.value || 'ALL';

        const filtered = appState.erpAssets.filter(item => {
            const matchesSearch = item.name.toLowerCase().includes(searchVal) || item.id.toLowerCase().includes(searchVal) || item.location.toLowerCase().includes(searchVal);
            const matchesDept = deptVal === 'ALL' || item.dept === deptVal;
            const matchesStatus = statusVal === 'ALL' || item.status === statusVal;
            return matchesSearch && matchesDept && matchesStatus;
        });

        erpTableBody.innerHTML = filtered.map(item => `
            <tr>
                <td><strong class="font-mono">${item.id}</strong></td>
                <td>${item.name}</td>
                <td><span class="badge badge-subtle">${item.dept}</span></td>
                <td>${item.location}</td>
                <td>${item.qty}</td>
                <td><span class="status-pill ${item.status.toLowerCase()}">${item.status}</span></td>
                <td>${item.lastAudit}</td>
                <td>
                    <button class="btn btn-ghost btn-sm btn-delete-erp" data-id="${item.id}" title="Delete"><i data-lucide="trash-2"></i></button>
                </td>
            </tr>
        `).join('');

        document.getElementById('erp-showing-count').textContent = `1-${filtered.length}`;
        if (window.lucide) lucide.createIcons();

        // Attach delete triggers
        document.querySelectorAll('.btn-delete-erp').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-id');
                appState.erpAssets = appState.erpAssets.filter(x => x.id !== id);
                saveState();
                renderErpTable();
            });
        });
    }

    renderErpTable();
    if (erpSearch) erpSearch.addEventListener('input', renderErpTable);
    if (erpDeptFilter) erpDeptFilter.addEventListener('change', renderErpTable);
    if (erpStatusFilter) erpStatusFilter.addEventListener('change', renderErpTable);

    // ERP Modal Add
    const modalErp = document.getElementById('modal-erp');
    const btnAddErp = document.getElementById('btn-add-erp-item');
    const formErp = document.getElementById('form-erp');

    if (btnAddErp && modalErp) {
        btnAddErp.addEventListener('click', () => modalErp.classList.add('active'));
    }

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            document.getElementById(modalId)?.classList.remove('active');
        });
    });

    if (formErp) {
        formErp.addEventListener('submit', (e) => {
            e.preventDefault();
            const newAsset = {
                id: `SKU-${Math.floor(1000 + Math.random() * 9000)}`,
                name: document.getElementById('erp-name').value,
                dept: document.getElementById('erp-dept').value,
                location: document.getElementById('erp-location').value,
                qty: document.getElementById('erp-qty').value,
                status: document.getElementById('erp-status').value,
                lastAudit: new Date().toISOString().split('T')[0]
            };
            appState.erpAssets.unshift(newAsset);
            saveState();
            renderErpTable();
            modalErp.classList.remove('active');
            formErp.reset();
        });
    }

    // 10. CRM Kanban Board Logic
    function renderCrmKanban() {
        const stages = ['lead', 'qualification', 'proposal', 'negotiation', 'closed-won'];
        stages.forEach(stage => {
            const container = document.getElementById(`cards-${stage}`);
            const countEl = document.getElementById(`count-${stage}`);
            if (!container) return;

            const stageDeals = appState.crmDeals.filter(d => d.stage === stage);
            if (countEl) countEl.textContent = stageDeals.length;

            container.innerHTML = stageDeals.map(deal => `
                <div class="kanban-card" data-id="${deal.id}">
                    <div class="card-title">${deal.client}</div>
                    <div class="card-value">$${deal.value.toLocaleString()}</div>
                    <div class="card-footer">
                        <span>${deal.owner}</span>
                        <span class="score-badge">AI Score ${deal.score}</span>
                    </div>
                </div>
            `).join('');
        });
    }

    renderCrmKanban();

    // CRM Modal Add
    const modalCrm = document.getElementById('modal-crm');
    const btnAddDeal = document.getElementById('btn-add-deal');
    const formCrm = document.getElementById('form-crm');

    if (btnAddDeal && modalCrm) {
        btnAddDeal.addEventListener('click', () => modalCrm.classList.add('active'));
    }

    if (formCrm) {
        formCrm.addEventListener('submit', (e) => {
            e.preventDefault();
            const newDeal = {
                id: Date.now(),
                client: document.getElementById('crm-client').value,
                value: parseFloat(document.getElementById('crm-value').value) || 100000,
                stage: document.getElementById('crm-stage').value,
                score: parseInt(document.getElementById('crm-score').value) || 80,
                owner: 'Eleanor Vance'
            };
            appState.crmDeals.unshift(newDeal);
            saveState();
            renderCrmKanban();
            modalCrm.classList.remove('active');
            formCrm.reset();
        });
    }

    // 11. Workflow Execution Simulation Trigger
    const btnTestWorkflow = document.getElementById('btn-test-workflow');
    if (btnTestWorkflow) {
        btnTestWorkflow.addEventListener('click', () => {
            btnTestWorkflow.disabled = true;
            btnTestWorkflow.innerHTML = `<i data-lucide="loader-2"></i> Executing Simulation...`;
            if (window.lucide) lucide.createIcons();

            setTimeout(() => {
                alert('✅ Autonomous Workflow Test Completed!\n- Trigger: Latency Spike Detected\n- Decision Engine: Rerouted to SG-Central Partner B\n- Status: 100% Success');
                btnTestWorkflow.disabled = false;
                btnTestWorkflow.innerHTML = `<i data-lucide="play"></i> Test Trigger Execution`;
                if (window.lucide) lucide.createIcons();
            }, 1200);
        });
    }

    // 12. Reset State Button
    const resetStateBtn = document.getElementById('reset-state-btn');
    if (resetStateBtn) {
        resetStateBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to reset all state to default sample metrics?')) {
                localStorage.removeItem('nexus_app_state');
                location.reload();
            }
        });
    }

    // 13. Export Report Generator (Quick Action Download)
    const exportBtn = document.getElementById('btn-quick-export');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            const reportData = {
                title: "Executive Intelligence Report",
                timestamp: new Date().toISOString(),
                telemetry: appState.telemetry,
                erpAssetsCount: appState.erpAssets.length,
                crmDealsTotalValue: appState.crmDeals.reduce((sum, d) => sum + d.value, 0),
                anomalies: appState.anomalies
            };

            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(reportData, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", `nexus_executive_report_${new Date().toISOString().split('T')[0]}.json`);
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
        });
    }
});
