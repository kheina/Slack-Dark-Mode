# Modify this to change your theme colors
# (will be able to be loaded from a file later)
colors = """
:root {
	--primary: #2676D5;
	--text: #EEE;
	--text-subtle: #5D636A;
	--background: #111;
	--background-hover: #222;
	--background-elevated: #2D333A;

	--online: #00ff00;



	--background-light: #AAA;
	--background-bright: #FFF;

	--border-dim: #666;
	--border-bright: var(--primary);

	--text-bright: #FFF;
	--text-special: var(--primary);

	--scrollbar-background: #000;
	--scrollbar-border: var(--primary);
}
"""

jsmod = """{
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
		{'rgb(255, 255, 255)': 'var(--background)'},
		{'rgb(97, 96, 97)': 'var(--text-subtle)'},
		{'rgb(221, 221, 221)': 'var(--border-dim)'},
		{'rgb(29, 28, 29)': 'var(--text)'},
		{'rgb(58, 163, 227)': 'var(--primary)'},
		{'rgb(18, 100, 163)': 'var(--primary)'},
		{'rgb(134, 134, 134)': 'var(--text-subtle)'},
		{'rgb(29, 155, 209)': 'var(--primary)'},
		{'rgb(248, 248, 248)': 'var(--background-hover)'},
		{'rgba(0, 0, 0, 0)': 'transparent'},
		{'rgba(29, 28, 29, 0.7)': 'var(--text-subtle)'},
		{'rgb(0, 122, 90)': 'var(--online)'},
		{'rgb(224, 30, 90)': 'magenta'},
		{'rgba(0, 0, 0, 0.1)': 'var(--background-light)'},
		{'rgba(29, 155, 209, 0.3)': 'var(--primary)'},
		{'rgb(11, 76, 140)': 'var(--primary)'}
	];

	for (i = 0; i < replacements.length; i++)
	{
		regex = new RegExp(Object.keys(replacements[i])[0].replace('(','\\\\(').replace(')','\\\\)'), 'g');
		allcss = allcss.replace(regex, Object.values(replacements[i])[0]);
	}

	allcss = '{your colors will go here}' + allcss

	$('<style></style>').appendTo('head').html(allcss);
}"""

jsmod = jsmod.replace('{your colors will go here}', colors.replace('\n', ' '))

print(jsmod)