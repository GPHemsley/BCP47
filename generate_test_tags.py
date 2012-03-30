#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

language_subtags = [ 'en', 'qaz' ]
script_subtags = [ '', '-Cyrl', '-Qaaz' ]
region_subtags = [ '', '-US', '-QZ' ]
variant_subtags = [ '', '-fonipa', '-qxqaaaaz' ]

test_tags = open( 'test_tags.txt', 'w+' )

for language in language_subtags:
	for script in script_subtags:
		for region in region_subtags:
			for variant in variant_subtags:
				test_tag = language + script + region + variant
				test_tags.write( test_tag + "\n" )
				print test_tag

test_tags.close()