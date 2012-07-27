
all: languageNames-l10n.properties scriptNames-l10n.properties regionNames-l10n.properties

# Get version of languageNames.properties before the overhaul
moz-current.txt: FORCE
	wget -O $@ 'http://hg.mozilla.org/mozilla-central/raw-file/444e087c6e27/toolkit/locales/en-US/chrome/global/languageNames.properties' 2> /dev/null
	sed -i'.bak' 's/ .*//' $@

# Stable URL on my site that lists language codes for which there is a
# FLOSS spell checker in existence (summarizing the more extensive
# http://borel.slu.edu/crubadan/stadas.html
moz-spell.txt: FORCE
	wget -O $@ 'http://borel.slu.edu/ispell/spell.txt' 2> /dev/null

# Get list of languages in which the Google search interface is available
moz-google.txt: FORCE
	wget -O google.html 'https://sites.google.com/site/tomihasa/google-language-codes' 2> /dev/null
	egrep -o '\?hl=[^&"]+' google.html | sed 's/^\?hl=//' | LC_ALL=C sort -u > $@
	rm -f google.html

# Get list of active wikipedias
moz-wiki.txt: FORCE
	wget -O wiki.html 'http://meta.wikimedia.org/wiki/List_of_Wikipedias' 2> /dev/null
	cat wiki.html | tr -d "\n" | sed 's/<tr>/~&/g' | tr '~' "\n" | egrep 'Special:Stat' | egrep '^<tr><td>[0-9]+</td>' | egrep -o '>[a-z][a-z-]+<' | sed 's/^>//; s/<$$//' | sort -u | egrep -v '^closed$$' > $@
	rm -f wiki.html

# get list of current Mozilla l10n teams (whoever is committed to l10n-central)
moz-teams.txt: FORCE
	wget -O l10n.html 'http://hg.mozilla.org/releases/l10n/mozilla-aurora/' 2> /dev/null
	egrep -o '/mozilla-aurora/[^/]+' l10n.html | sed 's/^\/mozilla-aurora\///' | egrep -v '^(static|x-testing)$$' | sort -u > $@
	rm -f l10n.html

# * Google adds some deprecated codes; iw, jw, sh (so be it)
# * Spelling adds some sublangs of macrolanguages (als, azj, plt, swh, etc.)
#   that coincide with existing spell checkers (in case they are relabelled)
#   and also some ISO 639-2/-5 codes (e.g. son, ber)
# * Teams currently adds "mai" only (also from spell checking though)
# * Wikipedia adds quite a few, but note many incorrect codes;
#   I'm filtering out incorrect als, nrm, and adding correct codes
#   where deprecated ones are used by WP - lzh, nan, etc.
languageNames-l10n.properties: moz-current.txt moz-google.txt moz-spell.txt moz-wiki.txt moz-teams.txt languageNames.properties
	(cat moz-current.txt; (cat moz-google.txt | egrep -v '^xx-'; cat moz-spell.txt moz-teams.txt; cat moz-wiki.txt | egrep -v '^(als|nrm|simple)$$'; echo "lzh nan rup sgs vro yue" | tr " " "\n") | sed 's/-.*//') | LC_ALL=C sort -u > cll-codes.txt

	# Exclude deprecated subtags
	printf '^(%s) = ' `cat languageDeprecated.properties | sed 's/^#.*//' | sed 's/ = .*//' | egrep '[a-z]' | tr "\n" '|' | sed 's/.$$//'` > dep-language-regexp.txt

	( cat languageNames.properties | egrep '^[a-z]{2,8} =' | LC_ALL=C sort -k1,1 | join - cll-codes.txt | sed '/^.. /s/^/@/' | LC_ALL=C sort -k1,1 | sed 's/^@//' ) | egrep -v -f dep-language-regexp.txt > $@

	# Remove parentheticals without 'sed -i'
	cat $@ | sed 's/^\([^ =]*\) *= *\(.*\)  *\((.*)\)$$/# \2 \3~\1 = \2/' | tr "~" "\n" | sed 's/^\([a-z]\{2\} \)/\1 /' > stripped.txt
	mv -f stripped.txt $@

	rm -f dep-language-regexp.txt cll-codes.txt

scriptNames-l10n.properties: FORCE
	# Exclude deprecated subtags
	printf '^(%s) = ' `cat scriptDeprecated.properties | sed 's/^#.*//' | sed 's/ = .*//' | egrep '[A-Za-z]' | tr "\n" '|' | sed 's/.$$//'` > dep-script-regexp.txt

	( cat scriptNames.properties | egrep '^[A-Z][a-z]{3} =' | LC_ALL=C sort -k1,1 ) | egrep -v -f dep-script-regexp.txt | egrep -v '^(Zinh|Zxxx|Zyyy|Zzzz)' | perl -pe '$$_ = lcfirst($$_)' > $@

	# Remove parentheticals without 'sed -i'
#	cat $@ | sed 's/^\([^ =]*\) *= *\(.*\)  *\((.*)\)$$/# \2 \3~\1 = \2/' | tr "~" "\n" > stripped.txt
#	mv -f stripped.txt $@

	rm -f dep-script-regexp.txt

regionNames-l10n.properties: FORCE
	# Exclude deprecated subtags
	printf '^(%s) = ' `cat regionDeprecated.properties | sed 's/^#.*//' | sed 's/ = .*//' | egrep '[A-Z]' | tr "\n" '|' | sed 's/.$$//'` > dep-region-regexp.txt

	( cat regionNames.properties | egrep '^([A-Z]{2}|[0-9]{3}) =' | LC_ALL=C sort -k1,1 | sed '/^[A-Z][A-Z] /s/^/!/' | LC_ALL=C sort -k1,1 | sed 's/^!//' ) | egrep -v -f dep-region-regexp.txt | egrep -v '^(AA|ZZ)' | perl -pe 's/^([A-Z]{2})/lc($$1) /e' | sed 's/^\([a-z]\{2\} \)/\1 /' > $@

	# Remove parentheticals without 'sed -i'
#	cat $@ | sed 's/^\([^ =]*\) *= *\(.*\)  *\((.*)\)$$/# \2 \3~\1 = \2/' | tr "~" "\n" > stripped.txt
#	mv -f stripped.txt $@

	rm -f dep-region-regexp.txt

FORCE:
