#!/usr/bin/env node

const { Command } = require('commander');
const fs = require('fs');

const ShadowModeFirewall = require('../lib/shadow-firewall');
const { toCSV } = require('../lib/csv-export');
const { summarize } = require('../lib/risk-summary');

const program = new Command();

program
  .name('uaal-shadow')
  .description('UAAL – LLM Intent Firewall')
  .version('1.2.0-shadow');

/**
 * ANALYZE (shadow / enforce)
 */
program
  .command('analyze')
  .description('Analyze historical LLM execution logs (shadow or enforce)')
  .requiredOption('-i, --input <file>', 'Input JSON logs file')
  .option('-o, --output <file>', 'Output file', 'proof.json')
  .option('--summary', 'Show executive risk summary')
  .option('--format <type>', 'json or csv', 'json')
  .option('-v, --verbose', 'Verbose output')
  .action(async (options) => {
    const logs = JSON.parse(fs.readFileSync(options.input, 'utf8'));

    const firewall = new ShadowModeFirewall();

    // ---- PROCESS LOGS ----
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
      const csvFile = options.output.replace('.json', '.csv');
      fs.writeFileSync(csvFile, csv);
      console.log(`\n✅ Shadow analysis complete → ${csvFile}`);
    } else {
      fs.writeFileSync(
        options.output,
        JSON.stringify(firewall.generateReport(), null, 2)
      );
      console.log(`\n✅ Shadow analysis complete → ${options.output}`);
    }
  });

/**
 * ENFORCE MODE SWITCH
 */
program
  .command('enforce')
  .description('Run UAAL in real-time enforcement mode')
  .action(() => {
    process.env.UAAL_MODE = 'enforce';
    console.log('🚨 UAAL running in ENFORCE mode');
    console.log('• Policy violations will be BLOCKED');
    console.log('• Decisions will emit to Kafka / webhook (if configured)');
  });

program.parse(process.argv);
