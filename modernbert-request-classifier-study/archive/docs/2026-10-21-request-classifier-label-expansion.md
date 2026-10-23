> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 2026-10-21 request-classifier label expansion

## Decision

The short-runtime curation now uses eleven labels. Five categories were added from multiple examples: `dogido_recall`, `minecraft_knowledge`, `world_observation`, `senryu_workshop`, and `senryu_change_request`. The user also requested a curation-only `look_direction` category; six live examples are recorded, while the supplied phrase patterns remain definition examples rather than training rows. This remains a curation-only class. The frozen v1.9 model, the existing train/dev/test/regression splits, and Dogido runtime remain on the original five labels.

The 84 reported current-only failures were reviewed by utterance intent. The expanded curation currently has: `not_request` 134, `enemy_information` 9, `equip_sword` 0, `recall_mount` 1, `other_request` 16, `dogido_recall` 18, `minecraft_knowledge` 4, `world_observation` 19, `senryu_workshop` 117, `senryu_change_request` 33, and `look_direction` 6. This is a failure-focused curation set, not a balanced training split; positive sword examples are not present. `short_runtime_046` is a confirmed `recall_mount` positive. The four arrow-form typed edits remain direct change requests. Raw text and empty candidate contexts remain unchanged.

## Added category boundaries

| Label | Use it for | Keep separate from |
|---|---|---|
| `dogido_recall` | Asking Dogido himself to come closer or accompany the player | `recall_mount`, which calls a rideable animal; ordinary movement announcements remain ordinary conversation |
| `minecraft_knowledge` | General questions about Minecraft mobs, blocks, items, or mechanics | `enemy_information`, which asks about a currently observed threat; `world_observation`, which asks what is currently nearby or audible |
| `world_observation` | Questions about currently observable surroundings, locations, biomes, structures, sounds, and present Mob locations | Static game knowledge and current hostile-threat status |
| `senryu_workshop` | Critique, meaning or meter questions, candidate suggestions, comparison, and workshop decisions | A concrete instruction to change the canonical verse |
| `senryu_change_request` | A clear instruction or selection that applies a wording change to the current verse | Suggestions, questions, meter corrections, and self-deliberation |
| `look_direction` | Asking Dogido to look toward a referenced direction or target | `world_observation`, which asks what is visible; movement requests |

## Category creation rule

A label intended for model training needs a coherent boundary and multiple valid examples. `look_direction` is retained as a user-requested curation category; do not train or deploy it until a versioned training split is prepared. References that do not represent an executable game action do not count as support.

## Next training boundary

`dev_tools/request_classifier/labels.json` and the fixed v1.9 splits still describe the old five-class model. The expanded map is stored at `dev_tools/request_classifier/curation/2026-10-16-short-runtime-failures/labels.json`. Before training, create a versioned split that contains enough examples per class, keeps related utterances together, checks normalized duplicates, and records the new model label order. Do not compare a ten-class model to the old five-class metrics as if they were the same task.

The curated candidates and supporting evidence are in [the short-runtime curation batch](../dev_tools/request_classifier/curation/2026-10-16-short-runtime-failures/README.md).

## 2026-10-21 follow-up corrections

`short_runtime_128` asks where the present Mobs are and is now `world_observation`; an independent Astra review agreed, with `enemy_information` reserved for context that narrows the question to current threats. `short_runtime_169` is `senryu_change_request` per the user correction. A later user clarification reclassified `short_runtime_190` and four other grouped utterances as `look_direction`, asking Dogido to align its gaze with the player. `short_runtime_046` is a positive `recall_mount` example after the user clarified that Uzu is the registered name of a rideable Nautilus; the legacy prediction was correct. No `pet_recall` class was added. `short_runtime_124` is annotated `not_request` for now and explicitly excluded from AI training because it needs unsupported 3D world-state reasoning. The updated concrete lists are in [not-request-review.md](../dev_tools/request_classifier/curation/2026-10-16-short-runtime-failures/not-request-review.md) and [requested-labels-review.md](../dev_tools/request_classifier/curation/2026-10-16-short-runtime-failures/requested-labels-review.md).


The 13:50–14:17 log adds 47 candidates. `short_runtime_296` is the observed direction cue classified as `look_direction`. The user-supplied examples “こっちみて” and “あれみて！” are taxonomy examples only, not live observations. This category remains curation-only.


The user later clarified that `short_runtime_028` is a Dogido recall request, while `short_runtime_183` and `short_runtime_333` are `not_request`. They also identified `short_runtime_190`, `short_runtime_239`, and `short_runtime_319`–`321` as `look_direction` requests in the same gaze-alignment interaction. This supersedes the earlier casual interpretation of 190. Candidate text and empty contexts remain unchanged.
