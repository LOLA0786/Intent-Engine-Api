class UserBaseline {
  constructor() {
    this.stats = new Map();
  }

  update(userId, amount) {
    if (!userId || typeof amount !== 'number') return;

    const s = this.stats.get(userId) || { n: 0, mean: 0, m2: 0 };
    s.n += 1;

    const delta = amount - s.mean;
    s.mean += delta / s.n;
    s.m2 += delta * (amount - s.mean);

    this.stats.set(userId, s);
  }

  zScore(userId, amount) {
    const s = this.stats.get(userId);
    if (!s || s.n < 5) return 0;

    const variance = s.m2 / s.n || 1;
    return (amount - s.mean) / Math.sqrt(variance);
  }
}

module.exports = UserBaseline;
