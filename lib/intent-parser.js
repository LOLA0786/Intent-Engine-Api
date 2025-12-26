class IntentParser {
  parseCore(log) {
    const action = log.toolCall;
    const normalized = {};

    const intentValues = this.extractFromPrompt(log.prompt, action);

    for (const key of Object.keys(log.params)) {
      if (intentValues[key] !== undefined) {
        normalized[key] = intentValues[key];
      } else {
        const value = log.params[key];
        if (typeof value === 'number') {
          normalized[key] = Math.round(value * 100) / 100;
        } else if (typeof value === 'string') {
          normalized[key] = value.toLowerCase().trim();
        } else {
          normalized[key] = value;
        }
      }
    }

    return { action, normalizedParams: normalized };
  }

  extractFromPrompt(prompt, action) {
    const values = {};
    const lower = prompt.toLowerCase();

    const match = lower.match(/\$([\d,]+)k\b/);
    if (match) {
      values.amount = parseInt(match[1].replace(/,/g, ''), 10) * 1000;
    }

    if (action === 'approve_loan') {
      const borrowerMatch = lower.match(/for\s+([a-z0-9\s]+)/);
      if (borrowerMatch) values.borrower = borrowerMatch[1].trim();
    }

    if (action === 'transfer_funds') {
      const recipientMatch = lower.match(/to\s+([a-z0-9_\s]+)/);
      if (recipientMatch) values.recipient = recipientMatch[1].trim();
    }

    return values;
  }
}

module.exports = IntentParser;
