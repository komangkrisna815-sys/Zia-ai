import os,threading,json,io,zipfile
os.environ['APP_PASSWORD']='browser-test-password'
os.environ['APP_ORIGIN']='http://127.0.0.1:3194'
import app
from wsgiref.simple_server import make_server,WSGIRequestHandler
class Quiet(WSGIRequestHandler):
 def log_message(self,*a):pass
def fixture(messages,instructions=app.POLICY):
 if 'Return ONLY JSON:' in instructions:
  count=json.loads(messages[0]['content'])['count'];return {'text':json.dumps({'slides':[{'title':'Fixture slide '+str(i+1),'bullets':['Test content only'],'notes':'Fixture notes'} for i in range(count)]})}
 return {'text':'## Test fixture\nMocked browser-test answer, not live AI.','model':'mock','usage':{}}
app.generate=fixture
server=make_server('127.0.0.1',3194,app.application,handler_class=Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
from playwright.sync_api import sync_playwright,expect
import re
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox','--single-process','--disable-dev-shm-usage','--disable-gpu'],timeout=5000)
  try:
   page=browser.new_page(viewport={'width':1280,'height':900});page.set_default_timeout(2500);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:3194');page.get_by_label('Kata sandi workspace').fill('browser-test-password');page.get_by_role('button',name='Masuk',exact=True).click();page.get_by_role('heading',name='Ide besar dimulai dari percakapan.').wait_for()
   page.get_by_role('button',name='Zia Chat',exact=True).click();page.get_by_label('Pesan untuk Zia AI').fill('Explain AI');page.get_by_role('button',name='Kirim',exact=True).click();page.get_by_role('heading',name='Test fixture',exact=True).wait_for();page.get_by_label('Pesan untuk Zia AI').fill('Make it shorter');page.get_by_label('Pesan untuk Zia AI').press('Enter');expect(page.locator(".message.assistant")).to_have_count(2)
   page.get_by_role('button',name='Zia Writer',exact=True).click();page.get_by_label('Topik / instruksi').fill('Email untuk dosen');page.get_by_role('button',name='Buat',exact=True).click();expect(page.locator("#editor")).to_have_value(re.compile("Test fixture"))
   page.get_by_role('button',name='Zia Presentation',exact=True).click();page.get_by_label('Topik presentasi').fill('Pengenalan AI');page.get_by_label('Jumlah slide').select_option('2')
   with page.expect_download() as download_info:page.get_by_role('button',name='Buat & unduh PowerPoint',exact=True).click()
   download=download_info.value
   with zipfile.ZipFile(download.path()) as z:assert z.testzip() is None;assert 'ppt/slides/slide2.xml' in z.namelist()
   page.get_by_role('button',name='Zia Voice',exact=True).click();page.get_by_label('Transkrip / fallback teks').fill('Fallback text available')
   page.set_viewport_size({'width':390,'height':844});page.reload();page.get_by_role('heading',name='Ide besar dimulai dari percakapan.').wait_for();assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth');assert not errors,errors
   print(json.dumps({'browser':'Chromium headless','passed':['login','dashboard','chat mock UI','follow-up Enter submission','Markdown heading','Writer mock output','PPTX browser download and ZIP check using fixture content','voice fallback form','mobile width 390px overflow check','no uncaught page errors'],'not_tested':['live AI','microphone','audible output','public deployment']}))
  finally:browser.close()
finally:server.shutdown();server.server_close()
