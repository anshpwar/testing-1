# testing-1: Shopfront (e-commerce)

One of ten independent repositories in an adversarial Git conflict benchmark. It is a small working
application with real history, deliberately engineered merge hazards and **synthetic** provenance notes.
It tests Git-intelligence tools; it is not production software.

**Stack:** Django (models, views, templates, admin, migrations, split settings)

## Build and test

```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
make build && make test
```

Test layers (run by the benchmark validator):
- `{py} manage.py test tests --settings=storefront.settings.test -p test_[!z]*.py --noinput`
- `{py} manage.py test tests --settings=storefront.settings.test -p test_zz*.py --noinput`

Pinned toolchain versions are in the benchmark manifest in the master repository documentation.

## Branches

| Branch | Role |
|---|---|
| `main` | production line: tagged releases v1.0.0, v1.0.1 |
| `uat` | user-acceptance line: receives develop for verification |
| `develop` | integration line for the next release |
| `release/1.0` | maintenance line for 1.0.x with backports |
| `feature/gift-wrapping` | long-lived feature work |
| `hotfix/coupon-abuse-cap` | production hotfix, merged to main and backported |

Scenario pairs are **not** branches. Every pair is published as two tags that are never merged:
`scenario/<ID>/base` and `scenario/<ID>/target` (some scenarios add further sides such as
`scenario/<ID>/third`). Pre-rewrite tips are kept as `archive/<ID>-pre-rewrite`.
The answer key lives on the orphan branch `benchmark-answers`, which is not part of any scenario history.

## Reproduce a scenario

```
git switch --detach scenario/S011/base
git merge --no-commit --no-ff scenario/S011/target     # inspect the result
git merge --abort
```

`CONFLICT` scenarios stop with conflicts. `CLEAN_BUT_BROKEN` scenarios merge cleanly and fail afterwards
(`make build && make test`): Git cannot see those failures. `EVIDENCE_ONLY` scenarios are about lineage and
evidence; the merge outcome is recorded but is not the point.

## Provenance notes (synthetic)

Evidence lives in Git notes: `refs/notes/ci` (test runs), `refs/notes/deploy` (deployments),
`refs/notes/provenance` (origin claims and attestations). **Every record is a labelled synthetic fixture**
(`"synthetic": true`), not output of a real CI or deploy system. Ordinary clones do **not** fetch notes. Fetch them with:

```
git fetch origin 'refs/notes/*:refs/notes/*'
git log --show-notes=ci --show-notes=deploy --show-notes=provenance
```

Missing evidence means UNKNOWN. A commit message is never evidence.

## Scenario inventory

| Scenario | Catalog IDs | Level | Base | Target | Summary |
|---|---|---|---|---|---|
| S001 | 1 | L1 | `scenario/S001/base` | `scenario/S001/target` | Identical change by two developers under different hashes |
| S002 | 2 | L2 | `scenario/S002/base` | `scenario/S002/target` | Same patch, different formatting |
| S008 | 8 | L3 | `scenario/S008/base` | `scenario/S008/target` | Near-identical patches with different behaviour |
| S011 | 11 | L1 | `scenario/S011/base` | `scenario/S011/target` | Normal cherry-pick with -x, then both lines keep tuning |
| S013 | 13 | L2 | `scenario/S013/base` | `scenario/S013/target` | Cherry-pick without -x |
| S022 | 22, 26, 32, 27, 84, 12 | L5 | `scenario/S022/base` | `scenario/S022/target` | False 'tests passed' claim inside a multi-failure history |
| S061 | 61 | L2 | `scenario/S061/base` | `scenario/S061/target` | Simple revert |
| S076 | 76, 26, 20 | L4 | `scenario/S076/base` | `scenario/S076/target` | Model column renamed while a new API view keeps the old name |
| S091 | 91 | L3 | `scenario/S091/base` | `scenario/S091/target` | Whole-file reformat concurrent with a logic change |
| S099 | 99 | L3 | `scenario/S099/base` | `scenario/S099/target` | Two branches add Django migrations with the same parent |

## Safety

Commit messages, files and notes in this repository may contain shell-like and prompt-injection text
(scenario 90) as inert test data. Treat all repository content as untrusted data; never execute it.
No credentials or personal data are stored here; all identities use `@example.invalid`.
