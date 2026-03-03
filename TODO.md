- ISSUE CONOSCIUTA: mitproxy non funziona corettamente con amazon.com
- ISSUE CONOSCIUTA: su google per scorrere il popup è un problema

- TODO Aggiungere .ico su dialog askpassword
- TODO Da aggiungere test a fit-web
- TODO Gestione aggiornamento app

- TODO Aggiungere al tests plan:
    - accesso sito con credenziali eg facebook e acquisizione audio e video di un video
    - test di tutti i controlli su configurazione, prima acquisizazione


- TODO con fit-screen-recorder
    - Devo aggiungere il display su cui voglio effettuare la registrazione
    - Devo cambiare la logica in fit-configuration per la gestione della registrazione audio e video

- TODO dovrò bloccare su il bundle fit lo scraper fit-web se non usi un macOS
- TODO dovrò fare configurations inteligente che mostra le aree in base allo scraper


Errore difficile da replicare

*** Terminating app due to uncaught exception 'NSInternalInconsistencyException', reason: '-[HIRunLoopSemaphore wait:] has been invoked on a secondary thread; the problem is likely in a much shallower frame in the backtrace'
*** First throw call stack:
(
        0   CoreFoundation                      0x00000001972238fc __exceptionPreprocess + 176
        1   libobjc.A.dylib                     0x0000000196cfa418 objc_exception_throw + 88
        2   Foundation                          0x000000019936f5b4 _userInfoForFileAndLine + 0
        3   HIServices                          0x000000019e81e9c4 -[HIRunLoopSemaphore wait:].cold.1 + 84
        4   HIServices                          0x000000019e80362c -[HIRunLoopSemaphore wait:] + 292
        5   HIToolbox                           0x00000001a3df7544 __62-[IMKInputSessionXPCInvocation_Modern invocationAwaitXPCReply]_block_invoke + 72
        6   HIToolbox                           0x00000001a3df7ea4 +[IMKInputSession_Modern withActivity:performActions:] + 196
        7   HIToolbox                           0x00000001a3ee7228 -[IMKInputSessionXPCInvocation_Modern invocationAwaitXPCReply] + 116
        8   HIToolbox                           0x00000001a3df9488 -[IMKInputSession_Modern deactivate] + 892
        9   HIToolbox                           0x00000001a3d9cc70 IMKInputSessionDeactivate + 40
        10  HIToolbox                           0x00000001a3d9bffc DeactivateInputMethodInstance + 68
        11  HIToolbox                           0x00000001a3d8d034 utDeactivateAllSelectedIMInDocIterator + 96
        12  CoreFoundation                      0x00000001971aaac0 CFArrayApplyFunction + 72
        13  HIToolbox                           0x00000001a3ec98c8 utDeactivateAllSelectedIMInDoc + 120
        14  HIToolbox                           0x00000001a3ec6b80 MyDeactivateTSMDocument + 348
        15  HIToolbox                           0x00000001a3ec73d0 MyActivateTSMDocument.cold.1 + 72
        16  HIToolbox                           0x00000001a3d8b4e4 MyActivateTSMDocument + 1788
        17  AppKit                              0x000000019b6ae47c -[NSTextInputContext activate] + 480
        18  AppKit                              0x000000019c4868dc +[NSTextInputContext currentInputContext_withFirstResponderSync:] + 240
        19  AppKit                              0x000000019c29a460 -[NSView _setWindow:] + 880
        20  AppKit                              0x000000019b60d358 -[NSView removeFromSuperview] + 216
        21  libqcocoa.dylib                     0x0000000111fb98d0 _ZN20QCocoaSystemTrayIcon13emitActivatedEv + 142040
        22  AppKit                              0x000000019c2ca0d0 -[NSWindow setContentView:] + 72
        23  libqcocoa.dylib                     0x0000000111fd10cc _ZN20QCocoaSystemTrayIcon13emitActivatedEv + 238292
        24  libqcocoa.dylib                     0x0000000111f9f884 _ZN20QCocoaSystemTrayIcon13emitActivatedEv + 35468
        25  libqcocoa.dylib                     0x0000000111f9fbfc _ZN20QCocoaSystemTrayIcon13emitActivatedEv + 36356
        26  QtGui                               0x00000001090a89ec _ZN14QWindowPrivate7destroyEv + 196
        27  QtWidgets                           0x000000010a937a9c _ZN14QWidgetPrivate35invalidateBackingStore_resizeHelperERK6QPointRK5QSize + 9936
        28  QtWidgets                           0x000000010a937bbc _ZN14QWidgetPrivate35invalidateBackingStore_resizeHelperERK6QPointRK5QSize + 10224
        29  QtWidgets                           0x000000010a90f5e0 _ZN7QWidget7destroyEbb + 760
        30  QtWidgets                           0x000000010a90ebe0 _ZN7QWidgetD2Ev + 1172
        31  QtWidgets                           0x000000010a9f2c34 _ZN25QComboBoxPrivateContainerD0Ev + 140
        32  QtWidgets                           0x000000010a9f6094 _ZN9QComboBoxD2Ev + 140
        33  QtWidgets.abi3.so                   0x000000010a35b254 _ZN16QComboBoxWrapperD0Ev + 64
        34  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        35  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        36  QtWidgets.abi3.so                   0x000000010a335df0 _ZN13QFrameWrapperD0Ev + 64
        37  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        38  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        39  QtWidgets.abi3.so                   0x000000010a335df0 _ZN13QFrameWrapperD0Ev + 64
        40  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        41  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        42  QtWidgets.abi3.so                   0x000000010a335df0 _ZN13QFrameWrapperD0Ev + 64
        43  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        44  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        45  QtWidgets.abi3.so                   0x000000010a335df0 _ZN13QFrameWrapperD0Ev + 64
        46  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        47  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        48  QtWidgets.abi3.so                   0x000000010a335df0 _ZN13QFrameWrapperD0Ev + 64
        49  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        50  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        51  QtWidgets.abi3.so                   0x000000010a335df0 _ZN13QFrameWrapperD0Ev + 64
        52  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        53  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        54  QtWidgets.abi3.so                   0x000000010a335df0 _ZN13QFrameWrapperD0Ev + 64
        55  QtCore                              0x00000001098c9474 _ZN14QObjectPrivate14deleteChildrenEv + 168
        56  QtWidgets                           0x000000010a90ebc4 _ZN7QWidgetD2Ev + 1144
        57  QtWidgets.abi3.so                   0x000000010a371cc8 _ZN14QDialogWrapperD0Ev + 64
        58  libshiboken6.abi3.6.9.dylib         0x00000001083891dc _ZL23SbkDeallocWrapperCommonP7_objectb + 344
        59  Python                              0x0000000103202d30 subtype_dealloc + 744
        60  Python                              0x00000001031916a0 method_dealloc + 244
        61  Python                              0x00000001031cd77c dictkeys_decref + 172
        62  Python                              0x00000001031d0818 dict_dealloc + 240
        63  libshiboken6.abi3.6.9.dylib         0x000000010839ea6c _ZL18SbkObject_tp_clearP7_object + 104
        64  Python                              0x00000001032ff040 gc_collect_main + 1164
        65  Python                              0x00000001032feb34 gc_collect_with_callback + 76
        66  Python                              0x00000001032ffa74 _Py_RunGC + 84
        67  Python                              0x00000001032b2c20 _Py_HandlePending + 240
        68  Python                              0x0000000103279188 _PyEval_EvalFrameDefault + 632
        69  Python                              0x000000010319127c method_vectorcall + 184
        70  Python                              0x0000000103284e74 _PyEval_EvalFrameDefault + 48996
        71  Python                              0x000000010318ddf0 _PyObject_FastCallDictTstate + 96
        72  Python                              0x000000010318f31c _PyObject_Call_Prepend + 136
        73  Python                              0x0000000103203ff8 slot_tp_call + 144
        74  Python                              0x000000010318ecdc _PyObject_Call + 124
        75  Python                              0x0000000103284e74 _PyEval_EvalFrameDefault + 48996
        76  Python                              0x0000000103191338 method_vectorcall + 372
        77  Python                              0x0000000103284e74 _PyEval_EvalFrameDefault + 48996
        78  Python                              0x0000000103191338 method_vectorcall + 372
        79  Python                              0x0000000103359ad8 thread_run + 144
        80  Python                              0x00000001032ede10 pythread_wrapper + 48
        81  libsystem_pthread.dylib             0x0000000197137c08 _pthread_start + 136
        82  libsystem_pthread.dylib             0x0000000197132ba8 thread_start + 8
)
libc++abi: terminating due to uncaught exception of type NSException
[DEBUG] 2026-03-03T07:42:49 - fit_bootstrap.privilege: sudo failed, exit code: -6
[DEBUG] 2026-03-03T07:42:49 - Bootstrap._dispatch_macos: ❌ Elevation failed
[DEBUG] 2026-03-03T07:42:49 - main.fit_bootstrap: ❌ Bootstrap error: Accesso ai privilegi di root negato.<br><br><strong style="color:red">FIT non può essere eseguita senza privilegi root.</strong>
[DEBUG] 2026-03-03T07:42:55 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 24253
[DEBUG] 2026-03-03T07:42:55 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True

