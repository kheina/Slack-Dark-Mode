import subprocess
import sys
import os

installFolders = ['/Applications/Slack.app', 'C:/Users/User/AppData/Local/slack']

def find(name, path) :
	for root, dirs, files in os.walk(path):
		if name in files:
			return os.path.join(root, name)

def createJavascript(customcss='colors.css') :
	# Modify colors.css to change your theme colors
	colors = ''
	with open(customcss, 'r') as colorfile :
		colors = colorfile.read()
	replacements = ''
	with open('replacements.json', 'r') as replacementsfile :
		replacements = replacementsfile.read()

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
		for (let k = 0; k < color1.length; k++)
		{ distance += (color1[k] - color2[k]) * (color1[k] - color2[k]); }
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
		return lowest < 50 ? Object.keys(replacements[index])[0] : false;
	}
	function darkMode()
	{
		let allcss = 'textarea { color: var(--text) !important; }';
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

		allcss = '{your colors will go here}' + '\\n' + allcss;

		$('<style></style>').appendTo('head').html(allcss);
	}
	"""

	jsmod = jsmod.replace('{your colors will go here}', colors.replace('\n', ' '))
	jsmod = jsmod.replace('{replacements.json will be added here}', replacements.replace('\n', ' '))

	return jsmod

def install() :
	csspath = 'colors.css'
	if os.path.isfile('custom/colors.css') :
		csspath = 'custom/colors.css'
		
	jsmod = createJavascript(customcss=csspath) + """
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
	if len(sys.argv) > 1 :
		if sys.argv[1].startswith('uninst') :
			uninstall()
			print('sorry you don\'t like darkmode, you can customize the colors in colors.css.\nfor now, please restart slack.')
		elif sys.argv[1].startswith('reinst') :
			uninstall()
			install()
		elif sys.argv[1].startswith('print') :
			print(createJavascript())
			print('darkMode()')
	elif len(sys.argv) > 2 :
		if sys.argv[1].startswith('css') :
			cssfile = sys.argv[2]
	else : install()
