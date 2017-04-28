#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is a parser of the IANA Language Subtag Registry.
#
# The Initial Developer of the Original Code is
# Gordon P. Hemsley <me@gphemsley.org>.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Gordon P. Hemsley <me@gphemsley.org>
#   Kevin Scannell <ksanne@gmail.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import string, re, urllib

lineFormat = "^([A-Za-z0-9]{2,8}(?:\.\.[A-Za-z0-9]{2,8})?|(?:en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon|i-lux|i-mingo|i-navajo|i-pwn|i-tao|i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE|art-lojban|cel-gaulish|no-bok|no-nyn|zh-guoyu|zh-hakka|zh-min|zh-min-nan|zh-xiang))\t(\d{4}-\d{2}-\d{2})\t(.*?)(?:\t([A-Za-z0-9 /-]+)?)?(?:\t([A-Za-z]{4})?\t(macrolanguage|collection|special|private-use)?\t([A-Za-z]{2,3})?)?\t(\d{4}-\d{2}-\d{2})?\t([A-Za-z0-9-]+)?\t(# .*)?$"

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

	languageFile = open( 'raw/language.txt', 'w+' )
	extlangFile = open( 'raw/extlang.txt', 'w+' )
	scriptFile = open( 'raw/script.txt', 'w+' )
	regionFile = open( 'raw/region.txt', 'w+' )
	variantFile = open( 'raw/variant.txt', 'w+' )
	grandfatheredFile = open( 'raw/grandfathered.txt', 'w+' )

	for tag in tags:
		# Just the date of the file
		if( 'File-Date' in tag ):
			file_date = tag['File-Date']
			languageFile.write( file_date + "\n" )
			extlangFile.write( file_date + "\n" )
			scriptFile.write( file_date + "\n" )
			regionFile.write( file_date + "\n" )
			variantFile.write( file_date + "\n" )
			grandfatheredFile.write( file_date + "\n" )
		# Redundant tag
		elif tag['Type'] == 'redundant':
			# We don't care about redundant tags
			continue
		# Regular tag
		else:
			line = tag['Tag'] if 'Tag' in tag else tag['Subtag']
			line += "\t" + tag['Added'] + "\t" + ' / '.join( tag['Description'] )

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
			elif( tag['Type'] == 'grandfathered' ):
				grandfatheredFile.write( line )

	print 'Registry:', file_date

	languageFile.close()
	extlangFile.close()
	scriptFile.close()
	regionFile.close()
	variantFile.close()
	grandfatheredFile.close()

