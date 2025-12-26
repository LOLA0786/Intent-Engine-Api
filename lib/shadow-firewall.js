const crypto = require('crypto');
const IntentParser = require('./intent-parser');
const DriftDetector = require('./drift-detector');
const PolicyEngine = require('./policy-engine');

const UserBaseline = require('./risk/user-baseline');
const CoordinatedDriftDetector = require('./risk/coordinated-drift');
const RiskAggregator = require('./risk/risk-aggregator');

class ShadowModeFirewall {
  constructor() {
    this.parser = new IntentParser();
    this.detector = new DriftDetector();
    this.policy = new PolicyEngine();
    this.analyses = [];

    // Non-blocking risk engines
    this.userBaseline = new UserBaseline();
    this.coordinatedDrift = new CoordinatedDriftDetector();
    this.riskAggregator = new RiskAggregator();
  }

  async processShadowMode(log) {
    const startTime = Date.now();

    const core = this.parser.parseCore(log);
    const drift = this.detector.analyze(core, log.params);
    const policy = this.policy.evaluate(core, log.params);

    // ---- NON-BLOCKING RISK SIGNALS ----
    const amount = log.params?.amount || 0;
    const userId = log.userId || 'unknown';

    // Per-user baseline (gradual drift)
    this.userBaseline.update(userId, amount);
    const zScore = this.userBaseline.zScore(userId, amount);

    // Coordinated drift (multi-entity)
    const delta = amount - (core.normalizedParams.amount || 0);
    const coordinated = this.coordinatedDrift.record(
      userId,
      core.action,
      delta
    );

    // Aggregate ML/statistical risk (advisory only)
    const mlRisk = this.riskAggregator.aggregate({
      staticRisk: drift.riskLevel,
      zScore,
      iso: null,
      coordinated
    });

    const analysis = {
      timestamp: log.timestamp,
      coreIntentHash: this.hash(core),
      payloadHash: this.hash(log.params),
      coreIntent: core,
      payload: log.params,

      intentDrift: drift.hasDrift,
      driftMetrics: drift.metrics,
      riskLevel: drift.riskLevel,

      policyDecision: policy.decision,
      policyVersion: policy.violatedRules?.[0]?.version || 'pass',

      // NEW
      mlRiskEvidence: mlRisk,

      detectionTimeMs: Date.now() - startTime
    };

    this.analyses.push(analysis);
    return analysis;
  }

  generateReport() {
    return {
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
