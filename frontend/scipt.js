document.getElementById("generateBtn").addEventListener("click", async () => {
  const output = document.getElementById("roastOutput");
  output.innerText = "Generating roast... 🔥";

  try {
    const response = await puter.ai.chat("Give me a short, funny roast", {
      model: "gpt-4o" // or "o3-mini" if you want faster
    });
    output.innerText = response;
  } catch (error) {
    output.innerText = "Something went wrong! 😬";
    console.error(error);
  }
});
