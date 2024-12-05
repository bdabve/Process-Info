#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import qtawesome as qta


def interface_icons(root):
    # PROCESS PAGE
    # -------------------
    root.ui.buttonProcess.setIcon(qta.icon('mdi.alpha-p-box', color="#ffffff"))
    root.ui.buttonProcess.clicked.connect(root.goto_process_page)

    # search button icon
    root.ui.searchButtonIcon.setIcon(qta.icon('ri.search-line', color="#ffffff"))

    # SERVICE PAGE
    # -------------------
    root.ui.buttonService.setIcon(qta.icon('mdi.alpha-s-box', color="#ffffff"))

    # MACHINE INFO PAGE
    # -------------------
    root.ui.buttonMachineInfo.setIcon(qta.icon('mdi.laptop-mac', color="#ffffff"))

    # DETAILS PAGE
    # -------------------
    # close card button
    root.ui.buttonCloseCard.setIcon(qta.icon('ri.close-fill', color="#ffffff"))
    root.ui.buttonCloseCard.clicked.connect(root.ui.dockWidget.close)

    # resume, suspend, terminate buttons
    root.ui.buttonTerminate.setIcon(qta.icon('mdi6.skull', color="#ffffff"))
    root.ui.buttonTerminate.clicked.connect(lambda: root.handle_process('terminate'))

    root.ui.buttonResume.setIcon(qta.icon('fa5s.walking', color="#ffffff"))
    root.ui.buttonResume.clicked.connect(lambda: root.handle_process('resume'))

    root.ui.buttonSuspend.setIcon(qta.icon('mdi.motion-pause-outline', color="#ffffff"))
    root.ui.buttonSuspend.clicked.connect(lambda: root.handle_process('suspend'))

    root.ui.buttonProcessMoreInfo.setIcon(qta.icon('mdi6.information-variant', color="#ffffff"))
    root.ui.buttonProcessMoreInfo.clicked.connect(root.process_more_details)
