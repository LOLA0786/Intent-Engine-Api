class GradualEnforcer {
  constructor(config) {
    this.config = config;
  }

  shouldBlock(analysis) {
    if (analysis.policyDecision !== "DENY") return false;

    if (this.config.exceptions?.includes(analysis.payload?.customerType)) {
      return false;
    }

    const roll = Math.random() * 100;
    return roll < this.config.current_percentage;
  }
}

module.exports = GradualEnforcer;
