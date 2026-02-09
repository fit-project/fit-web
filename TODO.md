
- TUTTI I MODULI CHE HANNO LANG: 
    - Devi modificare a tutti i moduli get_system_lang
    - devo modificare il modo in cui vengono gestite le traduzioni retranslateUi non può trovarsi nella *_ui.py
    - Devo scrivere nei log le informazioni prese in fase di boostrap nelle variabili d'ambiente

- TUTTI I MODULI SCRAPER
     - Devo cambiare le stringe di acquisition_type (web ,instagram, email, ... ) con: from fit_common.core import AcquisitionType
      - Devo cambiare le stringe di logger = logging.getLogger("scrapers.web") con: from fit_acquisition.logger_names import LoggerName logger = logging.getLogger(LoggerName.SCRAPER_WEB.value)

- BUG: Devo verificare perchè mitproxy non funziona corettamente con github

Errore de merda
[DEBUG] 2026-02-04T11:02:40 - privilege: sudo failed, exit code: -11
[DEBUG] 2026-02-04T11:02:40 - ❌ Elevation failed
[DEBUG] 2026-02-04T11:02:40 - main.fit_web: ❌ Admin permissions denied
[DEBUG] 2026-02-04T11:02:53 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 17749
[DEBUG] 2026-02-04T11:02:53 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True


[DEBUG] 2026-02-08T10:56:28.582720+01:00 - ZipAndRemoveFolderWorker.start: ℹ️ removing downloads_folder=/Users/zitelog/Documents/FIT/pippo/web/acquisition_2/downloads
[DEBUG] 2026-02-08T10:56:28.582863+01:00 - ZipAndRemoveFolderWorker.start: ✅ removed downloads_folder
[DEBUG] 2026-02-08T10:56:28.582898+01:00 - ZipAndRemoveFolderWorker.start: ℹ️ removing screenshot_folder=/Users/zitelog/Documents/FIT/pippo/web/acquisition_2/screenshot
[DEBUG] 2026-02-08T10:56:28.583403+01:00 - ZipAndRemoveFolderWorker.start: ✅ removed screenshot_folder
[DEBUG] 2026-02-08T10:56:28.583446+01:00 - ZipAndRemoveFolderWorker.start: ✅ ZipAndRemoveFolderWorker.start: done
[DEBUG] 2026-02-08T10:56:29.014565+01:00 - fit_bootstrap.privilege: sudo failed, exit code: -11
[DEBUG] 2026-02-08T10:56:29.014961+01:00 - Bootstrap._dispatch: ❌ Elevation failed
[DEBUG] 2026-02-08T10:56:29.015809+01:00 - main.fit_web: ❌ Admin permissions denied
[DEBUG] 2026-02-08T10:56:38.786084+01:00 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 65561
[DEBUG] 2026-02-08T10:56:38.787168+01:00 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True
[DEBUG] 2026-02-08T10:58:26.657248+01:00 - argv: ['main.py', '--debug', 'verbose']
[DEBUG] 2026-02-08T10:58:26.657516+01:00 - bundled: False



