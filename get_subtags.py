#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import string, re, urllib

# NOTE: Not all information available in the IANA registry is present
#       in the LangTag.net text files used to generate these lists.
#
#       Even some of the information that *is* present in the
#       LangTag.net text files is not used in the generated output files.

def parseRegistry():
	registryFile = urllib.urlopen( 'http://www.iana.org/assignments/language-subtag-registry' )
	registryFileString = registryFile.read()

	ALPHA = '[A-Za-z]'
	DIGIT = '[0-9]'
	CRLF = r"\n" # "\r\n"
	field_name = '((?:' + ALPHA + '|' + DIGIT + ')(?:(?:' + ALPHA + '|' + DIGIT + '|-)*(?:' + ALPHA + '|' + DIGIT + '))?)'
	field_sep = ' *: *'
	field_body = '(.*?(?:' + CRLF + '^\s+.*?)*)' #'(((( ' + CRLF + ')? +)?.+?)*)'
	field = '(?:' + field_name + field_sep + field_body + ')'# + CRLF + ')'
	record = '(?:^' + field + '$)+' + "\n"

	tags = []

	for fullRecord in registryFileString.split( "%%\n" ):
		add_tag = {}

		# NOTE: This regular expression doesn't strictly match the ABNF notation in BCP 47
		recordResults = re.findall( record, fullRecord, re.M )

		for fullField in recordResults:
			fullField = ( fullField[0], ' '.join( fullField[1].split( "\n  " ) ) )

			if( fullField[0] in ['Description', 'Comments', 'Prefix'] ):
				if( fullField[0] not in add_tag ):
					add_tag[fullField[0]] = []

				add_tag[fullField[0]].append( fullField[1] )
			else:
				add_tag[fullField[0]] = fullField[1]

		if( 'File-Date' not in add_tag ):
			if( ( 'Type' not in add_tag ) or ( ( 'Subtag' not in add_tag ) and ( 'Tag' not in add_tag ) ) or ( 'Description' not in add_tag ) or ( 'Added' not in add_tag ) ):
				print 'ERROR: BAD ENTRY'
				print add_tag
				continue

		tags.append( add_tag )

#	print tags
#	print record

	file_date = '1995-03-01'

	languageFile = open( 'language.txt', 'w+' )
	extlangFile = open( 'extlang.txt', 'w+' )
	scriptFile = open( 'script.txt', 'w+' )
	regionFile = open( 'region.txt', 'w+' )
	variantFile = open( 'variant.txt', 'w+' )
	grandfatheredFile = open( 'grandfathered.txt', 'w+' )

	for tag in tags:
		# Just the date of the file
		if( 'File-Date' in tag ):
			file_date = tag['File-Date']
			languageFile.write( file_date + "\n" )
			extlangFile.write( file_date + "\n" )
			scriptFile.write( file_date + "\n" )
			regionFile.write( file_date + "\n" )
			variantFile.write( file_date + "\n" )
			continue
		# Grandfathered or redundant tag
		elif( 'Tag' in tag ):
			if( tag['Type'] == 'redundant' ):
				# We don't care about redundant tags
				continue
			# TODO: Handle grandfathered tags
			pass
		# Regular tag
		elif( 'Subtag' in tag ):
			line = tag['Subtag'] + "\t" + tag['Added'] + "\t" + ' / '.join( tag['Description'] )

			if( tag['Type'] in ['extlang', 'variant'] ):
				line += "\t"
				if( 'Prefix' in tag ):
					line += ' / '.join( tag['Prefix'] )

			if( tag['Type'] in ['language', 'extlang'] ):
				line += "\t"
				if( 'Suppress-Script' in tag ):
					line += tag['Suppress-Script']

				line += "\t"
				if( 'Scope' in tag ):
					line += tag['Scope']

				line += "\t"
				if( 'Macrolanguage' in tag ):
					line += tag['Macrolanguage']

			line += "\t"
			if( 'Deprecated' in tag ):
				line += tag['Deprecated']

			line += "\t"
			if( 'Preferred-Value' in tag ):
				line += tag['Preferred-Value']

			line += "\t"
			if( 'Comments' in tag ):
				line += '# ' + ' / '.join( tag['Comments'] )

			line += "\n"

			if( tag['Type'] == 'language' ):
				languageFile.write( line )
			elif( tag['Type'] == 'extlang' ):
				extlangFile.write( line )
			elif( tag['Type'] == 'script' ):
				scriptFile.write( line )
			elif( tag['Type'] == 'region' ):
				regionFile.write( line )
			elif( tag['Type'] == 'variant' ):
				variantFile.write( line )

	print 'Registry:', file_date

	languageFile.close()
	extlangFile.close()
	scriptFile.close()
	regionFile.close()
	variantFile.close()
	grandfatheredFile.close()

