import subprocess
import sys
import os

installFolders = ['/Applications/Slack.app', f"{os.getenv('USERPROFILE')}\\AppData\\Local\\slack", '/usr/lib/slack']

def find(name, path) :
	paths = []
	for root, dirs, files in os.walk(path):
		if name in files:
			paths.append(os.path.join(root, name))
	paths.sort(reverse=True)
	return paths[0]

def createJavascript() :
	global sensitivity
	global cssfile

	jsmod = """
	const replacements = {replacements.json will be added here};

	function convertColor(str)
	{
		let color = [];
		let colorstring = str.match(/[0-9\\.]{1,10}/g);
		for (let l = 0; l < colorstring.length; l++)
		{ color[l] = parseFloat(colorstring[l]); }
		if (colorstring.length < 4)
		{ color[colorstring.length] = 1; }
		return color;
	}
	function compareColors(color1, color2)
	{
		let distance = 0;
		for (let k = 0; k < 3; k++)
		{ distance += (color1[k] - color2[k]) * (color1[k] - color2[k]); }
		if (color1.length > 3 && color2.length > 3)
		{
			const d = (color1[3] * 255) - (color2[3] * 255);
			distance += d * d;
		}
		return Math.sqrt(distance);
	}
	function findReplacement(color)
	{
		if (color.length > 3 && color[3] == 0)
		{ return "transparent"; }
		let lowest = 1000000;
		let index = -1;
		for (let m = 0; m < replacements.length; m++)
		{
			current = compareColors(Object.values(replacements[m])[0], color);
			if (lowest > current)
			{
				lowest = current;
				index = m;
			}
		}
		return lowest < {sensitivity} ? Object.keys(replacements[index])[0] : false;
	}
	function darkMode()
	{
		let allcss = '';
		const regexReplace  = /rgb[a]{0,1}\\([0-9\\., ]{7,}\\)/;
		const regexReplaceg = /rgb[a]{0,1}\\([0-9\\., ]{7,}\\)/g;
		const regexMatchCss = /[a-z0-9A-Z\\-\\_\\.\\#]{1,}\\:[a-z0-9A-Z\\-\\(\\._#, ]{0,}rgb[a]{0,1}\\([0-9\\., ]{7,}\\)[0-9a-zA-Z\\(\\),\\.\\%\\-\\\\/"_@! ]{0,};/g;
		for (let s = 0; s < document.styleSheets.length; s++)
		{
			for (let i = 0; i < document.styleSheets[s].cssRules.length; i++)
			{
				let temprule = document.styleSheets[s].cssRules[i].cssText;
				let newrule = '';
				if (regexMatchCss.test(temprule) && temprule.indexOf('sidebar') < 0 && temprule.indexOf('channels_list') < 0 && temprule.indexOf('#team_menu') < 0)
				{
					let newrules = temprule.match(regexMatchCss);
					for (let j = 0; j < newrules.length; j++)
					{
						let colorstrings = newrules[j].match(regexReplaceg);
						for (let o = 0; o < colorstrings.length; o++)
						{
							replacement = findReplacement(convertColor(colorstrings[o]));
							if (replacement)
							{ newrules[j] = newrules[j].replace(regexReplace, replacement); }
						}
						newrule = newrule + newrules[j] + ' ';
					}
				}

				allcss = allcss + temprule.substring(0, temprule.indexOf('{') + 1) + newrule + '}\\n';
			}
		}

		allcss = '{your colors will go here}' + '\\n' + allcss + '\\n' + '{and overrides will be here}';

		$('<style></style>').appendTo('head').html(allcss);
	}
	"""

	jsmod = jsmod.replace('{sensitivity}', str(sensitivity))

	with open('replacements.json', 'r') as replacementfile :
		replacements = replacementfile.read()
		jsmod = jsmod.replace('{replacements.json will be added here}', replacements.replace('\n', ' '))

	with open(cssfile, 'r') as colorfile :
		colors = colorfile.read()
		jsmod = jsmod.replace('{your colors will go here}', colors.replace('\n', ' '))

	with open('overrides.css', 'r') as overridefile :
		overrides = overridefile.read()
		jsmod = jsmod.replace('{and overrides will be here}', overrides.replace('\n', ' '))

	return jsmod

def install() :
	global cssfile
		
	jsmod = createJavascript() + """
	if (window.addEventListener)
		window.addEventListener('load', darkMode, false);
	else if (window.attachEvent)
		window.attachEvent('onload', darkMode);
	else window.onload = darkMode;
	"""

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
	else :
		# load from save instead
		with open('ssb-interop-save.js', 'r') as slackjs :
			ssbinterop = slackjs.read()

	ssbinterop = ssbinterop + '\n\n\n' + jsmod

	with open(installDirectory, 'w') as slackjs :
		slackjs.write(ssbinterop)

	print('done. please restart slack.')


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


if __name__ == '__main__' :
	method = 'install'
	global cssfile
	global sensitivity
	cssfile = 'colors.css'
	sensitivity = 50
	for i in range(len(sys.argv)) :
		if sys.argv[i].startswith('uninst') :
			method = 'uninstall'
			print('sorry you don\'t like darkmode, you can customize the colors in colors.css.\nfor now, please restart slack.')
		elif sys.argv[i].startswith('print') :
			method = 'createJavascript'
		elif sys.argv[i].startswith('css') :
			cssfile = sys.argv[i+1]
		elif sys.argv[i].startswith('sens') :
			sensitivity = int(sys.argv[i+1])

	getattr(sys.modules[__name__], method)()
