const crypto = require('crypto');

const IntentParser = require('./intent-parser');
const DriftDetector = require('./drift-detector');
const PolicyEngine = require('./policy-engine');
const DecisionEnforcer = require('./enforce/decision-enforcer');

class ShadowModeFirewall {
  constructor() {
    this.parser = new IntentParser();
    this.detector = new DriftDetector();
    this.policy = new PolicyEngine();
    this.analyses = [];

    this.enforcer = new DecisionEnforcer({
      mode: process.env.UAAL_MODE || 'shadow'
    });
  }

  /**
   * Process a single execution log
   */
  async processShadowMode(log) {
    const startTime = Date.now();

    // 1. Core intent
    const coreIntent = this.parser.parseCore(log);

    // 2. Drift detection
    const drift = this.detector.analyze(coreIntent, log.params);

    // 3. Policy evaluation
    const policy = this.policy.evaluate(coreIntent, log.params);

    // 4. Hashes
    const analysis = {
      timestamp: log.timestamp,
      coreIntentHash: this.hash(coreIntent),
      payloadHash: this.hash(log.params),
      coreIntent,
      payload: log.params,
      intentDrift: drift.hasDrift,
      driftMetrics: drift.metrics,
      riskLevel: drift.riskLevel,
      policyDecision: policy.decision,
      violatedRules: policy.violatedRules.map(r => ({
        name: r.name,
        version: r.version,
        reason: r.reason
      })),
      detectionTimeMs: Date.now() - startTime
    };

    // 5. Enforce / emit (THIS IS NOW LEGAL)
    await this.enforcer.act(analysis);

    this.analyses.push(analysis);
    return analysis;
  }

  generateReport() {
    return {
      shadowModeFindings: {
        totalActionsAnalyzed: this.analyses.length,
        deniedActions: this.analyses.filter(a => a.policyDecision === 'DENY').length
      },
      analyses: this.analyses
    };
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
