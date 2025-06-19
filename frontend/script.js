const roastBtn = document.getElementById('roast-btn');
const roastOutput = document.getElementById('roast-output');

roastBtn.addEventListener('click', async () => {
  roastBtn.disabled = true;
  roastOutput.textContent = "Cooking up a roast... 🔥";

  try {
    // Use Puter.js GPT-4o model to generate a roast
    const response = await puter.ai.chat("Write a funny, clever roast about someone who always loses at memes.");

    roastOutput.textContent = response;

    // Send roast to your backend to push to Telegram or Instagram
    await fetch('http://YOUR_BACKEND_URL/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: response })
    });
  } catch (err) {
    roastOutput.textContent = "Oops! Something went wrong. Try again.";
    console.error(err);
  } finally {
    roastBtn.disabled = false;
  }
});
