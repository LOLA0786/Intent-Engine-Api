const crypto = require('crypto');
const IntentParser = require('./intent-parser');
const DriftDetector = require('./drift-detector');
const PolicyEngine = require('./policy-engine');

class ShadowModeFirewall {
  constructor() {
    this.parser = new IntentParser();
    this.detector = new DriftDetector();
    this.policy = new PolicyEngine();
    this.analyses = [];
  }

  async processShadowMode(log) {
    const core = this.parser.parseCore(log);
    const drift = this.detector.analyze(core, log.params);
    const policy = this.policy.evaluate(core, log.params);

    const analysis = {
      coreIntentHash: this.hash(core),
      payloadHash: this.hash(log.params),
      coreIntent: core,
      payload: log.params,
      intentDrift: drift.hasDrift,
      driftMetrics: drift.metrics,
      riskLevel: drift.riskLevel,
      policyDecision: policy.decision,
      policyVersion: policy.violatedRules[0]?.version || 'pass'
    };

    this.analyses.push(analysis);
    return analysis;
  }

  hash(obj) {
    return crypto
      .createHash('sha256')
      .update(JSON.stringify(obj))
      .digest('hex')
      .slice(0, 16);
  }
}

module.exports = ShadowModeFirewall;
