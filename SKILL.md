---
name: protocol-registry-contributor
description: Run a Protocol Bicorder diagnostic on any protocol and submit the reading to the Protocol Institute's shared registry via a GitHub pull request. Use when a user wants to contribute a protocol analysis to the registry, run a bicorder for submission, or add a protocol entry to patwater/protocol-registry-pilot.
---

# Protocol Registry Contributor

This skill lets you conduct a Protocol Bicorder diagnostic interview and submit the result as a structured JSON entry to the Protocol Institute pilot registry at `github.com/patwater/protocol-registry-pilot`. Contributions are reviewed via pull request. Human-reviewed entries are marked as verified; LLM-only submissions are stamped `verified_by: auto`.

The bicorder instrument is built on Nathan Schneider's work at bicorder.ecologies.info (CU Boulder Media Economies Design Lab / Governance Ecologies project). It surfaces the hidden logic beneath a social or technical agreement across 23 gradient axes in three sets: Design, Entanglement, and Experience.

---

## Step 1: Establish the protocol and standpoint

Before scoring any gradients, confirm two things:

1. **What is the protocol?** Get a clear name and 1-3 sentence description. A protocol here means anything patterned: a handshake, a board meeting, a potluck, TCP/IP, a Slack norm, a family ritual, a procurement process.
2. **What is the standpoint?** Who is the analyst, and from what vantage point? (e.g., "designer," "long-time participant," "outsider observer," "the person the protocol is used against.") The same protocol reads very differently from different standpoints -- this is a first-class field, not a footnote.

Ask both questions if they are not clear from context. Do not proceed without them.

---

## Step 2: Choose full or shortform pass

Ask whether the user wants:
- **Full pass** (23 gradients) -- recommended for formal registry submissions, comparative analysis, or when the protocol is the subject of real research.
- **Shortform pass** (~11 gradients, flagged `shortform: true` in the bicorder template) -- fine for exploratory readings or when time is short.

Default to **full** for registry submissions, since that is the purpose of this skill.

---

## Step 3: Conduct the bicorder interview

Work through gradients **one set at a time** (Design → Entanglement → Experience), presenting 2-4 gradients per turn. For each gradient:

- Name both poles (not just the one-word terms -- give the full spectrum description so the analyst can score accurately).
- Ask for a 1-9 score (1 = fully left/first pole, 9 = fully right/second pole, 5 = genuinely mixed).
- Accept qualitative answers and translate them to a number, stating the number you landed on.
- Invite brief notes if the analyst has something to add.

Keep it conversational -- this is an interview, not a form. Light interpretation between gradients is welcome.

### Design gradients (how the protocol is created and remembered)

| Left pole | Right pole | Notes on what to probe |
|---|---|---|
| explicit | implicit | Is the protocol written down, or learned by watching? |
| institutional | organic | Did it emerge from a formal body or from practice? |
| immutable | mutable | How easily does it change? Who can change it? |
| monocultural | multicultural | Does it assume one cultural context or bridge many? |
| exclusive | inclusive | Who is kept out, and how? |
| hierarchical | egalitarian | Does the protocol encode status differences? |
| determined | open | How much room for interpretation does it leave? |
| macro | micro | What scale does it operate at -- systemic or atomic? |

### Entanglement gradients (how the protocol relates to participant agents)

| Left pole | Right pole | Notes on what to probe |
|---|---|---|
| obligatory | optional | Can participants opt out? At what cost? |
| symmetric | asymmetric | Do all participants play the same role? |
| voluntary | coerced | Is participation chosen or required? |
| agentic | passive | How much active judgment do participants exercise? |
| synchronous | asynchronous | Does the protocol require simultaneous participation? |

### Experience gradients (how the protocol is perceived in use)

| Left pole | Right pole | Notes on what to probe |
|---|---|---|
| legible | illegible | Can participants see and understand what is happening? |
| immediate | delayed | How quickly does the protocol resolve? |
| alive | dead | Is it actively used and evolving, or frozen? |
| smooth | rough | Does it feel frictionless or effortful? |
| pleasant | unpleasant | What is the affective experience of participation? |
| natural | artificial | Does it feel organic or imposed? |
| certain | uncertain | How predictable are outcomes? |
| efficient | inefficient | Does it feel like a good use of participants' time and attention? |
| exciting | boring | What is its energy? |
| engaging | disengaging | Does it pull participants in or push them away? |

---

## Step 4: Compute analysis metrics

After all gradients are scored, compute the following:

