## Protocol Registry Submission

**Protocol name:** <!-- e.g. "HOA Annual Meeting" -->

**Slug:** <!-- e.g. "hoa-annual-meeting" — should match the filename -->

**Standpoint:** <!-- Who is the analyst, from what vantage point? -->

---

### Submission checklist

- [ ] The JSON file is at `protocols/<slug>.json`
- [ ] The slug matches the filename (e.g. `protocols/hoa-annual-meeting.json` → slug `hoa-annual-meeting`)
- [ ] `metadata.name`, `metadata.description`, `metadata.standpoint`, `metadata.lifecycle`, and `metadata.scale` are all filled in
- [ ] All 23 gradients are scored (or `pass_type: "shortform"` with the shortform subset scored)
- [ ] `analysis.hardness` and `analysis.polarized` are computed and present
- [ ] `provenance.submitted_by` is set (GitHub username or `"anonymous"`)
- [ ] `provenance.submission_method` is set
- [ ] The file validates against the schema: `python scripts/validate.py protocols/<slug>.json`

---

### Human review

**If you are a human reviewer who has personally read this bicorder reading and can vouch for its quality:**

- [ ] ✅ I am a human reviewer. I have read the full bicorder reading, the gradient scores are plausible for this protocol from this standpoint, and I approve this entry for the verified registry.

**Leave the box above unchecked if this is an LLM-assisted submission being offered for community review.** An unchecked box is not a rejection -- it simply means the entry will be stamped `verified_by: auto` on merge, marking it as pending human review. That is a valid and welcome contribution to the corpus.

---

### Notes for reviewers

When reviewing a bicorder submission, consider:

- Is the standpoint clearly stated and consistently applied across gradients?
- Do the gradient scores make sense given the standpoint (a protocol looks different from a designer vs. a participant vs. an outsider)?
- Are there gradients scored at extremes (1 or 9) without explanation? Check the `notes` field.
- Is the `lifecycle` field a reasonable fit?
- Does the `summary_bar` in `analysis` roughly match the gradient values?

You do not need to re-run the full interview to approve. A careful read of the JSON and plausibility check is sufficient for human verification.

---

<!-- 
🤖 Generated with Claude Code

Submissions to this registry represent community knowledge about protocols.
By submitting, you agree to license your contribution under CC BY 4.0.
-->
