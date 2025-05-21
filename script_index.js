document.getElementById("analyzeBtn").addEventListener("click", () => {
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload a prescription image.");
    return;
  }
  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("results").classList.add("hidden");

  // Simulate OCR + drug analysis (replace with real logic/API call)
  setTimeout(() => {
    const medications = ["Paracetamol", "Ibuprofen", "Omeprazole"];
    const flagged = [
      { drug: "Paracetamol", reason: "Duplicate drug detected" },
      { drug: "Ibuprofen", reason: "Potential interaction with Omeprazole" }
    ];

    document.getElementById("loading").classList.add("hidden");
    document.getElementById("results").classList.remove("hidden");

    // Populate medication list
    const medList = document.getElementById("medicationsList");
    medList.innerHTML = "";
    medications.forEach(med => {
      const li = document.createElement("li");
      li.textContent = med;
      medList.appendChild(li);
    });

    // Populate alerts
    const flaggedList = document.getElementById("flaggedList");
    flaggedList.innerHTML = "";
    if (flagged.length > 0) {
      document.getElementById("alerts").classList.remove("hidden");
      flagged.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${item.drug}:</strong> ${item.reason}`;
        flaggedList.appendChild(li);
      });
    } else {
      document.getElementById("alerts").classList.add("hidden");
    }
  }, 2000);
  window.location.href = 'result.html';
});
