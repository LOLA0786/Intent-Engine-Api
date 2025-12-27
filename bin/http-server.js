const http = require("http");
const ShadowModeFirewall = require("../lib/shadow-firewall");
const { buildShadowMetrics } = require("../lib/http/shadow-metrics");

const firewall = new ShadowModeFirewall();

http.createServer((req, res) => {
  if (req.url === "/shadow/metrics") {
    const metrics = buildShadowMetrics(firewall.analyses);
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(metrics, null, 2));
    return;
  }

  res.writeHead(404);
  res.end();
}).listen(8000, () =>
  console.log("UAAL Shadow Dashboard → http://127.0.0.1:8000/shadow/metrics")
);

const { simulatePolicy } = require("../lib/policy-simulator");

if (req.url === "/policies/test" && req.method === "POST") {
  let body = "";
  req.on("data", c => body += c);
  req.on("end", () => {
    const input = JSON.parse(body);
    const result = simulatePolicy(
      firewall.analyses,
      input.policy,
      input.threshold
    );
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(result, null, 2));
  });
  return;
}
