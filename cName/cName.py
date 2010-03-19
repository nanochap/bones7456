#!/usr/bin/env python
# encoding: utf-8
import gtk, webkit, os.path, re

reg = re.compile(r'\{\{(.+?\|.+?\|.+?)\}\}')
reg1 = re.compile(r'&lt;py&gt;')
reg2 = re.compile(r'&lt;/py&gt;')
cat = {
'字体图片':'1b',
'字源图片':'zy',
'字形图片':'zx'
}

class WV(webkit.WebView):
    def __init__(self, html=''):
        webkit.WebView.__init__(self)
        self.open(html)
    def open(self, html):
        webkit.WebView.open(self, html)

class MainWindow:
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_default_size(750, 550)
        self.window.set_title('cName')

        self.vbox = gtk.VBox(False, 0)
        self.runpath = os.path.dirname(os.path.abspath(__file__))
        wel = os.path.join(self.runpath, 'welcome.html')
        self.wv = WV(wel)
        self.e = gtk.Entry()
        self.e.connect('activate', self.refresh)
        self.vbox.pack_start(self.e, False, False)
        sw = gtk.ScrolledWindow()
        sw.add(self.wv)
        self.vbox.pack_start(sw)

        self.window.add(self.vbox)
        self.window.connect("delete_event", self.on_close)
        self.window.show_all()
        
    def refresh(self, obj):
        self.show(obj.get_text().decode('utf8')[0])
        
    def show(self, c):
        from wikimarkup import parse
        f = os.path.join(self.runpath, 'data', '%s.wiki' % c)
        if os.path.exists(f):
            wiki = open(f).read()
            wiki = reg.sub(self._pic, wiki)
            wiki = reg1.sub('(', wiki)
            wiki = reg2.sub(')', wiki)
            html = parse(wiki, showToc=False)
            self.wv.load_html_string(html, 'file:///')
        else:
            self.wv.open(os.path.join(self.runpath, 'err.html'))
        
    def _pic(self, m):
        i1, i2, i3 = m.group(1).split('|')
        f = '_'.join([cat[i1], i2, i3]) + '.gif'
        f = os.path.join(self.runpath, 'pic', f)
        return '<img src="%s"/>' % f
        
    def on_close(self, *args):
        gtk.main_quit()

def main():
    gtk.gdk.threads_init()
    m = MainWindow()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()

if __name__ == '__main__':
    main()
