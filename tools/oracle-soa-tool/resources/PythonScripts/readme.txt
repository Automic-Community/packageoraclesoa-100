1. These .py files are used in WebLogic actions. They should be attached in PCK.AUTOMIC_ORACLE_SOA.PRV.STORE.

2. When you make changes in any file in /includes folder, pls run CodeMerger to merge the changes into related files.
	Requirement: 
		- Pls install Jython. 
		- Make sure the files are not read-only (i.e. check out them in P4 beforehand)
	Usage: 
		jython CodeMerger.py

3. You can make changes and commit this file to Perforce to trigger updating the storage object PCK.AUTOMIC_ORACLE_SOA.PRV.STORE.		
