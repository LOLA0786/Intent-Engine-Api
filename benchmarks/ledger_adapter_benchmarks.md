# Ledger Adapter Benchmarks (Real-Network Baselines)

This document captures **real-network performance baselines** for ledger adapters used by the
Intent Engine audit layer. These are **not mocks**.

Sources include:
- IEEE / arXiv papers (2024–2025)
- Hyperledger Caliper reports
- AWS QLDB documentation & performance notes
- Cosmos SDK / Tendermint ecosystem benchmarks

Workload profile:
- Audit-style payloads (JSON intent + decision)
- Submit (write) + ID-based query (read)
- Moderate enterprise scale (4–16 nodes, EC2-class hardware)
- Bursty traffic (100–1k ops typical; shadow-mode spikes higher)

---

## Baseline Performance (Moderate Load)

| Ledger | Avg Latency (Submit + Query) | Peak TPS | Notes |
|------|------------------------------|----------|-------|
| Fabric | ~1,500 ms (submit ~2s; query <200 ms) | 2k–3k (20k tuned) | Multi-org consensus; latency spikes under load |
| Besu / Quorum | ~450 ms (writes 300–500 ms) | 1k–3k | Private txs; gas limits bottleneck |
| AWS QLDB | ~200 ms | 3k+ | Serverless; no consensus drag |
| Cosmos SDK | ~400 ms | 10k+ | Instant finality; horizontal scale |
| WORM (local) | **0.23 ms** | ~8.4k | Single-node; tamper-evident |

### WORM Local Measurement
- Method: Python REPL, 100 cycles
- Operation: append SHA-256 hash + linear scan query
- Result: total 23.58 ms (100 ops)
- Submit: ~0.11 ms
- Query: ~0.12 ms

---

## High-Load Benchmarks (1k–10k TPS Bursts)

| Ledger | Sustained TPS | Latency Under Load (ms) | Notes |
|------|---------------|--------------------------|-------|
| Fabric | 2k–3k | 5,000–38,000 | Consensus tax dominates |
| Besu / Quorum | 200–1k | 300–500 | Privacy tx overhead ~20% |
| AWS QLDB | 3k+ | 100–200 | Horizontally scalable |
| Cosmos SDK | 10k–60k | 400–500 | BFT + instant finality |
| WORM (local) | ~775 | <1 ms | IO-bound; linear scan |

---

## Engineering Implications

- **Lowest latency:** WORM, QLDB
- **Highest distributed throughput:** Cosmos SDK
- **Strongest multi-party audit:** Fabric
- **Best fintech balance:** QLDB / Besu
- **Shadow-mode bursts:** Cosmos or WORM + periodic anchoring

---

## Routing Guidance (Internal)

Recommended routing via `LEDGER_TYPE`:
- `worm` → local dev, air-gapped, fail-safe default
- `qldb` → low-latency regulated environments
- `fabric` → multi-org compliance proofs
- `cosmos` → public timestamp anchoring, high-TPS spikes

---

## Caveats

- Performance varies with configuration (Raft vs PBFT, node count).
- Fabric latency can spike >15x under contention.
- QLDB scheduled EOL (July 2025): journal export required for long-term audits.
- Cosmos benchmarks assume healthy gossip + validator set <100.

For reproducible local tests:
- Fabric / Besu: Hyperledger Caliper
- Cosmos: gaiad stress / tx flooding
- WORM: local REPL tests (see `tests/test_worm.py`)

---

## Solana Performance Notes (Public High-Throughput Chain)

Solana represents a **distinct performance class** compared to EVM, Fabric, and Cosmos:
single global state, leader-based execution (PoH + Tower BFT), and extreme parallelism.

### Observed Performance (2024–2025)

| Metric | Solana |
|------|--------|
| Sustained TPS (realistic) | 2,000–5,000 |
| Burst TPS (theoretical) | 50k–65k+ |
| Avg Write Latency | 400–800 ms |
| Finality | ~400 ms |
| Read Latency | <10 ms |
| Failure Mode | Leader stalls / state contention |

Sources: Solana Labs reports, Firedancer benchmarks, Jump Crypto analyses, post-2024 mainnet incident reviews.

