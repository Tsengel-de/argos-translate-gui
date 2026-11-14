import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import unittest
from unittest.mock import Mock, patch

from argostranslategui import gui


class Language:
    def __init__(self, code):
        self.code = self.name = code
        self.get_translation = Mock(return_value=None)


class GUIRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = gui.QApplication.instance() or gui.QApplication([])

    def setUp(self):
        self.languages = [Language('en'), Language('fr'), Language('de')]
        self.loader = patch.object(gui.translate, 'load_installed_languages',
                                   side_effect=lambda: self.languages)
        self.loader.start()
        self.window = gui.GUIWindow()

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()
        self.loader.stop()

    def test_refresh_shrinking_languages_is_atomic(self):
        self.window.right_language_combo.setCurrentIndex(2)
        self.languages = self.languages[:1]
        with patch.object(self.window, 'translate', wraps=self.window.translate) as run:
            self.window.load_languages()
            self.assertEqual(run.call_count, 1)
        self.assertEqual(self.window.right_language_combo.currentIndex(), 0)

    def test_refresh_preserves_language_codes(self):
        self.window.left_language_combo.setCurrentIndex(2)
        self.languages.reverse()
        self.window.load_languages()
        self.assertEqual(self.window.left_language_combo.currentData(), 'de')
        self.assertEqual(self.window.right_language_combo.currentData(), 'fr')

    def test_invalid_selection_does_not_translate(self):
        self.window.left_language_combo.setCurrentIndex(-1)
        for language in self.languages:
            language.get_translation.reset_mock()
        self.window.translate()
        for language in self.languages:
            language.get_translation.assert_not_called()

    def test_uninstall_emits_one_change_after_refresh(self):
        table = gui.PackagesTable.__new__(gui.PackagesTable)
        with patch.object(gui.package, 'get_installed_packages', return_value=[]):
            table.__init__(gui.PackagesTable.TableContent.INSTALLED, [])
        changed = Mock()
        table.packages_changed.connect(changed)
        with patch.object(gui.package, 'uninstall'), patch.object(table, 'populate') as populate:
            table.uninstall_package(object())
            populate.assert_called_once()
        changed.assert_called_once()
        table.deleteLater()


if __name__ == '__main__':
    unittest.main()
