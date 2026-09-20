import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

spec=importlib.util.spec_from_file_location('exporter',Path(__file__).resolve().parents[1]/'scripts/export_xmp.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class ExportTest(unittest.TestCase):
    def render(self,settings,**extra):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.xmp'
            m.export({'name':'Warm & Punchy','group':'Tests','settings':settings,**extra},path)
            return ET.parse(path).find('.//'+m.q('rdf','Description'))
    def test_nonraw_wb(self):
        d=self.render({'IncrementalTemperature':10,'IncrementalTint':0,'Contrast2012':24})
        self.assertEqual(d.get(m.q('crs','WhiteBalance')),'Custom')
        self.assertEqual(d.get(m.q('crs','IncrementalTemperature')),'10')
        self.assertIsNone(d.get(m.q('crs','Temperature')))
    def test_raw_wb(self):
        d=self.render({'Temperature':6000,'Tint':3})
        self.assertEqual(d.get(m.q('crs','WhiteBalance')),'Custom')
        self.assertEqual(d.get(m.q('crs','Temperature')),'6000')
    def test_preserve_wb(self):
        self.assertIsNone(self.render({'Contrast2012':24}).get(m.q('crs','WhiteBalance')))
    def test_invalid_controls(self):
        for settings in [{'Temperature':6000,'IncrementalTemperature':10},{'IncrementalTemperature':101},{'Temperature':True},{'Contrast2012':float('nan')},{'Unknown':1}]:
            with self.subTest(settings=settings),self.assertRaises(ValueError):
                self.render(settings)
    def test_invalid_curve(self):
        with self.assertRaises(ValueError):
            self.render({'Contrast2012':5},curves={'ToneCurvePV2012':[[0,0],[20,30],[20,40],[255,255]]})
if __name__=='__main__':
    unittest.main()