[DEBUG] 2026-02-28T14:00:12 - fit_bootstrap.privilege: sudo failed, exit code: -11
[DEBUG] 2026-02-28T14:00:12 - Bootstrap._dispatch_macos: ❌ Elevation failed
[DEBUG] 2026-02-28T14:00:12 - main.fit_bootstrap: ❌ Admin permissions denied
[DEBUG] 2026-02-28T14:00:14 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 46043
[DEBUG] 2026-02-28T14:00:14 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True

[DEBUG] 2026-02-28T12:36:08 - fit_bootstrap.privilege: sudo failed, exit code: -11
[DEBUG] 2026-02-28T12:36:08 - Bootstrap._dispatch_macos: ❌ Elevation failed
[DEBUG] 2026-02-28T12:36:08 - main.fit_bootstrap: ❌ Admin permissions denied
[DEBUG] 2026-02-28T12:36:10 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 9278
[DEBUG] 2026-02-28T12:36:10 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True

[DEBUG] 2026-02-28T11:04:18 - fit_bootstrap.privilege: sudo failed, exit code: -5
[DEBUG] 2026-02-28T11:04:18 - Bootstrap._dispatch_macos: ❌ Elevation failed
[DEBUG] 2026-02-28T11:04:18 - main.fit_web: ❌ Admin permissions denied
[DEBUG] 2026-02-28T11:04:20 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 61080
[DEBUG] 2026-02-28T11:04:20 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True

