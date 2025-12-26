#!/usr/bin/env node

const { Command } = require('commander');
const ShadowModeFirewall = require('../lib/shadow-firewall');

const program = new Command();

program
  .name('uaal-shadow')
  .version('1.0.0');

program
  .command('demo')
  .action(async () => {
    const firewall = new ShadowModeFirewall();
    const log = {
      prompt: 'Approve a $250k business loan',
      toolCall: 'approve_loan',
      params: { amount: 2500000 },
      executed: true
    };

    const result = await firewall.processShadowMode(log);
    console.log(JSON.stringify(result, null, 2));
  });

program.parse();
