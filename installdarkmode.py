import subprocess
import sys
import os

installFolders = ['/Applications/Slack.app', 'C:/Users/User/AppData/Local/slack']

def find(name, path) :
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def createJavascript() :
	# Modify colors.css to change your theme colors
	colors = ''
	with open('colors.css', 'r') as colorfile :
		colors = colorfile.read()

	jsmod = """
	function darkMode() {
		allcss = '';
		regex = /rgb[\\(a]{1,2}/;
		for (s = 0; s < document.styleSheets.length; s++)
		{
			for (i = 0; i < document.styleSheets[s].cssRules.length; i++)
			{
				if (regex.test(document.styleSheets[s].cssRules[i].cssText))
				{ allcss = allcss + document.styleSheets[s].cssRules[i].cssText + '\\n'; }
			}
		}

		replacements = [
			{"rgb(255, 255, 255)": "var(--background)"},
			{"rgb(97, 96, 97)": "var(--text-subtle)"},
			{"rgb(221, 221, 221)": "var(--border-dim)"},
			{"rgb(29, 28, 29)": "var(--text)"},
			{"rgb(58, 163, 227)": "var(--primary)"},
			{"rgb(18, 100, 163)": "var(--primary)"},
			{"rgb(134, 134, 134)": "var(--text-subtle)"},
			{"rgb(29, 155, 209)": "var(--primary)"},
			{"rgb(248, 248, 248)": "var(--background-hover)"},
			{"rgba(29, 28, 29, 0.7)": "var(--text-subtle)"},
			{"rgb(0, 122, 90)": "var(--online)"},
			{"rgb(224, 30, 90)": "var(--text-code)"},
			{"rgba(29, 155, 209, 0.3)": "var(--primary)"},
			{"rgb(11, 76, 140)": "var(--primary)"},
			{"rgba(29, 28, 29, 0.13)": "var(--text-subtle)"},
			{"rgb(232, 145, 45)": "var(--private)"},
			{"rgb(247, 247, 249)": "var(--background-code)"},
			{"rgba(29, 28, 29, 0.5)": "var(--text-subtle)"},
			{"rgba(29, 28, 29, 0.52)": "var(--text-subtle)"},
			{"rgb(232, 245, 250)": "var(--text-special-hover)"},
			{"rgb(0, 0, 0)": "var(--background-bright)"},
			{"rgba(0, 0, 0, 0)": "transparent"},
			{"rgba(0, 0, 0, 0.1)": "var(--background-light)"},
			{"rgba(0, 0, 0, 0.08)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.15)": "var(--border-dim)"},
			{"rgba(0, 0, 0, 0.2)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.26)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.25)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.35)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.5)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.05)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.075)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.4)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.3)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.7)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.12)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.07)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.6)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.14)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.06)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.9)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.11)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.8)": "var(--text-subtle)"},
			{"rgba(0, 0, 0, 0.85)": "var(--text-subtle)"},
			{"rgba(255, 255, 255, 0.95)": "var(--background)"},
			{"rgb(34, 34, 34)": "var(--background-code)"},
			{"rgb(51, 51, 51)": "var(--text-code)"}
		];

		for (i = 0; i < replacements.length; i++)
		{
			regex = new RegExp(Object.keys(replacements[i])[0].replace('(','\\\\(').replace(')','\\\\)'), 'g');
			allcss = allcss.replace(regex, Object.values(replacements[i])[0]);
		}

		allcss = '{your colors will go here}' + allcss

		$('<style></style>').appendTo('head').html(allcss);
	}

	if (window.addEventListener)
		window.addEventListener('load', darkMode, false);
	else if (window.attachEvent)
		window.attachEvent('onload', darkMode);
	else window.onload = darkMode;
	"""

	return jsmod.replace('{your colors will go here}', colors.replace('\n', ' '))

def install() :
	jsmod = createJavascript()

	installDirectory = ''

	for installFolder in installFolders :
		if os.path.isdir(installFolder) :
			installDirectory = find('ssb-interop.js', installFolder)
			break

	if not installDirectory :
		installFolder = input('Could not find your install directory, please enter your Slack install directory here>')
		installDirectory = find('ssb-interop.js', installFolder)
		if not installDirectory :
			print('failed to find ssb-interop.js')
			exit(1)

	installDirectory = installDirectory.strip()

	ssbinterop = ''
	if not os.path.isfile('ssb-interop-save.js') :
		with open(installDirectory, 'r') as slackjs :
			ssbinterop = slackjs.read()

		if not os.path.isfile('ssb-interop-save.js') :
			with open('ssb-interop-save.js', 'w') as slackjs :
				slackjs.write(ssbinterop)

		ssbinterop = ssbinterop + '\n\n\n' + jsmod

		with open(installDirectory, 'w') as slackjs :
			slackjs.write(ssbinterop)
	else :
		# load from save instead
		with open('ssb-interop-save.js', 'r') as slackjs :
			ssbinterop = slackjs.read()

		ssbinterop = ssbinterop + '\n\n\n' + jsmod

		with open(installDirectory, 'w') as slackjs :
			slackjs.write(ssbinterop)

	print('done, please restart slack.')


def uninstall() :
	installDirectory = ''

	for installFolder in installFolders :
		if os.path.isdir(installFolder) :
			installDirectory = find('ssb-interop.js', installFolder)
			break

	if not installDirectory :
		installFolder = input('Could not find your install directory, please enter your Slack install directory here>')
		installDirectory = find('ssb-interop.js', installFolder)
		if not installDirectory : exit()

	installDirectory = installDirectory.strip()

	ssbinterop = ''
	with open('ssb-interop-save.js', 'r') as slackjs :
		ssbinterop = slackjs.read()

	with open(installDirectory, 'w') as slackjs :
		slackjs.write(ssbinterop)

	print('sorry you don\'t like darkmode, you can customize the colors in colors.css.\nfor now, please restart slack.')


if __name__ == '__main__' :
	query = False
	method = 'help'
	params = []
	if len(sys.argv) > 1 :
		if sys.argv[1].startswith('uninst') :
			uninstall()
		elif sys.argv[1].startswith('print') :
			print(createJavascript())
	else : install()
