// ========================================================================================
// POLICYCHECK AU - FRONTEND APPLICATION (VANILLA JS)
// ========================================================================================

const APP = {
    currentView: 'dashboard',
    currentScan: null,
    sectors: [],

    // ========================================================================================
    // INITIALIZATION
    // ========================================================================================

    async init() {
        console.log('Initializing PolicyCheck AU...');
        this.setupEventListeners();
        await this.loadSectors();
        this.updateDeadlineCountdown();
        setInterval(() => this.updateDeadlineCountdown(), 60000);
        await this.loadScans();
        await this.updateStats();
    },

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchView(item.dataset.view);
            });
        });

        // Form submission
        document.getElementById('scanForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitScan();
        });

        // Scan history table
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('history-action')) {
                const scanId = e.target.dataset.scanId;
                this.viewScan(scanId);
            }
            if (e.target.classList.contains('app-header')) {
                e.currentTarget.closest('.app-row')?.classList.toggle('expanded');
            }
        });

        // Result buttons
        document.getElementById('teaserBtn')?.addEventListener('click', () => this.viewReport('teaser'));
        document.getElementById('fullBtn')?.addEventListener('click', () => this.viewReport('full'));
        document.getElementById('exportBtn')?.addEventListener('click', () => this.exportJSON());

        // Modal close
        document.querySelector('.modal-close')?.addEventListener('click', () => {
            document.getElementById('reportModal').style.display = 'none';
        });
    },

    // ========================================================================================
    // NAVIGATION & VIEWS
    // ========================================================================================

    switchView(viewName) {
        // Update nav
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.view === viewName);
        });

        // Update views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.toggle('active', view.id === `${viewName}View`);
        });

        this.currentView = viewName;

        // Load view-specific data
        if (viewName === 'history') {
            this.loadScans();
        } else if (viewName === 'reports') {
            this.loadReports();
        }
    },

    // ========================================================================================
    // SECTOR MANAGEMENT
    // ========================================================================================

    async loadSectors() {
        try {
            const response = await fetch('/api/sectors');
            const data = await response.json();
            this.sectors = data.sectors;

            const select = document.getElementById('sectorSelect');
            select.innerHTML = '<option value="">Select sector...</option>';
            data.sectors.forEach(sector => {
                const option = document.createElement('option');
                option.value = sector;
                option.textContent = sector;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading sectors:', error);
        }
    },

    // ========================================================================================
    // SCAN SUBMISSION
    // ========================================================================================

    async submitScan() {
        const url = document.getElementById('urlInput').value.trim();
        const sector = document.getElementById('sectorSelect').value;
        const businessName = document.getElementById('businessInput').value.trim();

        if (!url || !sector) {
            alert('Please fill in URL and sector');
            return;
        }

        // Clear previous results
        document.getElementById('resultsSection').classList.remove('show');
        document.getElementById('progressSection').style.display = 'block';

        // Hide form, show progress
        document.querySelector('.scan-form').style.display = 'none';

        // Initialize progress tracker
        const tracker = document.getElementById('progressTracker');
        tracker.innerHTML = '';

        const steps = [
            { id: 'connecting', label: 'Connecting to website', detail: 'Accessing target website...' },
            { id: 'scraping', label: 'Scanning for privacy policy', detail: 'Searching for privacy policy page...' },
            { id: 'cookies', label: 'Checking cookie policy', detail: 'Looking for cookie consent notices...' },
            { id: 'terms', label: 'Checking terms & conditions', detail: 'Locating terms of service...' },
            { id: 'analyzing', label: 'Analyzing compliance', detail: 'Scanning against 13 Australian Privacy Principles...' },
            { id: 'complete', label: 'Analysis complete', detail: 'Generating compliance report...' }
        ];

        let currentStepIndex = -1;

        steps.forEach((step, index) => {
            const stepEl = document.createElement('div');
            stepEl.className = 'progress-step';
            stepEl.innerHTML = `
                <div class="step-icon">${step.id === 'complete' ? '✅' : '◯'}</div>
                <div class="step-content">
                    <div class="step-label">${step.label}</div>
                    <div class="step-detail">${step.detail}</div>
                </div>
            `;
            tracker.appendChild(stepEl);
        });

        const stepElements = tracker.querySelectorAll('.progress-step');

        // Start scan
        const eventSource = new EventSource(
            `/api/scan?url=${encodeURIComponent(url)}&sector=${encodeURIComponent(sector)}&business_name=${encodeURIComponent(businessName || url)}`
        );

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('SSE Event:', data.step);

            // Update progress
            switch(data.step) {
                case 'connecting':
                case 'scraping':
                case 'cookies':
                case 'terms':
                case 'analyzing':
                    const stepIndex = steps.findIndex(s => s.id === data.step);
                    if (stepIndex > currentStepIndex) {
                        currentStepIndex = stepIndex;
                        // Mark previous step as completed
                        if (currentStepIndex > 0) {
                            stepElements[currentStepIndex - 1].classList.add('completed');
                            stepElements[currentStepIndex - 1].querySelector('.step-icon').textContent = '✓';
                        }
                        // Mark current step as active
                        if (stepElements[currentStepIndex]) {
                            stepElements[currentStepIndex].classList.add('active');
                        }
                    }
                    break;

                case 'complete':
                    eventSource.close();
                    // Mark all steps as completed
                    stepElements.forEach((el, idx) => {
                        if (idx < stepElements.length) {
                            el.classList.add('completed');
                            el.querySelector('.step-icon').textContent = '✓';
                        }
                    });
                    // Display results
                    setTimeout(() => {
                        this.displayResults(data.result);
                    }, 300);
                    break;

                case 'privacy_not_found':
                    // Show warning but continue
                    console.warn('No privacy policy found');
                    break;

                case 'error':
                    eventSource.close();
                    alert('Scan failed: ' + data.message);
                    document.getElementById('progressSection').style.display = 'none';
                    document.querySelector('.scan-form').style.display = 'block';
                    break;
            }
        };

        eventSource.onerror = (error) => {
            console.error('SSE Error:', error);
            eventSource.close();
            alert('Connection error during scan');
            document.getElementById('progressSection').style.display = 'none';
            document.querySelector('.scan-form').style.display = 'block';
        };
    },

    // ========================================================================================
    // RESULTS DISPLAY
    // ========================================================================================

    displayResults(result) {
        if (!result || !result.analysis) {
            console.error('Invalid result format');
            return;
        }

        const analysis = result.analysis;
        this.currentScan = result;

        // Update header
        document.getElementById('resultBusiness').textContent = result.business_name || 'N/A';
        document.getElementById('resultSector').textContent = result.sector || 'N/A';
        document.getElementById('resultURL').textContent = result.url;
        document.getElementById('resultDate').textContent = new Date(analysis.analysis_date).toLocaleDateString();

        // Update score gauge
        const score = analysis.overall_score;
        const radius = 60;
        const circumference = 2 * Math.PI * radius;
        const progress = (score / 100) * circumference;
        const color = score >= 60 ? '#16a085' : score >= 30 ? '#f39c12' : '#e74c3c';

        document.getElementById('scoreText').textContent = score;
        document.getElementById('scoreCircle').setAttribute('stroke', color);
        document.getElementById('scoreCircle').style.strokeDasharray = `${progress},${circumference}`;

        // Update summary
        document.getElementById('summaryCompliant').textContent = analysis.summary.compliant_count;
        document.getElementById('summaryPartial').textContent = analysis.summary.partial_count;
        document.getElementById('summaryNonCompliant').textContent = analysis.summary.non_compliant_count;
        document.getElementById('summaryNotAddressed').textContent = analysis.summary.not_addressed_count;

        // Render apps
        this.renderApps(analysis.apps);

        // Show ADM warning if needed
        const admWarning = document.getElementById('admWarning');
        if (analysis.adm_check && !analysis.adm_check.adm_disclosed) {
            admWarning.style.display = 'flex';
            document.getElementById('admText').textContent = analysis.adm_check.recommendation;
        } else {
            admWarning.style.display = 'none';
        }

        // Show results section
        document.getElementById('progressSection').style.display = 'none';
        document.getElementById('resultsSection').classList.add('show');

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
    },

    renderApps(apps) {
        const container = document.getElementById('appsContainer');
        container.innerHTML = '';

        apps.forEach((app, index) => {
            const statusClass = app.status.toLowerCase().replace('_', '-');
            const statusLabel = this.formatStatus(app.status);

            const row = document.createElement('div');
            row.className = 'app-row';
            row.innerHTML = `
                <div class="app-header">
                    <div class="app-number">APP ${app.app_number}</div>
                    <div class="app-details">
                        <div class="app-name">${app.app_name}</div>
                    </div>
                    <div class="app-status-badge ${statusClass}">${statusLabel}</div>
                    <div class="app-toggle">▼</div>
                </div>
                <div class="app-content">
                    ${app.findings.length > 0 ? `
                        <div class="content-section">
                            <div class="content-label">Findings</div>
                            <ul class="findings-list">
                                ${app.findings.map(f => `<li>${this.escapeHtml(f)}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${app.gaps.length > 0 ? `
                        <div class="content-section">
                            <div class="content-label">Gaps</div>
                            <div class="gaps-tags">
                                ${app.gaps.map(g => `<div class="gap-tag">${this.escapeHtml(g)}</div>`).join('')}
                            </div>
                        </div>
                    ` : ''}

                    ${app.recommended_language ? `
                        <div class="content-section">
                            <div class="content-label">Recommended Language</div>
                            <div class="recommended">${this.escapeHtml(app.recommended_language)}</div>
                        </div>
                    ` : ''}

                    ${app.priority ? `
                        <div class="content-section">
                            <div class="content-label">Priority</div>
                            <div>${this.escapeHtml(app.priority)}</div>
                        </div>
                    ` : ''}
                </div>
            `;

            row.querySelector('.app-header').addEventListener('click', () => {
                row.classList.toggle('expanded');
            });

            container.appendChild(row);
        });
    },

    // ========================================================================================
    // REPORTS
    // ========================================================================================

    async viewReport(type) {
        if (!this.currentScan) {
            alert('No scan to report');
            return;
        }

        const scanId = this.currentScan.scan_id;
        const url = `/api/report/${scanId}/${type}`;

        try {
            const response = await fetch(url);
            const html = await response.text();

            const modal = document.getElementById('reportModal');
            const container = document.getElementById('reportContainer');
            container.innerHTML = html;
            modal.style.display = 'flex';
        } catch (error) {
            console.error('Error loading report:', error);
            alert('Failed to load report');
        }
    },

    exportJSON() {
        if (!this.currentScan) {
            alert('No scan to export');
            return;
        }

        const dataStr = JSON.stringify(this.currentScan, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `compliance-scan-${this.currentScan.scan_id}.json`;
        link.click();
        URL.revokeObjectURL(url);
    },

    // ========================================================================================
    // SCAN HISTORY
    // ========================================================================================

    async loadScans() {
        try {
            const response = await fetch('/api/scans');
            const data = await response.json();
            this.renderScanHistory(data.scans);
        } catch (error) {
            console.error('Error loading scans:', error);
        }
    },

    renderScanHistory(scans) {
        const tbody = document.getElementById('historyTableBody');
        const emptyMsg = document.getElementById('emptyHistory');

        if (!scans || scans.length === 0) {
            emptyMsg.style.display = 'block';
            tbody.innerHTML = '';
            return;
        }

        emptyMsg.style.display = 'none';
        tbody.innerHTML = '';

        scans.forEach(scan => {
            const row = document.createElement('tr');
            const date = new Date(scan.started_at).toLocaleDateString();
            const score = scan.score !== null ? scan.score : '--';
            const status = scan.compliance_status || 'Pending';

            row.innerHTML = `
                <td>${date}</td>
                <td>${this.escapeHtml(scan.business_name || 'N/A')}</td>
                <td>${this.escapeHtml(scan.sector)}</td>
                <td>${score}</td>
                <td><span class="app-status-badge ${status.toLowerCase().replace('_', '-')}">${this.formatStatus(status)}</span></td>
                <td><button class="history-action" data-scan-id="${scan.scan_id}">View</button></td>
            `;
            tbody.appendChild(row);
        });
    },

    async viewScan(scanId) {
        try {
            const response = await fetch(`/api/scan/${scanId}`);
            const scan = await response.json();

            // Switch to dashboard and show results
            this.switchView('dashboard');
            document.querySelector('.scan-form').style.display = 'none';
            document.getElementById('progressSection').style.display = 'none';

            this.displayResults(scan.result);
        } catch (error) {
            console.error('Error loading scan:', error);
            alert('Failed to load scan');
        }
    },

    // ========================================================================================
    // REPORTS VIEW
    // ========================================================================================

    async loadReports() {
        try {
            const response = await fetch('/api/scans');
            const data = await response.json();
            const container = document.getElementById('reportsContainer');
            const emptyMsg = document.getElementById('emptyReports');

            const completedScans = data.scans.filter(s => s.status === 'complete');

            if (completedScans.length === 0) {
                emptyMsg.style.display = 'block';
                container.innerHTML = '';
                return;
            }

            emptyMsg.style.display = 'none';
            container.innerHTML = '';

            completedScans.forEach(scan => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div>
                            <h3 style="margin: 0 0 4px 0;">${this.escapeHtml(scan.business_name)}</h3>
                            <p style="margin: 0; font-size: 12px; color: #8c8c8d;">${scan.sector} • ${new Date(scan.started_at).toLocaleDateString()}</p>
                        </div>
                        <div style="font-size: 24px; font-weight: 700; color: ${scan.score >= 60 ? '#16a085' : scan.score >= 30 ? '#f39c12' : '#e74c3c'};">${scan.score}</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn btn-secondary" onclick="APP.openReport('${scan.scan_id}', 'teaser')">Teaser</button>
                        <button class="btn btn-secondary" onclick="APP.openReport('${scan.scan_id}', 'full')">Full</button>
                    </div>
                `;
                container.appendChild(card);
            });
        } catch (error) {
            console.error('Error loading reports:', error);
        }
    },

    async openReport(scanId, type) {
        const url = `/api/report/${scanId}/${type}`;
        try {
            const response = await fetch(url);
            const html = await response.text();
            const modal = document.getElementById('reportModal');
            const container = document.getElementById('reportContainer');
            container.innerHTML = html;
            modal.style.display = 'flex';
        } catch (error) {
            console.error('Error loading report:', error);
            alert('Failed to load report');
        }
    },

    // ========================================================================================
    // STATS
    // ========================================================================================

    async updateStats() {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();

            document.getElementById('statTotalScans').textContent = stats.total_scans;
            document.getElementById('statAvgScore').textContent = stats.average_score;
            document.getElementById('statSectors').textContent = stats.sectors_scanned;
            document.getElementById('statViolations').textContent = stats.violations_found;
        } catch (error) {
            console.error('Error updating stats:', error);
        }
    },

    // ========================================================================================
    // DEADLINE COUNTDOWN
    // ========================================================================================

    updateDeadlineCountdown() {
        // Calculate days until July 1, 2026
        const today = new Date();
        const deadline = new Date(2026, 6, 1); // July 1, 2026
        const diffTime = deadline - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        const countdownEl = document.querySelector('.countdown-value');
        if (countdownEl) {
            countdownEl.textContent = Math.max(0, diffDays);
        }
    },

    // ========================================================================================
    // UTILITIES
    // ========================================================================================

    formatStatus(status) {
        const mapping = {
            'COMPLIANT': 'Compliant',
            'PARTIALLY_COMPLIANT': 'Partial',
            'NON_COMPLIANT': 'Non-Compliant',
            'NOT_ADDRESSED': 'Not Addressed',
            'COMPLIANT': 'Compliant',
            'Compliant': 'Compliant',
            'Partial': 'Partial',
            'Non-Compliant': 'Non-Compliant',
            'Not Addressed': 'Not Addressed'
        };
        return mapping[status] || status;
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => APP.init());
