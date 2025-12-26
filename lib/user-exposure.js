function perUserExposure(analyses) {
  const users = {};

  for (const a of analyses) {
    const userId = a.userId || "unknown";

    if (!users[userId]) {
      users[userId] = {
        totalExposure: 0,
        deniedActions: 0,
        actions: {}
      };
    }

    if (a.policyDecision === "DENY" && a.payload?.amount) {
      users[userId].totalExposure += a.payload.amount;
      users[userId].deniedActions += 1;
    }

    const action = a.coreIntent.action;
    users[userId].actions[action] =
      (users[userId].actions[action] || 0) + 1;
  }

  return users;
}

module.exports = { perUserExposure };
