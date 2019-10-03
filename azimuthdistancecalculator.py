# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AzimuthDistanceCalculator
                                 A QGIS plugin
 Calculates azimuths and distances
                              -------------------
        begin                : 2014-09-24
        copyright            : (C) 2014 by Luiz Andrade
        email                : luiz.claudio@dsg.eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from __future__ import absolute_import
from builtins import object
import os


from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion
from . import resources_rc
from .spugeo_memorial_dialog import SpuGeoMemorialDialog

try:
    import ptvsd
    ptvsd.enable_attach(secret='my_secret', address = ('localhost', 5679))
except:
    pass

class AzimuthDistanceCalculator (object):
    """Contains azimuths distance calculator methods
    """
    def __init__(self, iface):
        """constructor
        :param iface:
        :return:
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'azimuthdistancecalculator_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = AzimuthDistanceCalculatorDialog(self.iface)

        # Obtaining the map canvas
        self.canvas = iface.mapCanvas()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('azimuthdistancecalculator', message)

    def initGui(self):
        """Prepares the plugin interface
        :param
        :return:
        """
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/azimuthdistancecalculatorspu/north.png"),
            self.tr("Azimuth and Distance Calculator for SPU"), self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(self.tr("Azimuth and Distance Calculator"), self.action)

    def unload(self):
        """Remove the plugin menu item and icon
        :param
        :return:
        """
        self.iface.removePluginMenu(self.tr("Azimuth and Distance Calculator"), self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        """run method that performs all the real work
        :param
        :return:
        """
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
