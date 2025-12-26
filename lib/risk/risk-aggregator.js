class RiskAggregator {
  aggregate({ staticRisk, zScore, iso, coordinated }) {
    const evidence = [];

    if (staticRisk === 'CRITICAL') {
      evidence.push({ source: 'STATIC_DRIFT' });
    }

    if (zScore > 3) {
      evidence.push({ source: 'USER_BASELINE', zScore: zScore.toFixed(2) });
    }

    if (iso?.anomaly) {
      evidence.push({ source: 'ISOLATION_FOREST', score: iso.score });
    }

    if (coordinated?.detected) {
      evidence.push({
        source: 'COORDINATED_DRIFT',
        entities: coordinated.entityCount
      });
    }

    let overallRisk = 'LOW';
    if (evidence.length >= 2) overallRisk = 'HIGH';
    else if (evidence.length === 1) overallRisk = 'MEDIUM';

    return { overallRisk, evidence };
  }
}

module.exports = RiskAggregator;
