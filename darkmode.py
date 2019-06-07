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
	replacements = [
		{"var(--background)": [255, 255, 255, 1]},
		{"var(--text-subtle)": [97, 96, 97, 1]},
		{"var(--border-dim)": [221, 221, 221, 1]},
		{"var(--text)": [29, 28, 29, 1]},
		{"var(--primary)": [58, 163, 227, 1]},
		{"var(--primary)": [18, 100, 163, 1]},
		{"var(--text-subtle)": [134, 134, 134, 1]},
		{"var(--primary)": [29, 155, 209, 1]},
		{"var(--background-hover)": [248, 248, 248, 1]},
		{"var(--text-subtle)": [29, 28, 29, 0.7]},
		{"var(--pressed)": [0, 122, 90, 1]},
		{"var(--text-code)": [224, 30, 90, 1]},
		{"var(--primary)": [29, 155, 209, 0.3]},
		{"var(--primary)": [11, 76, 140, 1]},
		{"var(--text-subtle)": [29, 28, 29, 0.13]},
		{"var(--private)": [232, 145, 45, 1]},
		{"var(--background-code)": [247, 247, 249, 1]},
		{"var(--background-elevated)": [29, 28, 29, 0.05]},
		{"var(--text-special-hover)": [232, 245, 250, 1]},
		{"var(--background-hover)": [0, 0, 0, 0.08]},
		{"var(--border-dim)": [0, 0, 0, 0.15]},
		{"var(--text-subtle)": [0, 0, 0, 0.5]},
		{"var(--background-light)": [0, 0, 0, 0.9]},
		{"var(--background-bright)": [0, 0, 0, 1]},
		{"var(--background)": [255, 255, 255, 0.95]},
		{"var(--background-code)": [34, 34, 34, 1]},
		{"var(--text-code)": [51, 51, 51, 1]},
		{"var(--online)": [147, 204, 147, 1]},
		{"var(--gold)": [242, 199, 68, 1]}
	];

	function convertColor(str)
	{
		color = [];
		colorstring = str.match(/[0-9\\.]{1,10}/g);
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
		lowest = 1000000;
		index = -1;
		for (m = 0; m < replacements.length; m++)
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
		allcss = '';
		regex = /rgb[\\\\(a]{1,2}/;
		for (s = 0; s < document.styleSheets.length; s++)
		{
			for (i = 0; i < document.styleSheets[s].cssRules.length; i++)
			{
				temprule = document.styleSheets[s].cssRules[i].cssText;
				if (regex.test(temprule) && temprule.indexOf('sidebar') < 0 && temprule.indexOf('channels_list') < 0 && temprule.indexOf('#team_menu') < 0)
				{
					colorstrings = temprule.match(/rgb[a]{0,1}\\([0-9\\., ]{7,}\\)/g);
					for (j = 0; j < colorstrings.length; j++)
					{
						replacement = findReplacement(convertColor(colorstrings[j]));
						if (replacement)
						{ temprule = temprule.replace(/rgb[a]{0,1}\\([0-9\\., ]{7,}\\)/, replacement); }
					}


					allcss = allcss + temprule + '\\n';
				}
			}
		}

		allcss = '{your colors will go here}' + allcss;

		$('<style></style>').appendTo('head').html(allcss);
	}
	"""

	return jsmod.replace('{your colors will go here}', colors.replace('\n', ' '))

def install() :
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
	query = False
	method = 'help'
	params = []
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
	else : install()
