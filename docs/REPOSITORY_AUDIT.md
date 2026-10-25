# Reader resource audit · 25 October 2026

[Home](../README.md) · [Maintenance](../REPO_SETUP.md) · [Changelog](../CHANGELOG.md)

## Why the links failed

The public main branch at commit `5a1ebf350c69b668ea1d063184172e237b0ab220` contained ten top-level files. Its README and Start Here pages linked to research, practice, transcript, and source directories absent from that tree. There were **35 broken local link occurrences**: 22 in README and 13 in Start Here.

The complete Desktop repository had those resource folders committed at `307d97a` but had no remote configured. Local commits and the public repository had separate histories. The recovery used the public main branch as its base and preserved the local material rather than replacing either history.

## Restored and improved

| Area | Reader result |
|---|---|
| Source archive | Both preserved facsimiles, the editable transcript, and all five historical exhibits are available |
| Research | Full evidence review, overview, methodology, provenance, glossary, roadmap, and structured source inventory are available |
| Citation | Conversion markers are replaced with linked source IDs; a readable source guide preserves study designs and access limitations |
| Learning | Six weeks with separate baseline preparation, a reading-only route, optional short exercises, and a matching journal |
| Navigation | The README's routes open actual material; longer references have contents or page navigation and return links |
| Presentation | A restrained archival cover, concise reading routes, and consistent Markdown formatting |
| Maintenance | A local link/image/fragment checker and GitHub workflow catch missing destinations before publication |

The glossary retains its original 25 terms and expands to 47 linked entries. Word files are preserved September 2026 snapshots; the current reader edition is Markdown. The two PDFs and five exhibit images were recovered without altering their file contents.

## Evidence and availability

The literature review was prepared on **8 September 2026**. The October revision improves publication and reader resources; it is not a new comprehensive literature search. Source records retain whether the original review consulted full text, an abstract, an official summary, or partial material.

Spot-checks confirmed the cited study counts and findings for the 2023 EEG entrainment review, the two small Hemi-Sync clinical trials, the 2026 theta-beat review, the remote-viewing meta-analysis, and the 2026 preregistration comparison. These checks do not establish that every study's methods or underlying data were independently audited. See the [source guide](../research/SOURCES.md) for source-specific limits.

The CIA direct-PDF endpoint redirected to maintenance during inspection. The supplementary DocumentCloud S3 endpoint returned HTTP 403 to the audit tool. The original UCI report links also failed access checks; the Utts, Hyman, and response sections now link to a verified university archival copy of the AIR report. NASA provides a preprint alternate for the Schumann-resonance paper. Both local facsimiles remain available; the [GovInfo catalog](https://www.govinfo.gov/app/details/GOVPUB-D101-PURL-gpo152943) provides the government record. A publisher block or timeout is recorded as an access limitation, not treated as a vanished paper.

## What still needs a decision or research

- **Reuse license:** the owner has not selected a blanket license for the original project text. This update preserves that status. See [Licensing notes](../LICENSE-NOTES.md).
- **Evidence updates:** direct Gateway trials, Focus-state characterization, independent replication, and the origin of the page-25 omission remain open research questions. They are described in the [roadmap](../research/RESEARCH_ROADMAP.md), not presented as missing reader assets.
- **Optional distribution:** a tagged release, DOI archive, new Word/PDF exports, or a separate interactive site can follow if useful. The core resources are readable and linkable on GitHub now.

## Repeat verification

At this revision, all **721 local link, image, and fragment occurrences across 21 Markdown files** pass. Four regression checks cover valid routes, missing or mis-cased destinations, linked images, heading anchors, unfinished citations, and invalid source records. Preserved PDF, exhibit, and Word file hashes match the Desktop originals; the facsimiles contain 29 and 30 leaves respectively.

Run the commands in [Repository maintenance](../REPO_SETUP.md#check-reader-links-before-publishing). Local links, filename case, images, heading fragments, reference definitions, unresolved citation markers, and source records are checked automatically. External availability needs periodic manual checks because redirects and successful HTTP responses can conceal maintenance or challenge pages.
