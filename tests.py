import os
from shutil import copyfile
from main import get_content, save_content
import tempfile


def test_get_content_1():
	base_path = tempfile.mkdtemp()
	os.makedirs(base_path + '/foo/bar/')
	copyfile('test.md', base_path + '/foo/bar/index.md')
	assert '# test' == get_content('/foo/bar', base_path)
	copyfile('test.md', base_path + '/foo/bar/bla.md')
	assert '# test' == get_content('/foo/bar/bla', base_path)
	assert None == get_content('/foo', base_path)
	os.makedirs(base_path + '/foo/bar/blubb')
	copyfile('test.md', base_path + '/foo/bar/blubb/index.md')
	assert '# test' == get_content('/foo/bar/blubb', base_path)
	assert None == get_content('/foo/bar/po/argh', base_path)


def test_save_content_1():
	base_path = tempfile.mkdtemp()
	save_content('/foo', 'test1', base_path)
	assert 'test1' == open(base_path + '/foo.md').read()
	#this should move foo.md to index.md and create foo dir	
	save_content('/foo/bar', 'test2', base_path)
	#assert 'test1' == open(base_path + '/foo/index.md').read()	
	assert 'test2' == open(base_path + '/foo/bar.md').read()	
	save_content('/foo/bar/blubber/blubb', 'test3', base_path)
	assert 'test3' == open(base_path + '/foo/bar/blubber/blubb.md').read()	