[DEBUG] 2026-02-04T11:02:40 - privilege: sudo failed, exit code: -11
[DEBUG] 2026-02-04T11:02:40 - ❌ Elevation failed
[DEBUG] 2026-02-04T11:02:40 - main.fit_web: ❌ Admin permissions denied
[DEBUG] 2026-02-04T11:02:53 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 17749
[DEBUG] 2026-02-04T11:02:53 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True


[DEBUG] 2026-02-08T10:56:29.014565+01:00 - fit_bootstrap.privilege: sudo failed, exit code: -11
[DEBUG] 2026-02-08T10:56:29.014961+01:00 - Bootstrap._dispatch: ❌ Elevation failed
[DEBUG] 2026-02-08T10:56:29.015809+01:00 - main.fit_web: ❌ Admin permissions denied
[DEBUG] 2026-02-08T10:56:38.786084+01:00 - MitmproxyRunner.stop_by_pid: Sent SIGINT to mitmproxy pid 65561
[DEBUG] 2026-02-08T10:56:38.787168+01:00 - MitmproxyRunner.stop_by_pid: ℹ️ HAR exists: True
[DEBUG] 2026-02-08T10:58:26.657248+01:00 - argv: ['main.py', '--debug', 'verbose']
[DEBUG] 2026-02-08T10:58:26.657516+01:00 - bundled: False



