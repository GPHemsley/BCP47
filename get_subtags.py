#!/usr/local/bin/python

import string, re, urllib

# NOTE: Not all information available in the IANA registry is present
#       in the LangTag.net text files used to generate these lists.
#
#       Even some of the information that *is* present in the
#       LangTag.net text files is not used in the generated output files.

def getLanguageSubtags():
	langNames = open( 'languageNames.properties', 'w+' )
	languages = urllib.urlopen( 'http://www.langtag.net/registries/lsr-language-utf8.txt' )

	langNames.write( "#\n" )
	langNames.write( '# Language names from IANA Language Subtag Registry' + "\n" )
	langNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	langNames.write( "#\n" )
	langNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	langNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	langNames.write( "#\n" )
	langNames.write( '# Names can be overridden in the generating script.' + "\n" )
	langNames.write( "#\n" )

	most_recent_date = '1995-03-01'

	overrides = {"el":"Greek","ia":"Interlingua","km":"Khmer","ms":"Malay","oc":"Occitan","sw":"Swahili"}

	for language in languages.readlines():
		# Values are separated by a tab
		line_split = re.split( '\t', string.rstrip( language ) )

		subtag = date = name = suppress_script = scope = ''

		if( len( line_split ) == 5 ):
			# Language has Suppress-Script and Scope value specified
			subtag, date, name, suppress_script, scope = line_split
		elif( len( line_split ) == 4 ):
			# Language has a Suppress-Script value specified
			subtag, date, name, suppress_script = line_split
		elif( len( line_split ) == 3 ):
			# No Suppress-Script value
			subtag, date, name = line_split
		else:
			continue

		if( date > most_recent_date ):
			most_recent_date = date

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection
		if( subtag == 'dv' ):
			single_name = names[1]
		elif( subtag == 'ht' ):
			single_name = names[1]
		elif( subtag == 'ny' ):
			single_name = names[2]
		elif( subtag == 'pa' ):
			single_name = names[1]
		elif( subtag == 'ps' ):
			single_name = names[1]
#		elif( subtag == 'xx' ):
#			single_name = names[2]
#		elif( subtag == 'qq' ):
#			single_name = 'not in the list'

		if (subtag in overrides):
			single_name = overrides[subtag]

		if( single_name != name ):
			langNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			langNames.write( '# [Default Overridden]' + "\n" );

		langNames.write( subtag + ' = ' + single_name + "\n" )

		if( suppress_script ):
			print subtag + ' (' + suppress_script + ')' + "\t" + single_name
		else:
			print subtag + "\t\t" + single_name

	langNames.write( "#\n" )
	langNames.write( '# Current as of: ' + most_recent_date + "\n" )
	langNames.write( "#\n" )

	langNames.close()

def getScriptSubtags():
	scriptNames = open( 'scriptNames.properties', 'w+' )
	scripts = urllib.urlopen( 'http://www.langtag.net/registries/lsr-script-utf8.txt' )

	scriptNames.write( "#\n" )
	scriptNames.write( '# Script names from IANA Language Subtag Registry' + "\n" )
	scriptNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	scriptNames.write( "#\n" )
	scriptNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	scriptNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	scriptNames.write( "#\n" )
	scriptNames.write( '# Names can be overridden in the generating script.' + "\n" )
	scriptNames.write( "#\n" )

	most_recent_date = '1995-03-01'

	for script in scripts.readlines():
		# Values are separated by a tab
		line_split = re.split( '\t', string.rstrip( script ) )

		subtag = date = name = ''

		if( len( line_split ) == 3 ):
			subtag, date, name = line_split
		else:
			continue

		if( date > most_recent_date ):
			most_recent_date = date

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection
#		if( subtag == 'xx' ):
#			single_name = names[2]
#		elif( subtag == 'qq' ):
#			single_name = 'not in the list'

		if( single_name != name ):
			scriptNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			scriptNames.write( '# [Default Overridden]' + "\n" );

		scriptNames.write( subtag + ' = ' + single_name + "\n" )

		print subtag + "\t\t" + single_name

	scriptNames.write( "#\n" )
	scriptNames.write( '# Current as of: ' + most_recent_date + "\n" )
	scriptNames.write( "#\n" )

	scriptNames.close()

def getRegionSubtags():
	regionNames = open( 'regionNames.properties', 'w+' )
	regions = urllib.urlopen( 'http://www.langtag.net/registries/lsr-region-utf8.txt' )

	regionNames.write( "#\n" )
	regionNames.write( '# Region names from IANA Language Subtag Registry' + "\n" )
	regionNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	regionNames.write( "#\n" )
	regionNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	regionNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	regionNames.write( "#\n" )
	regionNames.write( '# Names can be overridden in the generating script.' + "\n" )
	regionNames.write( "#\n" )

	most_recent_date = '1995-03-01'

	for region in regions.readlines():
		# Values are separated by a tab
		line_split = re.split( '\t', string.rstrip( region ) )

		subtag = date = name = ''

		if( len( line_split ) == 3 ):
			subtag, date, name = line_split
		else:
			continue

		if( date > most_recent_date ):
			most_recent_date = date

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection
#		if( subtag == 'xx' ):
#			single_name = names[2]
#		elif( subtag == 'qq' ):
#			single_name = 'not in the list'

		if( single_name != name ):
			regionNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			regionNames.write( '# [Default Overridden]' + "\n" );

		regionNames.write( subtag + ' = ' + single_name + "\n" )

		print subtag + "\t\t" + single_name

	regionNames.write( "#\n" )
	regionNames.write( '# Current as of: ' + most_recent_date + "\n" )
	regionNames.write( "#\n" )

	regionNames.close()

def getVariantSubtags():
	variantNames = open( 'variantNames.properties', 'w+' )
	variants = urllib.urlopen( 'http://www.langtag.net/registries/lsr-variant-utf8.txt' )

	variantNames.write( "#\n" )
	variantNames.write( '# Variant names from IANA Language Subtag Registry' + "\n" )
	variantNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	variantNames.write( "#\n" )
	variantNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	variantNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	variantNames.write( "#\n" )
	variantNames.write( '# Names can be overridden in the generating script.' + "\n" )
	variantNames.write( "#\n" )

	most_recent_date = '1995-03-01'

	for variant in variants.readlines():
		# Values are separated by a tab
		line_split = re.split( '\t', string.rstrip( variant ) )

		subtag = date = name = prefix = ''

		if( len( line_split ) == 4 ):
			# Variant has a Prefix value specified
			subtag, date, name, prefix = line_split
		elif( len( line_split ) == 3 ):
			# No Prefix value
			subtag, date, name = line_split
		else:
			continue

		if( date > most_recent_date ):
			most_recent_date = date

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection
#		if( subtag == 'xx' ):
#			single_name = names[2]
#		elif( subtag == 'qq' ):
#			single_name = 'not in the list'

		if( single_name != name ):
			variantNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			variantNames.write( '# [Default Overridden]' + "\n" );

		variantNames.write( subtag + ' = ' + single_name + "\n" )

		if( prefix ):
			print subtag + ' (' + prefix + ')' + "\t" + single_name
		else:
			print subtag + "\t\t" + single_name

	variantNames.write( "#\n" )
	variantNames.write( '# Current as of: ' + most_recent_date + "\n" )
	variantNames.write( "#\n" )

	variantNames.close()

def main():
	getLanguageSubtags()
	getScriptSubtags()
	getRegionSubtags()
	getVariantSubtags()

main()
