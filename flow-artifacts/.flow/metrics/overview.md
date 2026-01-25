# FLOW Metrics

> Measuring stream health and team effectiveness.

## Why Measure?

Without metrics, you're guessing:
- Is FLOW actually working?
- Are we shipping faster?
- Where are the bottlenecks?
- Is agent autonomy helping or hurting?

## Core Metrics

### 1. Throughput

**Definition:** Objectives completed per time period.

| Period | Objectives Completed | By Human | By Agent |
|--------|---------------------|----------|----------|
| This Week | | | |
| Last Week | | | |
| This Month | | | |

**Trend:** <!-- increasing/stable/decreasing -->

---

### 2. Cycle Time

**Definition:** Time from objective start to completion.

| Size | Avg Cycle Time | Target | Status |
|------|----------------|--------|--------|
| XS | | < 4 hours | |
| S | | < 1 day | |
| M | | < 3 days | |
| L | | < 1 week | |

**Bottlenecks:** <!-- Where does time get spent? -->

---

### 3. Flow Efficiency

**Definition:** Active work time / Total time (start to done).

```
Flow Efficiency = Work Time / (Work Time + Wait Time)
```

| Stream | Flow Efficiency | Main Wait Reason |
|--------|-----------------|------------------|
| auth-overhaul | | |
| performance | | |

**Target:** > 40% (knowledge work baseline)

---

### 4. Stream Health

| Stream | Objectives In Progress | Blocked | Avg Age (days) | Health |
|--------|----------------------|---------|----------------|--------|
| | | | | 🟢/🟡/🔴 |

**Health Indicators:**
- 🟢 Green: Flowing well, objectives completing
- 🟡 Yellow: Some blockers, aging objectives
- 🔴 Red: Stalled, needs intervention

---

### 5. Rework Rate

**Definition:** Percentage of completed work that needed revision.

| Category | Count | Rework Count | Rate |
|----------|-------|--------------|------|
| PRs Merged | | | |
| Objectives Completed | | | |

**Acceptable:** < 15%
**Current:** <!-- x% -->

---

### 6. Agent Effectiveness

| Agent | Objectives | Avg Cycle Time | Rework Rate | Autonomy Level |
|-------|------------|----------------|-------------|----------------|
| @developer | | | | 3 |
| claude-main | | | | 2 |

**Insights:** <!-- What's working? What's not? -->

---

## Stream-Level Metrics

### [Stream Name]

```
Started:        [date]
Target:         [date]
Objectives:     [completed] / [total]
Cycle Time Avg: [days]
Blockers:       [count]
```

---

## Trends

### Weekly Throughput

```
Week of 01/06: ████████░░ 8 objectives
Week of 01/13: ██████████ 10 objectives
Week of 01/20: ███████░░░ 7 objectives
Week of 01/27: ████░░░░░░ 4 objectives (in progress)
```

### Cycle Time Trend

```
Week of 01/06: 2.3 days avg
Week of 01/13: 1.8 days avg ↓
Week of 01/20: 2.1 days avg ↑
Week of 01/27: 1.5 days avg ↓
```

---

## Alerts

Define thresholds that trigger attention:

| Metric | Threshold | Current | Status |
|--------|-----------|---------|--------|
| Blocked objectives | > 3 | | |
| Avg cycle time | > 5 days | | |
| Rework rate | > 20% | | |
| Pool size | > 20 | | |

---

## Collection

### Automatic

These can be calculated from git/GitHub:
- PR merge frequency
- Commit frequency
- Time between commits

### Manual Update

Update weekly:
- Objective completion counts
- Stream health assessment
- Blocker analysis
- Rework identification

### Update Command

`/flow-metrics` - Calculate and update metrics:

```markdown
---
description: Update FLOW metrics
---

Calculate and update metrics:

1. Count completed objectives (check streams/completed/ and stream files)
2. Calculate cycle times from objective work logs
3. Identify blocked objectives and duration
4. Assess stream health
5. Update this file with current data
6. Highlight any alerts triggered
```

---

## Using Metrics

### In Triage

Use throughput and cycle time to estimate capacity:
- "We complete ~8 M-sized objectives per week"
- "This L objective will likely take 5-7 days"

### In Retrospectives

Use trends to identify improvements:
- "Cycle time decreased after we added X"
- "Rework rate spiked when we rushed Y"

### In Agent Tuning

Use agent metrics to adjust autonomy:
- "claude-main's rework rate is low, promote to level 2"
- "Agent X keeps getting blocked, needs more guidance"
