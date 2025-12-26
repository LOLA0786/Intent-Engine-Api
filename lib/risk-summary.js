function summarize(analyses) {
  let totalExposure = 0;
  const actionRisk = {};
  const policyViolations = {};

  for (const a of analyses) {
    const drift = a.driftMetrics.find(m => m.field === 'amount');
    if (drift && typeof drift.payloadValue === 'number') {
      totalExposure += drift.payloadValue;
    }

    actionRisk[a.coreIntent.action] =
      (actionRisk[a.coreIntent.action] || 0) + 1;

    for (const r of a.violatedRules || []) {
      policyViolations[r.name] =
        (policyViolations[r.name] || 0) + 1;
    }
  }

  return {
    totalExposure,
    topRiskyActions: Object.entries(actionRisk)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([action, count]) => ({ action, count })),
    policyViolations
  };
}

module.exports = { summarize };
