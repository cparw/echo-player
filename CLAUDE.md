# Notes for Claude

This repo also holds the owner's GTA 6 reels studio in `reels-studio/`.
For any reels, GTA 6, content, voice or social media task, read `reels-studio/RULEBOOK.md` FIRST (the owner's rules and every piece of feedback so far, so he never has to repeat himself), then `reels-studio/STUDIO.md` (engine, accounts, footage sources, commands).
When the owner gives new feedback, add it to the RULEBOOK Feedback log and update the matching rule the same day.

## Model use (owner's standing rule, 13 Nov 2026)

The owner often runs the main session on Fable. Mix it with Opus so usage is spent well: never use Fable where Opus can do the same job to the same quality.
* Send research, web searches, name and fact vetting, file and footage audits, renders, QA sheets, bookkeeping and any long multi step legwork to subagents on Opus (Agent tool, `model: "opus"`), in parallel where possible.
* Keep on the main model only what needs it: creative direction, hooks and scripts, final judgment calls, and checking what the subagents return.
* A small job (a few tool calls) is done directly; a subagent would cost more than it saves.
* In the reply, say in one line which part ran on which model.