def getSubtagNames():
	global lineFormat

	subtagTypes = [ 'language', 'extlang', 'script', 'region', 'variant', 'grandfathered' ]

	override_choice = {
		'language':	{
			'cu':	1,
			'dv':	1,
			'ht':	1,
			'ny':	2,
			'pa':	1,
			'ps':	1,
			'ug':	1,
		},
		'extlang':	{

		},
		'script':	{

		},
		'region':	{

		},
		'variant':	{

		},
		'grandfathered':	{

		},
	}

	override_rename = {
		'language':	{
			'el':	'Greek',
			'ia':	'Interlingua',
			'km':	'Khmer',
			'oc':	'Occitan',
			'lez':	'Lezgian',
		},
		'extlang':	{

		},
		'script':	{

		},
		'region':	{
			'CD':	'Congo-Kinshasa',
			'CG':	'Congo-Brazzaville',
#			'CI':	'Ivory Coast',			# The French name is the preferred name now
#			'FM':	'Micronesia',			# The extended name is the preferred name for the nation
			'IR':	'Iran',
			'KP':	'North Korea',
			'KR':	'South Korea',
			'LA':	'Laos',
			'MF':	'Saint-Martin',			# French part
			'MK':	'Macedonia, f.Y.R. of',	# The lowercase 'f' is the preferred abbreviation for 'former'
			'SX':	'Sint Maarten',			# Dutch part
			'SY':	'Syria',
			'TW':	'Taiwan',
			'TZ':	'Tanzania',
			'VA':	'Vatican City',
			'VN':	'Vietnam',
		},
		'variant':	{

		},
		'grandfathered':	{

		},
	}

	for subtagType in subtagTypes:
		sourceFile = open( 'raw/' + subtagType + '.txt', 'r' )
		targetFile = open( 'properties/full/' + subtagType + 'Names.properties', 'w+' )

		targetFile.write( "#\n" )
		targetFile.write( '# ' + subtagType.capitalize() + ' names from IANA Language Subtag Registry' + "\n" )
		targetFile.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
		targetFile.write( "#\n" )
		targetFile.write( '# If a subtag has multiple names associated with it, the first one is chosen' + "\n" )
		targetFile.write( '# by default and the full list is written in a comment above the definition.' + "\n" )
		targetFile.write( "#\n" )
		targetFile.write( '# Names can be overridden in the generating script.' + "\n" )
		targetFile.write( "#\n" )

		file_date = '1995-03-01'
		previous_footnotes = False

		for sourceLine in sourceFile.readlines():
			date_line = re.search( '^(\d{4}-\d{2}-\d{2})$', string.strip( sourceLine ) )
			if( date_line ):
				file_date = date_line.group( 1 )

				targetFile.write( '# Registry Version: ' + file_date + "\n" )
				targetFile.write( "#\n" )

				print subtagType + ':', file_date
				continue

			line_split = re.search( lineFormat, string.rstrip( sourceLine, "\n" ) )

			# If something is broken, announce it.
			if( line_split == None ):
				print sourceLine
				continue

			subtag = line_split.group( 1 )
			added_date = line_split.group( 2 )
			name = line_split.group( 3 )
			prefix = line_split.group( 4 )
			suppress_script = line_split.group( 5 )
			scope = line_split.group( 6 )
			macrolanguage = line_split.group( 7 )
			deprecated_date = line_split.group( 8 )
			preferred_value = line_split.group( 9 )
			comments = line_split.group( 10 )

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

			footnotes = ''

			if( single_name != name ):
				footnotes += '# ' + name + "\n"

			if( single_name != names[0] ):
				footnotes += '# [Default Overridden]' + "\n"

			if( deprecated_date ):
				footnotes += '# Deprecated: ' + deprecated_date + "\n"

			if( preferred_value ):
				footnotes += '# Preferred-Value: ' + preferred_value + "\n"

			if( comments ):
				footnotes += comments + "\n"

			if( prefix ):
				footnotes += '# Prefix: ' + prefix + "\n"

			if( scope ):
				footnotes += '# Scope: ' + scope + "\n"

			if( macrolanguage ):
				footnotes += '# Macrolanguage: ' + macrolanguage + "\n"

			if( footnotes ):
				if( not previous_footnotes ):
					targetFile.write( "\n" )
				targetFile.write( footnotes )

			targetFile.write( subtag + ' = ' + single_name + "\n" )

			if( footnotes ):
				targetFile.write( "\n" )
				previous_footnotes = True
			else:
				previous_footnotes = False

		targetFile.close()

def getSuppressScripts():
	global lineFormat

	sourceFile = open( 'raw/language.txt', 'r' )
	targetFile = open( 'properties/full/scriptSuppress.properties', 'w+' )

	targetFile.write( "#\n" )
	targetFile.write( '# Suppress-Script values from IANA Language Subtag Registry' + "\n" )
	targetFile.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
	targetFile.write( "#\n" )

	file_date = '1995-03-01'

	for sourceLine in sourceFile.readlines():
		date_line = re.search( '^(\d{4}-\d{2}-\d{2})$', string.strip( sourceLine ) )
		if( date_line ):
			file_date = date_line.group( 1 )

			targetFile.write( '# Registry Version: ' + file_date + "\n" )
			targetFile.write( "#\n" )

			print 'Suppress-Script:', file_date
			continue

		line_split = re.search( lineFormat, string.rstrip( sourceLine, "\n" ) )

		# If something is broken, announce it.
		if( line_split == None ):
			print sourceLine
			continue

		subtag = line_split.group( 1 )
		added_date = line_split.group( 2 )
		name = line_split.group( 3 )
		prefix = line_split.group( 4 )
		suppress_script = line_split.group( 5 )
		scope = line_split.group( 6 )
		macrolanguage = line_split.group( 7 )
		deprecated_date = line_split.group( 8 )
		preferred_value = line_split.group( 9 )
		comments = line_split.group( 10 )

		if( suppress_script ):
			targetFile.write( subtag + ' = ' + suppress_script + "\n" )

	targetFile.close()

