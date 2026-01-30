aggiunti log in:
scraper.py
privilege.py
zip_and_remove_folder.py completamente modificato
headers.py


riportate modifiche:

Ho aggiornato headers.py per:

aggiungere un User‑Agent “browser-like”
fare fallback HEAD se il GET ritorna 403
in caso di 403 persistente, ritornare comunque gli headers (senza far fallire il task)
Modifica in:






Da risolvrare:

si è riverificato errore per cui abbiamo messo debug privilege.py ora mi sembra più analizzabile: 

[DEBUG] 2026-01-29T15:10:59.701472+01:00 - Web.on_start_tasks_finished: Finished executing all tasks in the start_tasks list of Acquisition.
[DEBUG] 2026-01-29T15:11:02.995400+01:00 - privilege: ❌ osascript failed (code=1) stderr=0:267: execution error: PasteBoard: Error creating pasteboard: com.apple.pasteboard.clipboard [-4960]
PasteBoard: Error creating pasteboard: com.apple.pasteboard.find [-4960]
qt.core.qmetaobject.connectslotsbyname: QMetaObject::connectSlotsByName: No matching signal for on_start_tasks_finished()
qt.core.qmetaobject.connectslotsbyname: QMetaObject::connectSlotsByName: No matching signal for on_stop_tasks_finished()
qt.core.qmetaobject.connectslotsbyname: QMetaObject::connectSlotsByName: No matching signal for on_post_acquisition_finished()
2026-01-29 15:10:50.539 Python[79528:6145707] NOT IMPLEMENTED - CopyPropertiesForAllFonts (1011)
[DEBUG] 2026-01-29T15:11:02.995955+01:00 - ❌ Elevation failed
[DEBUG] 2026-01-29T15:11:02.996118+01:00 - Main.fit_web: ❌ Bootstrap error: Elevation failed
[DEBUG] 2026-01-29T15:11:02.996586+01:00 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 79463
[DEBUG] 2026-01-29T15:11:02.996817+01:00 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True