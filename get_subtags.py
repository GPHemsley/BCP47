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

def getSubtagNames():

	subtagTypes = ['language', 'extlang', 'script', 'region', 'variant']

	override_choice = {
		'language':	{
			'cu':	1,
			'dv':	1,
			'ht':	1,
			'ny':	2,
			'pa':	1,
			'ps':	1,
		},
		'extlang':	{

		},
		'script':	{

		},
		'region':	{

		},
		'variant':	{

		},
	}

	override_rename = {
		'language':	{
			'el':	'Greek',
			'ia':	'Interlingua',
			'km':	'Khmer',
			'oc':	'Occitan',
		},
		'extlang':	{

		},
		'script':	{

		},
		'region':	{

		},
		'variant':	{

		},
	}

	for subtagType in subtagTypes:
		sourceFile = open( subtagType + '.txt', 'r' )
		targetFile = open( subtagType + 'Names.properties', 'w+' )

		targetFile.write( "#\n" )
		targetFile.write( '# ' + subtagType.capitalize() + ' names from IANA Language Subtag Registry' + "\n" )
		targetFile.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
		targetFile.write( "#\n" )
		targetFile.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
		targetFile.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
		targetFile.write( "#\n" )
		targetFile.write( '# Names can be overridden in the generating script.' + "\n" )
		targetFile.write( "#\n" )

		for sourceLine in sourceFile.readlines():
			# Values are separated by a tab
			line_split = re.split( "\t", string.rstrip( sourceLine, "\n" ) )

			# This is the date of the file
			if( len( line_split ) == 1 ):
				file_date = line_split[0].strip()
				print subtagType + ':', file_date
				continue

			# Common to all subtag types
			subtag = line_split[0]
			added_date = line_split[1]
			name = line_split[2]

			# NOTE: None of these variables ever come into play when selecting the subtag name.
			if( subtagType == 'language' ):
				suppress_script = line_split[3]
				scope = line_split[4]
				macrolanguage = line_split[5]
				deprecated_date = line_split[6]
				preferred_value = line_split[7]
				comments = line_split[8]
			elif( subtagType == 'extlang' ):
				prefix = line_split[3]
				suppress_script = line_split[4]
				scope = line_split[5]
				macrolanguage = line_split[6]
				deprecated_date = line_split[7]
				preferred_value = line_split[8]
				comments = line_split[9]
			elif( subtagType in ['script', 'region'] ):
				deprecated_date = line_split[3]
				preferred_value = line_split[4]
				comments = line_split[5]
			elif( subtagType == 'variant' ):
				prefix = line_split[3]
				deprecated_date = line_split[4]
				preferred_value = line_split[5]
				comments = line_split[6]

			# Multiple names for a given subtag are separated by a slash
			# For simplicity, arbitrarily choose the first one
			names = re.split( ' / ', name )
			single_name = names[0]

			# Override name selection by choice
			if( subtag in override_choice[subtagType] ):
				single_name = names[override_choice[subtagType][subtag]]

			# Override name selection by renaming
			if( subtag in override_rename[subtagType] ):
				single_name = override_rename[subtagType][subtag]

			if( single_name != name ):
				targetFile.write( '# ' + name + "\n" );

			if( single_name != names[0] ):
				targetFile.write( '# [Default Overridden]' + "\n" );

			targetFile.write( subtag + ' = ' + single_name + "\n" )

		targetFile.write( "#\n" )
		targetFile.write( '# Registry: ' + file_date + "\n" )
		targetFile.write( "#\n" )

		targetFile.close()

def main():
	parseRegistry()
	getSubtagNames()

main()
