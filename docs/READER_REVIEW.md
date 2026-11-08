# Reader review

[Contributing](../CONTRIBUTING.md) · [Maintenance](../REPO_SETUP.md) · [Learning path](../practice/LEARNING_PATH.md)

Use this review when a change affects how someone starts, follows, or interprets a reading route. Agents can attempt a task from the published instructions and show where they hesitated or inferred more than the text supports. A human reader can also tell us how long a task took, how it felt, and whether it worked in ordinary life.

## Run a round

1. **Pick a task and a starting page.** Record the revision being tested. Good tasks are “find the five-minute paper route from the README and finish Week 1,” “carry the map record from Week 4 to Week 5,” or “explain Universal Mind and the Absolute using the glossary.” Give the reviewer the task and the starting page. Hold back the expected answer and the author's notes.
2. **Run independent reads.** Give each agent a fresh context and the same version of the files. One reviewer follows the paper route. Another prepares a real-case entry without claiming to have carried out a physical task. For changes to research claims, add a source reviewer who checks the relevant primary passages and evidence limits. Keep reviewers read-only until their reports are in. Use the prompt below or run the same exercise with a person.
3. **Check the reports and edit.** The editor reproduces concrete friction and checks source objections against the passage in question. Fix blocked paths, premature answers, contradictions, and unsupported inferences first. Separate taste from a problem the reader encountered. Keep any deliberate choice with a short reason.
4. **Re-run the affected task.** Start a fresh reader at the same page. Give them the revised text and the original task without the prior findings. Compare the two attempts and run the [link checks](../REPO_SETUP.md#check-reader-links-before-publishing). Save a brief result with the revision or pull request, including anything a simulated read could not verify.

## Prompt for a fresh reviewer

```text
Act as a reader encountering Project Gateway for the first time. Read only the
starting page and the pages you would open from it. Do not edit the files or
look at the editorial plan, prior reviews, or sample answers before attempting
the task.

Starting page: [path or URL]
Task: [one concrete reader task]

Attempt the task. Show your first click or next action and the answer or record
you produced. If you get stuck, quote the instruction or name the heading and
say what you tried. Note at most three points of friction you actually hit and
one smallest change per point. Separate preferences from things that blocked
you. Do not claim you performed an in-person activity or measured reading time.
Say what a human reader would still need to try.
```

For a source review, ask the reviewer to identify the strongest claim a paragraph makes, locate its primary source, and report which interpretation or inference the source supports. Ask them to keep a first-person experience, a change in behavior, an inference about concealed information, and a claim of direct influence separate. Link a disagreement to the exact passage so the editor can check it.

## Record the result

| Record | Include |
|---|---|
| Task and revision | Starting page, snapshot, and route attempted |
| What happened | Click path or output, with the point where the reader stalled or inferred too much |
| Decision | Fix, keep with reason, or ask a human reader |
| Recheck | What a fresh reader did with the revised version |

The review is complete when a reader can find the intended route, produce the expected kind of record unaided, and explain what the result can support. Agent feedback is an editorial check. It does not establish course effectiveness, safety, or how real readers will respond. When a human volunteers, ask them to try the same task before offering guidance, and keep their private practice notes out of the repository.

## First use · November 2026

A first reader of the Week 4 pilot had to scan past the practice instructions to find the paper task and saw the sample answer before attempting it. The revised course gives the paper route its own links and lets the reader judge the outcome first. A practice reader found that the lesson asked for details that the journal did not prompt for. The journal now carries the conditions for the check and the open question into the next week. A separate source reader caught a weak summary of Haanel's causal claim and paragraph numbers that belonged to a different edition.

A fresh reader then started from the README and completed the Week 1 and Week 4 paper prompts. They explained the two authors' claims and worked through how a missed check carries forward in the journal. The round checked whether the instructions were usable on paper. Human reading times and real-world practice are still open checks.
