#!/usr/bin/env python3

import os, sys
from datetime import datetime, timezone
from optparse import OptionParser
from subprocess import Popen, PIPE, STDOUT
from markdown import Markdown
from glob import glob
from re import compile
from pwd import getpwuid

HOOKPOINT_INIT = 0
HOOKPOINT_PARSE = 1

def extFileName(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		bname = os.path.basename(filename)
		fname, fext = os.path.splitext(bname)

		files[filename]['input-path'] = filename
		files[filename]['input-name'] = fname
		files[filename]['input-ext'] = fext
		files[filename]['input-basename'] = bname

		if options.output:
			bname = os.path.basename(options.output)
			fname, fext = os.path.splitext(bname)

			files[filename]['output-path'] = options.output
			files[filename]['output-name'] = fname
			files[filename]['output-ext'] = fext
			files[filename]['output-basename'] = bname

def extStat(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		stat = os.stat(filename)
		files[filename]['input-date-update'] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime(options.date_fmt)
		if hasattr(stat, 'st_birthtime'):
			files[filename]['input-date-create'] = datetime.fromtimestamp(stat.st_birthtime, tz=timezone.utc).strftime(options.date_fmt)
		else:
			files[filename]['input-date-create'] = datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).strftime(options.date_fmt)
		files[filename]['input-owner'] = getpwuid(stat.st_uid).pw_name

def extGit(*args):
	if args[0] == HOOKPOINT_INIT:
		parser = args[1]
		parser.add_option('-g', '--git-dir', dest='git_dir', default='%s/.git' % os.path.dirname(sys.argv[0]), help='Set GIT directory location, e.g. /home/user/repo/.git')

	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]

		def stdResult(gitStdOut, gitStdErr):
			return ('<font color="red">%s</font>' % gitStdErr.decode()) if gitStdErr else gitStdOut.decode()

		gitDir = '--git-dir="%s"' % options.git_dir
		date = '"--date=format:%s"' % options.date_fmt

		# git --git-dir="%s" log -1 "--date=format:%s" --format=%ad -- filename
		p = Popen(['git', gitDir, 'log', '-1', date, '--format=%ad', '--', filename], stdout=PIPE, stderr=PIPE)
		gitStdOut, gitStdErr = p.communicate()
		files[filename]['input-date-commit'] = stdResult(gitStdOut, gitStdErr)

		# git --git-dir="%s" log -1 "--format=%an <%ae>" -- filename
		p = Popen(['git', gitDir, 'log', '-1', '"--format=%an <%ae>"', '--', filename], stdout=PIPE, stderr=PIPE)
		gitStdOut, gitStdErr = p.communicate()
		files[filename]['input-commiter'] = stdResult(gitStdOut, gitStdErr)

		# git --git-dir="%s" log -1 "--date=format:%s" --format=%ad --diff-filter=A -- filename
		p = Popen(['git', gitDir, 'log', '-1', date, '--format=%ad', '--diff-filter=A', '--', filename], stdout=PIPE, stderr=PIPE)
		gitStdOut, gitStdErr = p.communicate()
		files[filename]['input-date-add'] = stdResult(gitStdOut, gitStdErr)

		# git --git-dir="%s" log -1 "--format=%an <%ae>" --diff-filter=A -- filename
		p = Popen(['git', gitDir, 'log', '-1', '"--format=%an <%ae>"', '--diff-filter=A', '--', filename], stdout=PIPE, stderr=PIPE)
		gitStdOut, gitStdErr = p.communicate()
		files[filename]['input-author'] = stdResult(gitStdOut, gitStdErr)

def extCustom(*args):
	if args[0] == HOOKPOINT_INIT:
		parser = args[1]
		parser.add_option('-a', '--add', dest='params', action="append", help='Add parameter in format name:value')

	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		if options.params:
			for p in options.params:
				name, value = p.split(':')
				files[filename][name] = value

# example: %(input-file-date:1.md)s
extMetaPattern = compile('%\((([^:\)]+):([^:\)]+))\)')

