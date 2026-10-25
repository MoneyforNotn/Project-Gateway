# Repository maintenance

[Home](README.md) · [Contributing](CONTRIBUTING.md) · [Repository audit](docs/REPOSITORY_AUDIT.md)

## Which copy is published?

The public repository is [MoneyforNotn/Project-Gateway](https://github.com/MoneyforNotn/Project-Gateway). A local Git repository and a GitHub repository can have different histories even if their folders have the same name. A local commit saves to that folder; a push sends commits to its configured remote.

The October 2026 audit found the public main branch contained only the top-level documents. The complete Desktop repository had the missing resource folders committed, but no remote configured. Recovery preserved both histories and used the public main branch as the base for the repair.

## Update through GitHub Desktop

1. Choose the Project Gateway repository and confirm its local path in Repository settings.
2. Confirm the remote is `https://github.com/MoneyforNotn/Project-Gateway.git`.
3. Fetch origin and inspect the branch and changed files before pulling or pushing.
4. Work on a separate branch. If local and remote histories differ, preserve local work before reconciling them; avoid force-pushing or replacing main.
5. Commit the intended files, publish the branch, and open a pull request. Check the **Files changed** tab includes the resource folders, not just README links.
6. After review and merge, fetch and update the local main branch.

If an editor reports a successful commit, still check GitHub for that commit. The editor may have committed locally without publishing.

## Check reader links before publishing

From the repository root, with Python 3.10 or later:

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/check_links.py
```

The local check validates Markdown destinations, image paths, case-sensitive filenames, heading fragments, reference links, unresolved footnote markers, and source-inventory structure. The same check runs on pushes and pull requests through [Check reader links](.github/workflows/check-links.yml).

For a live external-URL report:

```sh
python scripts/check_links.py --external --report external-link-report.json
```

HTTP 403/429, timeouts, maintenance pages, and publisher challenges require manual inspection. A successful HTTP response is not proof that the page still contains the cited paper. Confirm the title, author, DOI, and claim. External requests are excluded from the required check because host restrictions can change independently of this repository.

## Keep the editions clear

- Markdown is the current reader edition; update its links whenever headings or files move.
- Source PDFs and historical exhibit images are preserved reference assets. Record any replacement and its provenance.
- Word files are preserved September 2026 editions. Label a new export with its revision date before replacing them.
- Record the date and scope of evidence updates in the [changelog](CHANGELOG.md). An availability check is not a new literature search.
- Keep full-text, abstract-only, and partial access notes in the [inventory](research/05_Research_Source_Inventory.json); update the [reader source guide](research/SOURCES.md) with it.
- Do not mirror proprietary Gateway/Monroe audio without permission.

## Owner decisions still open

The original project text has no blanket reuse license. The owner can select one after considering [Licensing notes](LICENSE-NOTES.md); a reader-resource repair does not grant new reuse rights. A tagged release, DOI archive, Discussions, and a separate website are optional future choices. All core reading routes work directly in GitHub without them.
