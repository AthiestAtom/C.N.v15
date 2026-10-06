const configuredBaseUrl = (window.CITYNEXUS_CONFIG?.apiBaseUrl || "").trim();
const apiBaseLabel = document.getElementById("api-base");
const resultNode = document.getElementById("health-result");
const healthButton = document.getElementById("health-check");

apiBaseLabel.textContent = configuredBaseUrl
  ? `Backend API base URL: ${configuredBaseUrl}`
  : "Backend API base URL is not configured. Set web/config.js before production use.";

healthButton.addEventListener("click", async () => {
  if (!configuredBaseUrl) {
    resultNode.textContent = "No API base URL configured.";
    return;
  }

  try {
    const response = await fetch(`${configuredBaseUrl.replace(/\/$/, "")}/health`);
    const data = await response.json();
    resultNode.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    resultNode.textContent = `Health check failed: ${error}`;
  }
});
