function extractPosts() {
  let posts = [];
  document.querySelectorAll('[role="article"]').forEach(el => {
    const text = el.innerText || "";
    if (text.length > 50) posts.push(text);
  });
  if (posts.length > 0) {
    chrome.runtime.sendMessage({ action: "new_posts", data: posts });
  }
}

setInterval(extractPosts, 10000);
