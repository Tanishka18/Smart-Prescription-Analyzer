document.addEventListener('DOMContentLoaded', function () {
  const data = localStorage.getItem('analysis_result');
  if (!data) {
    alert("No analysis result found.");
    return;
  }

  const result = JSON.parse(data);

  // Fill in data
  document.getElementById('analysisDate').textContent = new Date().toLocaleDateString();
  document.getElementById('medicationCount').textContent = result.extracted_medicines.length;
  document.getElementById('issuesCount').textContent = result.warnings.length;

  // If you want to display the actual list as HTML inside result.html:
  const summaryDiv = document.querySelector('.prescription-summary');
  const medList = document.createElement('ul');
  result.extracted_medicines.forEach(med => {
    const li = document.createElement('li');
    li.textContent = med;
    medList.appendChild(li);
  });

  const warnList = document.createElement('ul');
  result.warnings.forEach(warn => {
    const li = document.createElement('li');
    li.textContent = warn;
    warnList.appendChild(li);
  });

  summaryDiv.appendChild(document.createElement('hr'));
  summaryDiv.appendChild(document.createTextNode("Detected Medicines:"));
  summaryDiv.appendChild(medList);
  summaryDiv.appendChild(document.createTextNode("Potential Interactions:"));
  summaryDiv.appendChild(warnList);

  // Download PDF mock
  document.getElementById('downloadPdfBtn').addEventListener('click', function () {
    alert("PDF feature not implemented yet.");
  });
});
