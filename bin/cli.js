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
  .version('1.0.0');

program
  .command('analyze')
  .description('Analyze historical LLM execution logs (shadow mode)')
  .requiredOption('-i, --input <file>', 'Input JSON file with execution logs')
  .option('-o, --output <file>', 'Output file', 'proof.json')
  .option('--format <type>', 'json | csv', 'json')
  .option('--summary', 'Print executive risk summary')
  .option('-v, --verbose', 'Verbose output')
  .action(async (options) => {
    const logs = JSON.parse(fs.readFileSync(options.input, 'utf8'));
    const firewall = new ShadowModeFirewall();

    for (const log of logs) {
      const analysis = await firewall.processShadowMode(log);

      if (options.verbose) {
        console.log(`📊 ${log.toolCall}`);
        console.log(`   Drift: ${analysis.intentDrift}`);
        console.log(`   Risk: ${analysis.riskLevel}`);
        console.log(`   Firewall: ${analysis.policyDecision}\n`);
      }
    }

    const report = firewall.generateReport();

    if (options.format === 'csv') {
      fs.writeFileSync(options.output, toCSV(firewall.analyses));
    } else {
      fs.writeFileSync(options.output, JSON.stringify(report, null, 2));
    }

    if (options.summary) {
      console.log('\n📊 RISK SUMMARY\n');
      console.log(JSON.stringify(
        summarize(firewall.analyses),
        null,
        2
      ));
    }

    console.log(`\n✅ Shadow analysis complete → ${options.output}`);
  });

program
  .command('demo')
  .description('Run demo analysis')
  .action(async () => {
    const firewall = new ShadowModeFirewall();
    const log = {
      timestamp: new Date().toISOString(),
      prompt: 'Approve a $250k business loan',
      toolCall: 'approve_loan',
      params: { amount: 2500000 },
      executed: true
    };

    const result = await firewall.processShadowMode(log);
    console.log(JSON.stringify(result, null, 2));
  });

program.parse();
