class CoordinatedDriftDetector {
  constructor(windowMs = 300000, threshold = 3) {
    this.windowMs = windowMs;
    this.threshold = threshold;
    this.events = [];
  }

  record(entityId, action, delta) {
    const now = Date.now();
    this.events.push({ now, entityId, action, delta });

    this.events = this.events.filter(e => now - e.now <= this.windowMs);

    const entities = new Set(
      this.events
        .filter(e => e.action === action && e.delta > 0)
        .map(e => e.entityId)
    );

    return {
      type: 'COORDINATED_DRIFT',
      detected: entities.size >= this.threshold,
      entityCount: entities.size
    };
  }
}

module.exports = CoordinatedDriftDetector;
