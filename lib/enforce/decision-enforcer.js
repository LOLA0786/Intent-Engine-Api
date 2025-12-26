class DecisionEnforcer {
  constructor({ mode = "shadow", webhookUrl = null, kafkaProducer = null }) {
    this.mode = mode; // shadow | enforce
    this.webhookUrl = webhookUrl;
    this.kafkaProducer = kafkaProducer;
  }

  async act(analysis) {
    const decision = {
      timestamp: new Date().toISOString(),
      action: analysis.coreIntent.action,
      decision: analysis.policyDecision,
      riskLevel: analysis.riskLevel,
      coreIntentHash: analysis.coreIntentHash,
      payloadHash: analysis.payloadHash
    };

    // Emit to Kafka if configured
    if (this.kafkaProducer) {
      await this.kafkaProducer.send({
        topic: "uaal-decisions",
        messages: [{ value: JSON.stringify(decision) }]
      });
    }

    // Send webhook if configured
    if (this.webhookUrl) {
      await fetch(this.webhookUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(decision)
      });
    }

    // ENFORCE MODE: block execution
    if (this.mode === "enforce" && analysis.policyDecision === "DENY") {
      throw new Error(
        `UAAL BLOCKED ACTION: ${analysis.coreIntent.action} (policy violation)`
      );
    }

    return decision;
  }
}

module.exports = DecisionEnforcer;
