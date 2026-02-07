
- TUTTI I MODULI CHE HANNO LANG: 
    - Devi modificare a tutti i moduli get_system_lang
    - devo modificare il modo in cui vengono gestite le traduzioni retranslateUi non può trovarsi nella *_ui.py
    - La lingua deve essere quella dello user al monento del bootstrap
    - Devo cambiare le stringe di acquisition_type (web ,instagram, email, ... ) con: from fit_common.core import AcquisitionType

- devo aggiungere un disclaimer che dice di chiudere tutte le altre finestre che fanno traffico


- BUG: devo verificare perchè acquisition.log è vuoto
- Devo scrivere nei log le informazioni prese in fase di boostrap nelle variabili d'ambiente
- BUG: devo assolutamente modificare approccio per la scrittura dei file di acquisizione acquisition.log, traceroute.txt, ....
- BUG: Devo verificare perchè mitproxy non funziona corettamente con github

Errore de merda
[DEBUG] 2026-02-04T11:02:40 - privilege: sudo failed, exit code: -11
[DEBUG] 2026-02-04T11:02:40 - ❌ Elevation failed
[DEBUG] 2026-02-04T11:02:40 - main.fit_web: ❌ Admin permissions denied
[DEBUG] 2026-02-04T11:02:53 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 17749
[DEBUG] 2026-02-04T11:02:53 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True