def getLanguageSubtags():
	langNames = open( 'languageNames.properties', 'w+' )
#	languages = urllib.urlopen( 'http://www.langtag.net/registries/lsr-language-utf8.txt' )
	languages = open( 'language.txt', 'r' )

	langNames.write( "#\n" )
	langNames.write( '# Language names from IANA Language Subtag Registry' + "\n" )
	langNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	langNames.write( "#\n" )
	langNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	langNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	langNames.write( "#\n" )
	langNames.write( '# Names can be overridden in the generating script.' + "\n" )
	langNames.write( "#\n" )

	override_choice = {
		'cu':	1,
		'dv':	1,
		'ht':	1,
		'ny':	2,
		'pa':	1,
		'ps':	1,
	}

	override_rename = {
		'el':	'Greek',
		'ia':	'Interlingua',
		'km':	'Khmer',
		'oc':	'Occitan',
	}

	for language in languages.readlines():
		# Values are separated by a tab
		line_split = re.split( "\t", string.rstrip( language, "\n" ) )

		# This is the date of the file
		if( len( line_split ) == 1 ):
			file_date = line_split[0].strip()
			print 'language:', file_date
			continue

		subtag = line_split[0]
		added_date = line_split[1]
		name = line_split[2]
		suppress_script = line_split[3]
		scope = line_split[4]
		macrolanguage = line_split[5]
		deprecated_date = line_split[6]
		preferred_value = line_split[7]
		comments = line_split[8]

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection by choice
		if( subtag in override_choice ):
			single_name = names[override_choice[subtag]]

		# Override name selection by renaming
		if( subtag in override_rename ):
			single_name = override_rename[subtag]

		if( single_name != name ):
			langNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			langNames.write( '# [Default Overridden]' + "\n" );

		langNames.write( subtag + ' = ' + single_name + "\n" )

#		if( suppress_script ):
#			print subtag + ' (' + suppress_script + ')' + "\t" + single_name
#		else:
#			print subtag + "\t\t" + single_name

	langNames.write( "#\n" )
	langNames.write( '# Registry: ' + file_date + "\n" )
	langNames.write( "#\n" )

	langNames.close()

def getScriptSubtags():
	scriptNames = open( 'scriptNames.properties', 'w+' )
#	scripts = urllib.urlopen( 'http://www.langtag.net/registries/lsr-script-utf8.txt' )
	scripts = open( 'script.txt', 'r' )

	scriptNames.write( "#\n" )
	scriptNames.write( '# Script names from IANA Language Subtag Registry' + "\n" )
	scriptNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	scriptNames.write( "#\n" )
	scriptNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	scriptNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	scriptNames.write( "#\n" )
	scriptNames.write( '# Names can be overridden in the generating script.' + "\n" )
	scriptNames.write( "#\n" )

	override_choice = {
	}

	override_rename = {
	}

	for script in scripts.readlines():
		# Values are separated by a tab
		line_split = re.split( "\t", string.rstrip( script, "\n" ) )

		# This is the date of the file
		if( len( line_split ) == 1 ):
			file_date = line_split[0].strip()
			print 'script:', file_date
			continue

		subtag = line_split[0]
		added_date = line_split[1]
		name = line_split[2]
		deprecated_date = line_split[3]
		preferred_value = line_split[4]
		comments = line_split[5]

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection by choice
		if( subtag in override_choice ):
			single_name = names[override_choice[subtag]]

		# Override name selection by renaming
		if( subtag in override_rename ):
			single_name = override_rename[subtag]

		if( single_name != name ):
			scriptNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			scriptNames.write( '# [Default Overridden]' + "\n" );

		scriptNames.write( subtag + ' = ' + single_name + "\n" )