---

### Engineering Interpretation

- **Strength:** Extremely high throughput for append-style workloads.
- **Weakness:** Global state contention; outages under pathological load.
- **Audit Suitability:** Good for *public anchoring* of hashes, not as a primary audit store.
- **Reliability Tradeoff:** Faster than Ethereum L1, less predictable than Cosmos/Fabric under stress.

---

### Comparison vs Ethereum & Cosmos

- **Solana vs Ethereum L1**
  - Solana: 5–10× throughput, lower latency
  - Ethereum: stronger decentralization, higher latency variance
- **Solana vs Ethereum L2**
  - Comparable throughput
  - L2s win on reliability + tooling
- **Solana vs Cosmos**
  - Solana: higher raw TPS
  - Cosmos: better fault isolation via app-chains

---

### Recommended Usage in Intent Engine

- ❌ Not recommended for internal shadow-mode auditing
- ⚠️ Not suitable for regulator-grade evidence alone
- ✅ Suitable for:
  - Public hash anchoring
  - Viral / DeFi-facing proofs
  - Periodic anchoring of WORM / QLDB digests

**Pattern:**  
WORM / QLDB (primary evidence) → batched hash → Solana tx (public timestamp)

---

### Risk Notes

- Mainnet outages still occur (reduced but non-zero).
- Performance claims assume no global state hot-spotting.
- Firedancer client may materially change this profile post-2025.


---

## Ethereum L2 Performance Notes (Rollup-Based Scaling)

Ethereum Layer 2s (Optimistic and ZK rollups) represent the **most production-stable public scaling path**
for audit anchoring workloads. They inherit Ethereum’s security while avoiding L1 mempool contention.

Benchmarks below reflect **2024–2025 production measurements** from Arbitrum, Optimism, Base,
and zkSync Era under audit-like workloads (append hash + query by tx_hash).

### Observed Performance (Production L2s)

| L2 | Sustained TPS | Avg Write Latency | Finality (Economic) | Notes |
|---|---|---|---|---|
| Arbitrum One | 2k–4k | 200–400 ms | ~7 min (L1 settle) | Most mature; strong tooling |
| Optimism | 1k–2k | 300–500 ms | ~7 min | Stable, conservative upgrades |
| Base | 2k–3k | 200–400 ms | ~7 min | Coinbase infra; fast reads |
| zkSync Era | 2k–5k | 300–600 ms | ~10–20 min | ZK proofs; higher variance |

Sources: L2beat analytics, OP Stack reports, Arbitrum Nitro benchmarks, zkSync technical blog, 2024–2025 postmortems.

---

### Engineering Interpretation

- **Strength:** High throughput + predictable latency under load.
- **Security Model:** Inherits Ethereum L1 security (fraud proofs / validity proofs).
- **Cost Profile:** Orders of magnitude cheaper than L1.
- **Reliability:** Significantly more stable than Ethereum mainnet during spikes.

---

### Comparison vs Other Ledgers

- **vs Ethereum L1**
  - L2s avoid mempool wars and latency explosions.
  - L1 remains too volatile for frequent audit writes.
- **vs Solana**
  - Solana offers higher raw TPS.
  - L2s win on reliability, uptime, and enterprise trust.
- **vs Cosmos**
  - Cosmos better for sovereign app-chains.
  - L2s better for public, shared trust anchoring.

---

### Recommended Usage in Intent Engine

- ✅ Public-facing audit proofs
- ✅ DeFi / ecosystem-integrated agents
- ✅ Batched anchoring of internal evidence

**Preferred Pattern:**  
WORM / QLDB / Fabric → batch hash (N=100–1000) → Ethereum L2 tx → Ethereum L1 settlement

This preserves:
- low operational latency
- public verifiability
- cost control
- regulatory defensibility

---

### Risk Notes

- Finality is delayed until L1 settlement (minutes, not seconds).
- Sequencer centralization still exists (mitigated via decentralization roadmaps).
- ZK rollups trade latency predictability for cryptographic finality.

For audit evidence, **economic finality is sufficient**; cryptographic finality is optional.

