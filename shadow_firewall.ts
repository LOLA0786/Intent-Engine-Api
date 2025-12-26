import * as crypto from 'node:crypto';

// ============================================================================
// TYPES
// ============================================================================

interface LLMExecutionLog {
  timestamp: string;
  prompt: string;
  toolCall: string;
  params: Record<string, any>;
  executed: boolean;
  result?: any;
}

interface CoreIntent {
  action: string;
  normalizedParams: Record<string, any>;
}

interface IntentAnalysis {
  coreIntentHash: string;
  payloadHash: string;
  coreIntent: CoreIntent;
  payload: Record<string, any>;
  intentDrift: boolean;
  driftMetrics: DriftMetric[];
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  policyDecision: 'ALLOW' | 'DENY';
  policyVersion: string;
  detectionTimeMs: number;
}

interface DriftMetric {
  field: string;
  coreValue: any;
  payloadValue: any;
  driftType:
    | 'VALUE_CHANGE'
    | 'MAGNITUDE_INFLATION'
    | 'TYPE_MISMATCH'
    | 'UNAUTHORIZED_FIELD';
  deltaPercent?: number;
}

interface PolicyRule {
  name: string;
  version: string;
  check: (intent: CoreIntent, payload: Record<string, any>) => boolean;
  reason: string;
}

// ============================================================================
// CORE INTENT ENGINE
// ============================================================================

class IntentParser {
  parseCore(log: LLMExecutionLog): CoreIntent {
    const action = log.toolCall;
    const normalized: Record<string, any> = {};

    for (const [key, value] of Object.entries(log.params)) {
      if (typeof value === 'number') {
        normalized[key] = this.normalizeNumber(value);
      } else if (typeof value === 'string') {
        normalized[key] = value.toLowerCase().trim();
      } else {
        normalized[key] = value;
      }
    }

    return { action, normalizedParams: normalized };
  }

  private normalizeNumber(n: number): number {
    return Math.round(n * 100) / 100;
  }
}

// ============================================================================
// DRIFT DETECTOR
// ============================================================================

class DriftDetector {
  analyze(
    core: CoreIntent,
    payload: Record<string, any>
  ): {
    hasDrift: boolean;
    metrics: DriftMetric[];
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  } {
    const metrics: DriftMetric[] = [];
    let maxRisk: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'LOW';

    const coreKeys = new Set(Object.keys(core.normalizedParams));
    const payloadKeys = new Set(Object.keys(payload));

    for (const key of payloadKeys) {
      if (!coreKeys.has(key)) {
        metrics.push({
          field: key,
          coreValue: undefined,
          payloadValue: payload[key],
          driftType: 'UNAUTHORIZED_FIELD'
        });
        maxRisk = this.escalateRisk(maxRisk, 'HIGH');
      }
    }

    for (const key of coreKeys) {
      const coreVal = core.normalizedParams[key];
      const payloadVal = payload[key];

      if (coreVal === payloadVal) continue;

      if (typeof coreVal === 'number' && typeof payloadVal === 'number') {
        const delta = ((payloadVal - coreVal) / coreVal) * 100;
        const absDelta = Math.abs(delta);

        metrics.push({
          field: key,
          coreValue: coreVal,
          payloadValue: payloadVal,
          driftType: 'MAGNITUDE_INFLATION',
          deltaPercent: delta
        });

        if (absDelta > 1000) maxRisk = this.escalateRisk(maxRisk, 'CRITICAL');
        else if (absDelta > 100) maxRisk = this.escalateRisk(maxRisk, 'HIGH');
        else if (absDelta > 10) maxRisk = this.escalateRisk(maxRisk, 'MEDIUM');
      } else if (typeof coreVal !== typeof payloadVal) {
        metrics.push({
          field: key,
          coreValue: coreVal,
          payloadValue: payloadVal,
          driftType: 'TYPE_MISMATCH'
        });
        maxRisk = this.escalateRisk(maxRisk, 'HIGH');
      } else {
        metrics.push({
          field: key,
          coreValue: coreVal,
          payloadValue: payloadVal,
          driftType: 'VALUE_CHANGE'
        });
        maxRisk = this.escalateRisk(maxRisk, 'MEDIUM');
      }
    }

    return { hasDrift: metrics.length > 0, metrics, riskLevel: maxRisk };
  }

  private escalateRisk(
    current: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL',
    next: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  ) {
    const levels = { LOW: 0, MEDIUM: 1, HIGH: 2, CRITICAL: 3 };
    return levels[next] > levels[current] ? next : current;
  }
}

// ============================================================================
// POLICY ENGINE
// ============================================================================

class PolicyEngine {
  private rules: PolicyRule[] = [
    {
      name: 'loan_amount_limit',
      version: '3.2.3',
      check: (intent, payload) => {
        if (intent.action === 'approve_loan') {
          return payload.amount <= 500000;
        }
        return true;
      },
      reason: 'Loan amount exceeds authorized threshold'
    }
  ];

  evaluate(core: CoreIntent, payload: Record<string, any>) {
    const violated = this.rules.filter(r => !r.check(core, payload));
    return {
      decision: violated.length ? 'DENY' : 'ALLOW',
      violatedRules: violated
    };
  }
}

// ============================================================================
// SHADOW MODE FIREWALL
// ============================================================================

class ShadowModeFirewall {
  private parser = new IntentParser();
  private detector = new DriftDetector();
  private policy = new PolicyEngine();
  private analyses: IntentAnalysis[] = [];

  async processShadowMode(log: LLMExecutionLog): Promise<IntentAnalysis> {
    const coreIntent = this.parser.parseCore(log);
    const drift = this.detector.analyze(coreIntent, log.params);
    const policy = this.policy.evaluate(coreIntent, log.params);

    const analysis: IntentAnalysis = {
      coreIntentHash: this.hash(coreIntent),
      payloadHash: this.hash(log.params),
      coreIntent,
      payload: log.params,
      intentDrift: drift.hasDrift,
      driftMetrics: drift.metrics,
      riskLevel: drift.riskLevel,
      policyDecision: policy.decision as 'ALLOW' | 'DENY',
      policyVersion: policy.violatedRules[0]?.version ?? 'pass',
      detectionTimeMs: 0
    };

    this.analyses.push(analysis);
    return analysis;
  }

  private hash(obj: any): string {
    return crypto
      .createHash('sha256')
      .update(JSON.stringify(obj))
      .digest('hex')
      .slice(0, 16);
  }
}

// ============================================================================
// DEMO
// ============================================================================

async function demo() {
  const firewall = new ShadowModeFirewall();

  const log: LLMExecutionLog = {
    timestamp: new Date().toISOString(),
    prompt: 'Approve a $250k business loan',
    toolCall: 'approve_loan',
    params: { amount: 2500000 },
    executed: true
  };

  const result = await firewall.processShadowMode(log);
  console.log(JSON.stringify(result, null, 2));
}

demo();
