chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "new_posts") {
    chrome.storage.local.get(["userPrefs"], prefs => {
      msg.data.forEach(post => {
        fetch("http://127.0.0.1:8000/analyze_post", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: post, prefs: prefs.userPrefs })
        })
        .then(res => res.json())
        .then(result => {
          if (result.relevant) {
            chrome.notifications.create({
              type: "basic",
              iconUrl: "icon.png",
              title: "找到符合條件的房子！",
              message: result.summary
            });
          }
        })
        .catch(err => console.error("API 錯誤", err));
      });
    });
  }
});
