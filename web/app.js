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

  const apiUrl = `${configuredBaseUrl.replace(/\/$/, "")}/health`;

  resultNode.textContent =
    `Checking backend health...\n${apiUrl}`;

  healthButton.disabled = true;

  try {
    const response = await fetch(apiUrl, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    });

    const body = await response.text();

    let data;
    try {
      data = JSON.parse(body);
    } catch {
      data = body;
    }

    if (!response.ok) {
      resultNode.textContent =
        `Backend returned HTTP ${response.status} ${response.statusText}\n` +
        (typeof data === "string"
          ? data
          : JSON.stringify(data, null, 2));
      return;
    }

    resultNode.textContent =
      typeof data === "string"
        ? data
        : JSON.stringify(data, null, 2);
  } catch (error) {
    resultNode.textContent =
      "Health check failed. The browser could not complete the request.\n" +
      "This can indicate CORS, network/DNS failure, or an unavailable backend.\n\n" +
      String(error);
  } finally {
    healthButton.disabled = false;
  }
});
