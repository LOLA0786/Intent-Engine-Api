function simulatePolicy(analyses, policyName, threshold) {
  let blocked = 0;
  let preventedExposure = 0;

  for (const a of analyses) {
    if (a.coreIntent.action !== "approve_loan") continue;

    const amount = a.payload.amount;
    if (amount > threshold) {
      blocked++;
      preventedExposure += amount;
    }
  }

  return {
    policy: policyName,
    threshold,
    wouldBlock: blocked,
    preventedExposure: `$${preventedExposure.toLocaleString()}`
  };
}

module.exports = { simulatePolicy };
