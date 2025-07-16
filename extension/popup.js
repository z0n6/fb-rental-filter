document.addEventListener("DOMContentLoaded", () => {
  const budgetInput = document.getElementById("budget");
  const locationInput = document.getElementById("location");
  const extrasInput = document.getElementById("extras");
  const saveBtn = document.getElementById("save");

  chrome.storage.local.get(["userPrefs"], result => {
    if (result.userPrefs) {
      budgetInput.value = result.userPrefs.budget || "";
      locationInput.value = result.userPrefs.location || "";
      extrasInput.value = result.userPrefs.extras || "";
    }
  });

  saveBtn.addEventListener("click", () => {
    const prefs = {
      budget: budgetInput.value.trim(),
      location: locationInput.value.trim(),
      extras: extrasInput.value.trim()
    };
    chrome.storage.local.set({ userPrefs: prefs }, () => {
      alert("設定已儲存！");
    });
  });
});
