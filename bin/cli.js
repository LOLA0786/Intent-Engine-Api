#!/usr/bin/env node

const { Command } = require('commander');
const fs = require('fs');

const ShadowModeFirewall = require('../lib/shadow-firewall');
const { toCSV } = require('../lib/csv-export');
const { summarize } = require('../lib/risk-summary');

const program = new Command();

program
  .name('uaal-shadow')
  .description('LLM Intent Firewall - Shadow Mode')
  .version('1.1.0-shadow');

program
  .command('analyze')
  .description('Analyze historical LLM execution logs')
  .requiredOption('-i, --input <file>', 'Input JSON logs file')
  .option('-o, --output <file>', 'Output report file', 'proof.json')
  .option('--summary', 'Show executive risk summary')
  .option('--format <type>', 'json or csv', 'json')
  .option('-v, --verbose', 'Verbose output')
  .action(async (options) => {
    // ---- LOAD LOGS ----
    const logs = JSON.parse(fs.readFileSync(options.input, 'utf8'));
    const firewall = new ShadowModeFirewall();

    // ---- RUN SHADOW MODE ----
    for (const log of logs) {
      const analysis = await firewall.processShadowMode(log);

      if (options.verbose) {
        console.log(`📊 ${log.toolCall}`);
        console.log(`   Drift: ${analysis.intentDrift}`);
        console.log(`   Risk: ${analysis.riskLevel}`);
        console.log(`   Firewall: ${analysis.policyDecision}\n`);
      }
    }

    // ---- EXECUTIVE SUMMARY ----
    if (options.summary) {
      const summary = summarize(firewall.analyses);
      console.log('\n📊 RISK SUMMARY\n');
      console.log(JSON.stringify(summary, null, 2));
    }

    // ---- OUTPUT ----
    if (options.format === 'csv') {
      const csv = toCSV(firewall.analyses);
      fs.writeFileSync(options.output.replace('.json', '.csv'), csv);
      console.log(`\n✅ Shadow analysis complete → ${options.output.replace('.json', '.csv')}`);
    } else {
      fs.writeFileSync(
        options.output,
        JSON.stringify(firewall.generateReport(), null, 2)
      );
      console.log(`\n✅ Shadow analysis complete → ${options.output}`);
    }
  });

program.parse(process.argv);