def extMeta(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		sourceDir = os.path.dirname(options.source)
		for it in extMetaPattern.finditer(files[filename]['source']):
			if options.trace:
				print('[meta] triggered on %s at %s' % (it.group(0), it.span(0)), file=sys.stderr)

			name = it.group(2)
			path = it.group(3)
			dependency = '%s/%s' % (sourceDir, path)
			stack.append(dependency)
			if dependency not in files[filename]['dependencies']:
				files[filename]['dependencies'][dependency] = []

			files[filename]['dependencies'][dependency].append((it.group(1), name, lambda a, b: b))

# example: %(glob:row:*.md)s
extGlobPattern = compile('%\((glob:([^:\)]+):([^:\)]+))\)')

def extGlob(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		sourceDir = os.path.dirname(options.source)
		for it in extGlobPattern.finditer(files[filename]['source']):
			if options.trace:
				print('[glob] triggered on %s at %s' % (it.group(0), it.span(0)), file=sys.stderr)

			name = it.group(2)
			mask = it.group(3)

			if options.trace:
				print('[glob] glob path %s/%s' % (sourceDir, mask), file=sys.stderr)

			for g in glob('%s/%s' % (sourceDir, mask)):
				if options.trace:
					print('[glob] add dependency from %s: %s, %s' % (g, it.group(1), name), file=sys.stderr)

				stack.append(g)
				if g not in files[filename]['dependencies']:
					files[filename]['dependencies'][g] = []

				files[filename]['dependencies'][g].append((it.group(1), name, lambda a, b: a + b))

extensions = {
	'filename': extFileName,
	'stat': extStat,
	'git': extGit,
	'custom': extCustom,
	'meta': extMeta,
	'glob': extGlob,
}

def main(options):
	if options.source is None or options.html is None or options.trace is None or options.markdown_ext is None or options.date_fmt is None or options.ext is None:
		print('error: invalid parameter', file=sys.stderr)
		return False

	hooks = []
	files = {}
	stack = [options.source]

	if options.ext:
		for e in list(set(options.ext.split(','))):
			if e not in extensions:
				print('error: invalid extension "%s"' % e, file=sys.stderr)
				return False

			hooks.append(extensions[e])

	with open(options.html) as f:
		html = f.read()

	while len(stack):
		filename = stack[-1]
		stack = stack[:-1]

		if options.trace:
			print('parse %s...' % filename, file=sys.stderr)

		with open(filename) as f:
			files[filename] = {
				'dependencies': {},
				'source': f.read(),
			}

		# hook point
		for hook in hooks:
			hook(HOOKPOINT_PARSE, filename, stack, files, options)

	while len(files):

		indep = [filename for filename in files if len(files[filename]['dependencies']) == 0]
		if len(indep) == 0:
			print('error: dependency loop', file=sys.stderr)
			return False

		filename = indep[0]

		if options.trace:
			print('generate %s...' % filename, file=sys.stderr)

		if 'document' not in files[filename]:
			md = Markdown(extensions=options.markdown_ext.split(','))

			files[filename]['body'] = md.convert(files[filename]['source'])

			if md.Meta:
				toFormat = []
				for metaName in md.Meta:
					files[filename][metaName] = ''.join(md.Meta[metaName])
					toFormat.append(metaName)

				if options.trace:
					print('format metadata: %s...' % toFormat, file=sys.stderr)

				for metaName in toFormat:
					files[filename][metaName] = files[filename][metaName] % files[filename]

			files[filename]['body'] = files[filename]['body'] % files[filename]
			files[filename]['document'] = html % files[filename]
	
		for i in files:
			if filename in files[i]['dependencies']:
				if options.trace:
					print('update dependencies for %s (%s)...' % (i, len(files[i]['dependencies'][filename])), file=sys.stderr)

				for dst, src, action in files[i]['dependencies'][filename]:
					if options.trace:
						print('set %%(%s)=%%(%s)' % (dst, src), file=sys.stderr)

					files[i][dst] = action(files[i][dst] if (dst in files[i]) else '', files[filename][src])
				del files[i]['dependencies'][filename]

		if filename == options.source:
			if options.output:
				with open(options.output, 'w') as f:
					f.write(files[filename]['document'])
			else:
				print(files[filename]['document'])
			break

		del files[filename]

	return True

def main_m():
	parser = OptionParser(usage="python -m mdhtmlgen [options]")
	parser.add_option('-S', '--source', dest='source', help='Markdown source filename (*.md)')
	parser.add_option('-H', '--html', dest='html', help='HTML template filename (*.t)')
	parser.add_option('-t', '--trace', dest='trace', action='store_true', default=False, help='Print diagnostic traces')
	parser.add_option('-o', '--output', dest='output', help='Set output file')
	parser.add_option('-m', '--markdown-ext', dest='markdown_ext', default='', help='Set markdown extension list, coma separated, e.g. meta,toc,footnotes,...')
	parser.add_option('-d', '--date-fmt', dest='date_fmt', default='%Y-%m-%d %H:%M:%S', help='Set date format, e.g. %Y-%m-%d %H:%M:%S')
	parser.add_option('-e', '--ext', dest='ext', default='', help='Set extension list, e.g. meta,glob,filename,date,...')

	# hook point
	for hook in extensions:
		extensions[hook](HOOKPOINT_INIT, parser)

	(options, args) = parser.parse_args()

	if options.source is None or options.html is None:
		parser.print_help()
		exit(1)

	if not main(options):
		exit(1)

if __name__ == '__main__':
	main_m()