#		print subtag + "\t\t" + single_name

	scriptNames.write( "#\n" )
	scriptNames.write( '# Registry: ' + file_date + "\n" )
	scriptNames.write( "#\n" )

	scriptNames.close()

def getRegionSubtags():
	regionNames = open( 'regionNames.properties', 'w+' )
#	regions = urllib.urlopen( 'http://www.langtag.net/registries/lsr-region-utf8.txt' )
	regions = open( 'region.txt', 'r' )

	regionNames.write( "#\n" )
	regionNames.write( '# Region names from IANA Language Subtag Registry' + "\n" )
	regionNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	regionNames.write( "#\n" )
	regionNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	regionNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	regionNames.write( "#\n" )
	regionNames.write( '# Names can be overridden in the generating script.' + "\n" )
	regionNames.write( "#\n" )

	override_choice = {
	}

	override_rename = {
	}

	for region in regions.readlines():
		# Values are separated by a tab
		line_split = re.split( "\t", string.rstrip( region, "\n" ) )

		# This is the date of the file
		if( len( line_split ) == 1 ):
			file_date = line_split[0].strip()
			print 'region:', file_date
			continue

		subtag = line_split[0]
		added_date = line_split[1]
		name = line_split[2]
		deprecated_date = line_split[3]
		preferred_value = line_split[4]
		comments = line_split[5]

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection by choice
		if( subtag in override_choice ):
			single_name = names[override_choice[subtag]]

		# Override name selection by renaming
		if( subtag in override_rename ):
			single_name = override_rename[subtag]

		if( single_name != name ):
			regionNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			regionNames.write( '# [Default Overridden]' + "\n" );

		regionNames.write( subtag + ' = ' + single_name + "\n" )

#		print subtag + "\t\t" + single_name

	regionNames.write( "#\n" )
	regionNames.write( '# Registry: ' + file_date + "\n" )
	regionNames.write( "#\n" )

	regionNames.close()

def getVariantSubtags():
	variantNames = open( 'variantNames.properties', 'w+' )
#	variants = urllib.urlopen( 'http://www.langtag.net/registries/lsr-variant-utf8.txt' )
	variants = open( 'variant.txt', 'r' )

	variantNames.write( "#\n" )
	variantNames.write( '# Variant names from IANA Language Subtag Registry' + "\n" )
	variantNames.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	variantNames.write( "#\n" )
	variantNames.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
	variantNames.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
	variantNames.write( "#\n" )
	variantNames.write( '# Names can be overridden in the generating script.' + "\n" )
	variantNames.write( "#\n" )

	override_choice = {
	}

	override_rename = {
	}

	for variant in variants.readlines():
		# Values are separated by a tab
		line_split = re.split( "\t", string.rstrip( variant, "\n" ) )

		# This is the date of the file
		if( len( line_split ) == 1 ):
			file_date = line_split[0].strip()
			print 'variant:', file_date
			continue

		subtag = line_split[0]
		added_date = line_split[1]
		name = line_split[2]
		prefix = line_split[3]
		deprecated_date = line_split[4]
		preferred_value = line_split[5]
		comments = line_split[6]

		# Multiple names for a given subtag are separated by a slash
		# For simplicity, arbitrarily choose the first one
		names = re.split( ' / ', name )
		single_name = names[0]

		# Override name selection by choice
		if( subtag in override_choice ):
			single_name = names[override_choice[subtag]]

		# Override name selection by renaming
		if( subtag in override_rename ):
			single_name = override_rename[subtag]

		if( single_name != name ):
			variantNames.write( '# ' + name + "\n" );

		if( single_name != names[0] ):
			variantNames.write( '# [Default Overridden]' + "\n" );

		variantNames.write( subtag + ' = ' + single_name + "\n" )

#		if( prefix ):
#			print subtag + ' (' + prefix + ')' + "\t" + single_name
#		else:
#			print subtag + "\t\t" + single_name

	variantNames.write( "#\n" )
	variantNames.write( '# Registry: ' + file_date + "\n" )
	variantNames.write( "#\n" )

	variantNames.close()

def main():
	parseRegistry()
	getLanguageSubtags()
	getScriptSubtags()
	getRegionSubtags()
	getVariantSubtags()

main()
