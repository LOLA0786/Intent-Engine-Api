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
