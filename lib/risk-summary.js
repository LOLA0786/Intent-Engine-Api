const { perUserExposure } = require("./user-exposure");
function summarize(analyses) {
  let totalExposure = 0;
  const actionCounts = {};
  const policyViolations = {};

  for (const a of analyses) {
    if (a.policyDecision === 'DENY' && a.payload?.amount) {
      totalExposure += a.payload.amount;
    }

    const action = a.coreIntent?.action || 'unknown';
    actionCounts[action] = (actionCounts[action] || 0) + 1;

    if (a.policyDecision === 'DENY') {
      const rule =
        a.violatedRules?.[0]?.name ||
        `policy_${a.policyVersion || 'unknown'}`;

      policyViolations[rule] = (policyViolations[rule] || 0) + 1;
    }
  }

  return {
    totalExposure,
    topRiskyActions: Object.entries(actionCounts)
      .map(([action, count]) => ({ action, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10),
    policyViolations
  };
perUserExposure: perUserExposure(analyses)}

module.exports = { summarize };
