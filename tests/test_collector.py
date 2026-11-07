import importlib.util
import pathlib
import unittest

path=pathlib.Path(__file__).resolve().parents[1]/'scripts'/'collect.py'
spec=importlib.util.spec_from_file_location('collector',path)
c=importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

class TestFeed(unittest.TestCase):
    def test_rss_economy_only(self):
        xml=b'''<rss><channel>
          <item><title>Ethiopia coffee exports increase</title><link>https://example.org/coffee?utm_source=x</link><pubDate>Fri, 06 Nov 2026 12:00:00 GMT</pubDate></item>
          <item><title>Football team scores</title><link>https://example.org/sports</link><pubDate>Fri, 06 Nov 2026 12:00:00 GMT</pubDate></item>
        </channel></rss>'''
        items=c.extract(xml,{'name':'Example','ethiopiaFocused':True})
        self.assertEqual(len(items),1)
        self.assertEqual(items[0]['url'],'https://example.org/coffee')
        self.assertIn('Trade & Exports',items[0]['categories'])
    def test_atom(self):
        xml=b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Ethiopia bank expands lending</title><link href="https://example.org/bank"/><updated>2026-11-06T09:00:00Z</updated></entry></feed>'''
        items=c.extract(xml,{'name':'Example','ethiopiaFocused':False})
        self.assertEqual(len(items),1)
        self.assertIn('Banking & Finance',items[0]['categories'])
    def test_reject_non_http(self):
        self.assertIsNone(c.normalize_url('javascript:alert(1)'))
if __name__=='__main__':unittest.main()