- **Hardness** = mean of all gradient scores. Values below 5 trend soft/left-pole; values above 5 trend hard/right-pole.
- **Polarized** = measure of how extreme vs. central the readings ran. Compute as the mean absolute deviation from 5, normalized to 0-1: `mean(|score - 5| for each score) / 4`.
- **Formal/informal** = heuristic reconstruction (the real bicorder uses Linear Discriminant Analysis on a private corpus; this is an approximation). Weight the Design gradients more heavily: use the mean of (explicit + institutional + immutable + determined) / 4, normalized. State this is a heuristic when presenting.
- **Usefulness** = ask the analyst directly (1-9). "Was the bicorder useful or revealing for this particular protocol, or did some axes feel irrelevant?"

Generate a plain-text summary bar showing the three set means, e.g.:
```
Design     [========-] 8.0  Entanglement [====-----] 4.3  Experience [======---] 6.1
```

---

## Step 5: Choose the slug and finalize metadata

Derive a `slug` from the protocol name: lowercase, kebab-case, no special characters (e.g., "TCP Three-Way Handshake" → `tcp-three-way-handshake`). Confirm with the user.

Map to lifecycle:
- **budding** -- newly emerging, not yet established
- **juvenile** -- growing, still developing norms
- **mature** -- stable, widely used
- **dead** -- no longer practiced
- **fossilized** -- preserved/referenced but not active

Map to scale:
- **systemic** -- operates at the level of whole systems or institutions
- **meso** -- mid-range, organizational or community level
- **atomic** -- a single interaction or handshake

---

## Step 6: Build the JSON entry

Construct a JSON file conforming to `schema/protocol-entry.schema.json`. The structure is:

```json
{
  "metadata": {
    "name": "...",
    "slug": "...",
    "description": "...",
    "standpoint": "...",
    "lifecycle": "mature|budding|juvenile|dead|fossilized",
    "scale": "systemic|meso|atomic",
    "tags": [],
    "related_protocols": []
  },
  "bicorder": {
    "date": "YYYY-MM-DD",
    "pass_type": "full|shortform",
    "gradients": {
      "explicit": { "score": 7, "notes": "..." },
      "institutional": { "score": 8 },
      ...
    },
    "analysis": {
      "hardness": 5.6,
      "polarized": 0.74,
      "formal_informal": 0.72,
      "usefulness": 7,
      "usefulness_notes": "...",
      "summary_bar": "Design [===] ... Entanglement [===] ... Experience [===] ..."
    }
  },
  "provenance": {
    "submitted_by": "github-username-or-anonymous",
    "submission_method": "llm-assisted|manual|batch-script",
    "llm_model": "claude-sonnet-4-6",
    "verified_by": "auto",
    "verification_date": null,
    "notes": ""
  }
}
```

Set `verified_by: "auto"` as the default. A human reviewer who checks the verification box in the PR template will have their GitHub username stamped in by the merge action.

See `protocols/examples/tcp-three-way-handshake.json` for a complete worked example.

---

## Step 7: Submit the pull request

Tell the user to:

1. **Fork** `github.com/patwater/protocol-registry-pilot`.
2. **Create a branch** named `add/<slug>` (e.g., `add/tcp-three-way-handshake`).
3. **Write the JSON file** to `protocols/<slug>.json`.
4. **Run the validator** locally (optional but recommended): `python scripts/validate.py protocols/<slug>.json`
5. **Open a pull request** against `main` with:
   - Title: `Add: <Protocol Name>`
   - Description: fill out the PR template (generated automatically by GitHub)
   - **Check the human review box** in the PR template if they have personally read and can vouch for the bicorder reading. Leave it unchecked if this is an LLM-generated reading being submitted for community review.

If the user has GitHub CLI (`gh`) available, offer to generate the branch and PR commands directly.

---

## Notes for LLM contributors

- Be honest about LLM limitations on subjective experience gradients (pleasant/unpleasant, exciting/boring). These axes are most meaningful from a human participant's perspective -- note this when scoring them.
- The `standpoint` field is critical. A TCP handshake reads very differently from the perspective of a network engineer vs. an end user who has never heard of it.
- When in doubt on a gradient, score 5 and add a note explaining the ambiguity. A thoughtful 5 is more useful than a confident wrong number.
- Do not invent gradient names not in the schema. The 23 gradients listed above are the complete instrument.
- The formal/informal heuristic is a reconstruction, not the real LDA model. Note this when presenting formal_informal scores to users.
