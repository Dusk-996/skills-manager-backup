---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.

## Optional domain documentation

When the user requests a glossary, architecture decision records, or documentation alongside the interview, use the installed `domain-modeling` skill while running this session. Read existing domain documents relevant to the topic and record terminology and decisions as they are resolved. Ask the same single decision question at a time; documenting a resolved decision does not authorize implementing it.

This mode incorporates the former `grill-with-docs` shortcut. The former `grill-me` shortcut is the ordinary interview above. Both are now available through this one `grilling` entry point.
