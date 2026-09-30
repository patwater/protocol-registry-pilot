# Protocol Registry

An open, community-maintained registry of Protocol Bicorder readings -- a pilot project of the [Protocol Institute](https://protocolize.it).

The Protocol Bicorder is an instrument for studying protocols developed by Nathan Schneider (CU Boulder Media Economies Design Lab) as part of the [Governance Ecologies](https://bicorder.ecologies.info/) project and the Summer of Protocols research program. It surfaces the hidden logic beneath social and technical agreements across 23 gradient axes in three sets: Design, Entanglement, and Experience.

This registry is the shared corpus: anyone can contribute a reading, and pull requests serve as the peer review mechanism.

---

## What goes in here

Any protocol is fair game -- a handshake, a board meeting, a potluck, TCP/IP, a Slack norm, a family ritual, a procurement process, a treaty. The instrument is designed for slowness and depth, not speed-scoring.

Each entry is a JSON file at `protocols/<slug>.json` containing:

- **Metadata** -- name, description, standpoint, lifecycle, scale
- **Bicorder reading** -- all 23 gradient scores with optional analyst notes, plus computed analysis metrics
- **Provenance** -- who submitted it, how (LLM-assisted or manual), and whether a human reviewer has verified it

Entries are marked either `verified_by: <github-username>` (human-reviewed) or `verified_by: auto` (LLM-generated, awaiting community review). Both are welcome contributions to the corpus.

---

## Contributing

### The fast path: use the SKILL.md with your LLM

Load `SKILL.md` into any capable LLM (Claude, GPT-4, Gemini, etc.) and it will walk you through the full bicorder interview, generate the properly formatted JSON, and tell you exactly how to submit the PR.

```
# With Claude Code or similar:
/load SKILL.md
# Then: "Run a bicorder on [your protocol]"
```

### The manual path

1. **Read the schema** at `schema/protocol-entry.schema.json` to understand the required structure.
2. **See the example** at `protocols/examples/tcp-three-way-handshake.json` for a complete worked entry.
3. **Conduct your bicorder** -- either using the [live instrument](https://bicorder.ecologies.info/) or following the gradient tables in `SKILL.md`.
4. **Create your file** at `protocols/<your-slug>.json`.
5. **Validate locally**: `python scripts/validate.py protocols/<your-slug>.json`
6. **Open a pull request** with title `Add: <Protocol Name>`.

### Validation

The GitHub Actions CI runs automatically on every PR touching `protocols/`. It checks:

- JSON is valid and conforms to the schema
- The slug in `metadata.slug` matches the filename
- `pass_type` matches the number of gradients scored
- Required fields are present

Run it locally before submitting:

```bash
pip install jsonschema
python scripts/validate.py protocols/<your-slug>.json

# Or validate everything at once:
python scripts/validate.py --all
```

---

## Verification

When a PR is merged, a GitHub Action automatically stamps the `verified_by` field:

- If the submitter checked the **human review checkbox** in the PR template, their GitHub username is stamped in.
- If the box was left unchecked, the entry is stamped `verified_by: auto`.

`auto` entries are not second-class -- they are a valid part of the corpus, and human reviewers are encouraged to review them and open update PRs to upgrade the verification status.

---

## Repository structure

```
protocol-registry/
  protocols/               # one JSON file per protocol reading
    examples/              # reference examples (not community submissions)
      tcp-three-way-handshake.json
      corporate-budget-cycle.json
  schema/
    protocol-entry.schema.json   # canonical JSON schema for entries
  scripts/
    validate.py            # local and CI validation script
  .github/
    pull_request_template.md     # structured review checklist
    workflows/
      validate.yml         # schema check on every PR
      auto-verify.yml      # stamps verified_by on merge
  SKILL.md                 # load this into your LLM to contribute
  README.md
```

---

## The gradients

The bicorder covers 23 axes across three sets. A reading scores each axis from 1 (left pole) to 9 (right pole), with 5 representing a genuinely mixed or midpoint condition.

**Design** (how the protocol is created and remembered): explicit/implicit, institutional/organic, immutable/mutable, monocultural/multicultural, exclusive/inclusive, hierarchical/egalitarian, determined/open, macro/micro.

**Entanglement** (how the protocol relates to participant agents): obligatory/optional, symmetric/asymmetric, voluntary/coerced, agentic/passive, synchronous/asynchronous.

**Experience** (how the protocol is perceived in use): legible/illegible, immediate/delayed, alive/dead, smooth/rough, pleasant/unpleasant, natural/artificial, certain/uncertain, efficient/inefficient, exciting/boring, engaging/disengaging.

Analysis metrics computed from the scores: hardness/softness (mean), polarized/centrist (spread), formal/informal (Design-weighted heuristic; note this is a reconstruction -- the real instrument uses LDA on a private corpus), and a usefulness judgment from the analyst.

---

## Licensing

Protocol readings contributed to this registry are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). By submitting a PR you agree to this license.

The bicorder instrument was created by Nathan Schneider / CU Boulder Media Economies Design Lab as part of the Governance Ecologies project. This registry is an independent community use of the instrument, not an official product of that project.

---

## Related

- [Protocol Bicorder](https://bicorder.ecologies.info/) -- the original instrument
- [Protocol Institute](https://protocolize.it) -- the research community hosting this registry
- [Summer of Protocols](https://summerofprotocols.com/) -- the research program that incubated the bicorder
- [C3PO](https://c3po.protocolize.it) -- the Protocol Institute's oracle, which may eventually index this corpus

---

*This registry is a pilot. The schema, contribution process, and governance are all expected to evolve as the community grows. Open an issue to propose changes.*
