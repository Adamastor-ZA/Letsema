'use strict';
// Smoke test for helpers.js: styles, lists, table, box, figure placeholder, header and footer.
const path = require('path');
const H = require('./helpers');

async function main() {
  const ctx = H.makeContext();
  H.setChapter(ctx, '2');
  const children = [
    new H.Paragraph({ style: 'CoverTitle', children: [new H.TextRun('Unlocking Tourism Growth')] }),
    new H.Paragraph({ style: 'CoverSub', children: [new H.TextRun('A Strategy for the Western Cape to 2035')] }),
    new H.Paragraph({ style: 'CoverMeta', children: [new H.TextRun('Final Research Report. Draft for discussion, 2 November 2026')] }),
    H.h1('Analysis summaries', 'ch2'),
    H.h2('2.1 Demand-side analysis and market strategy'),
    H.lead('Growth is capped by market concentration and seasonality before it is capped by demand.'),
    H.body('Five markets hold **63%** of overseas arrivals and 65% of visitors travel between October and March ' + H.cite('Demand-Side Analysis', 'Jun 2026', 'p9') + '. A placeholder looks like this: [2028 target to be confirmed].'),
    H.kicker('2.1 Accessibility, connectivity and infrastructure'),
    H.h3('Win direct routes and add seats on full routes'),
    ...H.numbered(['First numbered item renders with a number.', 'Second item continues the sequence.']),
    ...H.numbered(['A new list restarts at one.', 'And continues.'], 'n_90'),
    ...H.bullets(['A bullet.', 'Another bullet.']),
    ...H.table(ctx, {
      caption: 'Three scenarios reach between 1.82m and 2.52m arrivals by 2035.',
      source: 'Market Assessment Report, May 2026, p21.',
      columns: [{ header: 'Scenario', width: 2 }, { header: '2025 base', width: 1, align: H.AlignmentType.RIGHT }, { header: '2035', width: 1, align: H.AlignmentType.RIGHT }, { header: 'CAGR', width: 1, align: H.AlignmentType.RIGHT }],
      rows: [['Conservative', '1,498,829', '1,822,634', '2.0%'], ['Base', '1,498,829', '2,175,778', '3.8%'], ['Accelerated', '1,498,829', '2,516,282', '5.3%']],
      boldFirstCol: true,
    }),
    ...H.box('What this means for the tree', ['Supports focus areas 4, 5 and 7. Refines focus area 2.']),
    ...H.figure(ctx, { file: path.join(__dirname, 'assets', 'does_not_exist.png'), caption: 'The base case reaches the seat ceiling in 2030.', source: 'Market Assessment Report, May 2026, p22.' }),
    H.h4('Recommendation'),
    H.body('What Wesgro does. What Wesgro asks partners to do. What sits outside the province and is escalated.'),
  ];
  const doc = H.buildDocument({ sections: [{ children, firstPageBlank: true }], shortTitle: 'Unlocking Tourism Growth: A Strategy for the Western Cape to 2035', title: 'Smoke test' });
  const out = await H.save(doc, path.join(__dirname, '..', 'outputs', 'smoke_test.docx'));
  console.log('wrote', out);
}
main().catch((e) => { console.error(e); process.exit(1); });
