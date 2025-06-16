const askBtn = document.getElementById("askBtn");
const copyBtn = document.getElementById("copyBtn");
const questionInput = document.getElementById("question");
const topicSelect = document.getElementById("topic");
const answerBox = document.getElementById("answer");
const loading = document.getElementById("loading");

askBtn.addEventListener("click", async () => {
  const question = questionInput.value.trim();
  const topic = topicSelect.value;

  if (!question) {
    alert("Please enter a question.");
    return;
  }

  answerBox.textContent = "";
  loading.classList.remove("hidden");

  try {
    const response = await fetch("https://wi8e1yzkm5.execute-api.ap-south-1.amazonaws.com/prod/claude", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, topic }),
    });

    if (!response.ok) throw new Error("Claude API failed.");

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      answerBox.textContent += decoder.decode(value);
    }

  } catch (error) {
    answerBox.textContent = "⚠️ Error: " + error.message;
  } finally {
    loading.classList.add("hidden");
  }
});

copyBtn.addEventListener("click", () => {
  navigator.clipboard.writeText(answerBox.textContent)
    .then(() => alert("Copied to clipboard!"))
    .catch(() => alert("Failed to copy."));
});
