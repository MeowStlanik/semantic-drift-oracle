# Release evidence


- Repository: `https://github.com/MeowStlanik/semantic-drift-oracle`
- Immutable source: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/7436227dea6b0bc49e4eefb6b87f2ca441cc2e5c/contracts/semantic_drift_oracle.py`
- Tests: `https://github.com/MeowStlanik/semantic-drift-oracle/tree/7436227dea6b0bc49e4eefb6b87f2ca441cc2e5c/tests`
- Consensus design: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/7436227dea6b0bc49e4eefb6b87f2ca441cc2e5c/docs/CONSENSUS.md`
- Security analysis: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/7436227dea6b0bc49e4eefb6b87f2ca441cc2e5c/docs/SECURITY.md`
- Contract address: `0xF7F2269078bd2aAa726CAF78050EF4C980F5Cabb`
- Deployment transaction: `0x5c91a220a6a01b418c8c24eb3950150c9f39e7e0e74b9e3eb06550c8d69a358b`
- Explorer transaction: `https://explorer-bradbury.genlayer.com/tx/0x5c91a220a6a01b418c8c24eb3950150c9f39e7e0e74b9e3eb06550c8d69a358b`
- Explorer contract: `https://explorer-bradbury.genlayer.com/address/0xF7F2269078bd2aAa726CAF78050EF4C980F5Cabb`
- Source SHA-256: `61e8524cd813535800fc195d63b537e5ca693da0b20323c60d1a2b1807f1fd54`

Local verification required by the release script:

1. Python syntax compilation.
2. GenVM lint and SDK validation.
3. Full direct-mode test suite, including validator agreement/disagreement and
   pickling checks.
4. The same lint and test suite a second time in a fresh process.
5. Bradbury deployment compilation/consensus.
6. Post-deployment schema fetch and `get_stats()` view call.
