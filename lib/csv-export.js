function toCSV(analyses) {
  const headers = [
    'timestamp',
    'action',
    'core_amount',
    'payload_amount',
    'delta_percent',
    'risk_level',
    'policy_decision',
    'policy_version',
    'core_intent_hash',
    'payload_hash'
  ];

  const rows = analyses.map(a => {
    const drift = a.driftMetrics.find(m => m.field === 'amount') || {};
    return [
      a.timestamp || '',
      a.coreIntent.action,
      a.coreIntent.normalizedParams.amount ?? '',
      a.payload.amount ?? '',
      drift.deltaPercent ?? '',
      a.riskLevel,
      a.policyDecision,
      a.policyVersion,
      a.coreIntentHash,
      a.payloadHash
    ];
  });

  return [
    headers.join(','),
    ...rows.map(r => r.join(','))
  ].join('\n');
}

module.exports = { toCSV };
