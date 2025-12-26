class DriftDetector {
  analyze(core, payload) {
    const metrics = [];
    let maxRisk = 'LOW';

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
        maxRisk = 'HIGH';
      }
    }

    for (const key of coreKeys) {
      const c = core.normalizedParams[key];
      const p = payload[key];
      if (c === p) continue;

      if (typeof c === 'number' && typeof p === 'number') {
        const delta = ((p - c) / c) * 100;
        metrics.push({
          field: key,
          coreValue: c,
          payloadValue: p,
          driftType: 'MAGNITUDE_INFLATION',
          deltaPercent: delta
        });
        if (Math.abs(delta) > 100) maxRisk = 'CRITICAL';
      }
    }

    return { hasDrift: metrics.length > 0, metrics, riskLevel: maxRisk };
  }
}

module.exports = DriftDetector;
