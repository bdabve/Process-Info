#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import qtawesome as qta


def interface_icons(root):
    # PROCESS BUTTON
    root.ui.buttonProcess.setIcon(qta.icon('mdi.alpha-p-box', color="#ffffff"))
    root.ui.buttonProcess.clicked.connect(root.goto_process_page)

    # SERVICE BUTTON
    root.ui.buttonService.setIcon(qta.icon('mdi.alpha-s-box', color="#ffffff"))

    # Machine info
    root.ui.buttonMachineInfo.setIcon(qta.icon('mdi.laptop-mac', color="#ffffff"))

    # CLOSE CARD BUTTON
    root.ui.buttonCloseCard.setIcon(qta.icon('ri.close-fill', color="#ffffff"))
    root.ui.buttonCloseCard.clicked.connect(root.ui.dockWidget.close)

    # search button icon
    root.ui.searchButtonIcon.setIcon(qta.icon('ri.search-line', color="#ffffff"))

    # RESUME, SUSPEND, TERMINATE BUTTONS
    root.ui.buttonTerminate.setIcon(qta.icon('mdi6.skull', color="#ffffff"))
    root.ui.buttonTerminate.clicked.connect(lambda: root.handle_process('terminate'))
    root.ui.buttonResume.setIcon(qta.icon('fa5s.walking', color="#ffffff"))
    root.ui.buttonResume.clicked.connect(lambda: root.handle_process('resume'))
    root.ui.buttonSuspend.setIcon(qta.icon('mdi.motion-pause-outline', color="#ffffff"))
    root.ui.buttonSuspend.clicked.connect(lambda: root.handle_process('suspend'))
