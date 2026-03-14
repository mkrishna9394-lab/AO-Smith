async function loadStationReport() {
  const stationCode = document.getElementById('station_code')?.value || 'ST10';
  const reportDate = document.getElementById('report_date')?.value || new Date().toISOString().split('T')[0];

  const response = await fetch(`/reports/api/station-report?station_code=${encodeURIComponent(stationCode)}&date=${encodeURIComponent(reportDate)}`);
  if (!response.ok) {
    alert('Unable to load report. Check station code and data.');
    return;
  }

  const data = await response.json();
  document.getElementById('completed_batches').textContent = data.completed_batches;
  document.getElementById('delay_count').textContent = data.delay_count;
  document.getElementById('delay_minutes').textContent = `${data.total_delay_minutes} min`;
  document.getElementById('station_name').textContent = `${data.station_code} - ${data.station}`;

  const tbody = document.getElementById('reason_tbody');
  tbody.innerHTML = '';
  if (!data.reasons.length) {
    tbody.innerHTML = '<tr><td colspan="3">No delay reasons found for selected date.</td></tr>';
    return;
  }

  data.reasons.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${row.reason}</td><td>${row.count}</td><td>${row.minutes}</td>`;
    tbody.appendChild(tr);
  });
}
