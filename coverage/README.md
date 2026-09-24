# Coverage

A private, local-first model of whether liquid assets plus reliable income cover what is owed, month by month over a horizon of up to 30 years. It is a forward-looking coverage model, not a budget or a transaction tracker. There is no backend, no network access and no analytics; data stays in the browser's IndexedDB.

This folder is self-contained and separate from the Letsema website at the repo root. It is not deployed.

## Status

Phases 1 and 2 of 5 are complete: the projection engine with its tests, and the storage layer with editors for every entity and the global assumptions. The dashboard, charts, scenarios and check-in screens are placeholders until Phases 3 to 5.

```sh
npm install
npm run dev         # http://localhost:5173
npm run build       # production build into dist/, with the Content Security Policy
npm run preview     # serve the production build at http://localhost:4173
npm test            # unit and UI tests
npm run demo        # sample household projection in the terminal (optionally: npm run demo -- 2027-03)
npm run check       # typecheck + lint + tests
```

Data lives in IndexedDB for the origin you open the app on, so `localhost:5173` and `localhost:4173` hold separate data. Pick one for real use.

## Layout

```
src/engine/   pure projection engine, metrics, scenarios, diagnostics (no framework, clock or I/O)
src/schema/   Zod schemas for entities, settings and the whole dataset; engine input mapping
src/db/       Dexie database and repository (validated writes, reference clean-up, reordering)
src/sample/   fictional sample household
src/ui/       React screens, generic entity editor, field parsing and formatting
```

Every write goes through a Zod schema. The editors share one form model (`src/ui/editors/fields.ts`): each field has a kind that controls how it is parsed and formatted, fields can be hidden depending on other fields, and schema errors are mapped back to the field they concern. Amounts accept either decimal convention (`12 000,50` or `12,000.50`).

The production build carries a Content Security Policy with `connect-src 'none'`, so the browser blocks any network request from the app. The app asks the browser for persistent storage so IndexedDB is not evicted under storage pressure.

## Conventions

Money is integer cents. Rates are integer basis points (11.75% is `1175`). Months are `'YYYY-MM'` strings, converted inside the engine to a month index so date arithmetic is integer addition. Income is entered net of tax.

Amounts on obligations and income are as at the as-of month. Escalation and growth step up once a year in their configured calendar month, counting from the as-of month, including for items that start in the future. Annual obligations are paid as a lump in their payment month.

Loan interest uses the nominal annual rate divided by 12. Asset growth uses the monthly-equivalent effective rate, `(1 + r)^(1/12) − 1`. Each amount is rounded to the cent once, at the step that produces it.

## Engine

`src/engine` is pure TypeScript. ESLint forbids it from importing React, Dexie, Recharts, Zod or anything outside the folder, and from touching the clock, randomness, storage or the network.

`project(inputs)` runs month by month from the as-of month:

1. Add income due.
2. Pay recurring obligations, with escalation in the configured month.
3. Accrue interest on debts and pay instalments. In the end month any remaining balance is paid as a balloon. Interest on a carried deficit accrues here if an overdraft rate is set (default 0).
4. Apply one-off events.
5. Grow assets.
6. From a surplus, first repay any carried deficit, then sweep the rest into the sweep asset (falling back to the first T1 asset, then to a notional unallocated cash bucket).
7. Fund a shortfall from T1 in list order, then T2 net of haircut, then the accessible T3 amount if enabled. Anything unfunded is carried forward as a deficit and the month is flagged.

Net worth is all assets at full value less debt and deficit. Liquid assets are T1, plus T2 after haircut, plus the accessible T3 amount after haircut. Liquid net worth is liquid assets less debt and deficit. Real values are a display conversion only (`toReal`).

`evaluate(inputs, overrides)` returns the projection and headline metrics: the 12-month coverage ratio, the base-case first shortfall, the two runways (variable income stops; all income stops, with one-off events still applied) and net worth today and at the horizon. The coverage ratio is `(T1 + T2 after haircut + committed income) / (obligations + debt payments + one-off outflows)` over the next 12 months.

Scenarios are overrides applied to a copy of the inputs. When combined, deltas add, factors multiply, exclusions are pooled and extra events are appended. The presets are a rate shock (prime +200 bps, with variable-rate instalments recalculated as the user's instalment plus the change in level instalment over the remaining term), variable income down 40% and cost escalation (+3 percentage points).

## Tests

`src/engine/__tests__` covers amortisation against a textbook schedule and the closed-form balance, escalation timing, drawdown order and haircuts, the coverage ratio, both runways, scenario overrides and edge cases (debts retired mid-horizon, balloons, income ending, empty tiers, carried deficits). A conservation test checks every month of the sample household under each scenario, and of 300 generated households, for cash and debt to reconcile to the cent.