def getDeprecatedSubtags():
	global lineFormat

	subtagTypes = [ 'language', 'extlang', 'script', 'region', 'variant', 'grandfathered' ]

	for subtagType in subtagTypes:
		sourceFile = open( 'raw/' + subtagType + '.txt', 'r' )
		targetFile = open( 'properties/full/' + subtagType + 'Deprecated.properties', 'w+' )

		targetFile.write( "#\n" )
		targetFile.write( '# Deprecated ' + subtagType + ' values from IANA Language Subtag Registry' + "\n" )
		targetFile.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
		targetFile.write( "#\n" )

		file_date = '1995-03-01'

		for sourceLine in sourceFile.readlines():
			date_line = re.search( '^(\d{4}-\d{2}-\d{2})$', string.strip( sourceLine ) )
			if( date_line ):
				file_date = date_line.group( 1 )

				targetFile.write( '# Registry Version: ' + file_date + "\n" )
				targetFile.write( "#\n" )

				print 'Deprecated ' + subtagType + ':', file_date
				continue

			line_split = re.search( lineFormat, string.rstrip( sourceLine, "\n" ) )

			# If something is broken, announce it.
			if( line_split == None ):
				print sourceLine
				continue

			subtag = line_split.group( 1 )
			added_date = line_split.group( 2 )
			name = line_split.group( 3 )
			prefix = line_split.group( 4 )
			suppress_script = line_split.group( 5 )
			scope = line_split.group( 6 )
			macrolanguage = line_split.group( 7 )
			deprecated_date = line_split.group( 8 )
			preferred_value = line_split.group( 9 )
			comments = line_split.group( 10 )

			if( deprecated_date ):
				targetFile.write( "\n" )

				targetFile.write( '# ' + name + "\n" )
				targetFile.write( '# Deprecated: ' + deprecated_date + "\n" )

				if( comments ):
					targetFile.write( comments + "\n" )

				if( preferred_value ):
					targetFile.write( subtag + ' = ' + preferred_value + "\n" )
				else:
#					targetFile.write( '# ' + subtag + "\n" )
					targetFile.write( subtag + "\n" )
			elif( preferred_value ):
				# Mostly limited to extlang
#				print subtag, deprecated_date, preferred_value, comments
				pass

		targetFile.close()

def getScopedSubtags():
	global lineFormat

	subtagTypes = ['language', 'extlang']

	for subtagType in subtagTypes:
		sourceFile = open( 'raw/' + subtagType + '.txt', 'r' )
		targetFile = open( 'properties/full/' + subtagType + 'Scope.properties', 'w+' )

		targetFile.write( "#\n" )
		targetFile.write( '# Scoped ' + subtagType + ' values from IANA Language Subtag Registry' + "\n" )
		targetFile.write( '# http://www.iana.org/assignments/language-subtag-registry' + "\n" )
		targetFile.write( "#\n" )

		file_date = '1995-03-01'

		for sourceLine in sourceFile.readlines():
			date_line = re.search( '^(\d{4}-\d{2}-\d{2})$', string.strip( sourceLine ) )
			if( date_line ):
				file_date = date_line.group( 1 )

				targetFile.write( '# Registry Version: ' + file_date + "\n" )
				targetFile.write( "#\n" )

				print 'Scoped ' + subtagType + ':', file_date
				continue

			line_split = re.search( lineFormat, string.rstrip( sourceLine, "\n" ) )

			# If something is broken, announce it.
			if( line_split == None ):
				print sourceLine
				continue

			subtag = line_split.group( 1 )
			added_date = line_split.group( 2 )
			name = line_split.group( 3 )
			prefix = line_split.group( 4 )
			suppress_script = line_split.group( 5 )
			scope = line_split.group( 6 )
			macrolanguage = line_split.group( 7 )
			deprecated_date = line_split.group( 8 )
			preferred_value = line_split.group( 9 )
			comments = line_split.group( 10 )

			if( scope ):
				targetFile.write( "\n" )

				targetFile.write( '# ' + name + "\n" )

				if( comments ):
					targetFile.write( comments + "\n" )

				if( preferred_value ):
					targetFile.write( '# Preferred-Value: ' + preferred_value + "\n" )

				targetFile.write( subtag + ' = ' + scope + "\n" )

		targetFile.close()

def main():
	parseRegistry()
	getSubtagNames()
	getSuppressScripts()
	getDeprecatedSubtags()
	getScopedSubtags()

main()
