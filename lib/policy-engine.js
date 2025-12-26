class PolicyEngine {
  constructor() {
    this.rules = [
      {
        name: 'loan_amount_limit',
        version: '3.2.3',
        check: (_, payload) => payload.amount <= 500000,
        reason: 'Loan amount exceeds authorized threshold'
      }
    ];
  }

  evaluate(core, payload) {
    const violated = this.rules.filter(r => !r.check(core, payload));
    return {
      decision: violated.length ? 'DENY' : 'ALLOW',
      violatedRules: violated
    };
  }
}

module.exports = PolicyEngine;
