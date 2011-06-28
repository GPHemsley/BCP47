
all: languageNames-l10n.properties

# Get version of languageNames.properties before the overhaul
moz-current.txt: FORCE
	wget -O $@ 'http://hg.mozilla.org/mozilla-central/raw-file/444e087c6e27/toolkit/locales/en-US/chrome/global/languageNames.properties' 2> /dev/null
	sed -i 's/ .*//' $@

# Stable URL on my site that lists language codes for which there is a
# FLOSS spell checker in existence (summarizing the more extensive
# http://borel.slu.edu/crubadan/stadas.html
moz-spell.txt: FORCE
	wget -O $@ 'http://borel.slu.edu/ispell/spell.txt' 2> /dev/null

# Get list of languages in which the Google search interface is available
moz-google.txt: FORCE
	wget -O google.html 'http://www.google.com/language_tools?hl=en' 2> /dev/null
	egrep -o 'hl=[^&"]+' google.html | sed 's/^hl=//' | LC_ALL=C sort -u > $@
	rm -f google.html

# Get list of active wikipedias
moz-wiki.txt: FORCE
	wget -O wiki.html 'http://meta.wikimedia.org/wiki/List_of_Wikipedias' 2> /dev/null
	cat wiki.html | tr -d "\n" | sed 's/<tr>/\n\n\n&/g'  | egrep 'Special:Stat' | egrep '^<tr><td>[0-9]+</td>' | egrep -o '>[a-z][a-z-]+<' | sed 's/^>//; s/<$$//' | sort -u | egrep -v '^closed$$' > $@
	rm -f wiki.html

# get list of current Mozilla l10n teams (whoever is committed to l10n-central)
moz-teams.txt: FORCE
	wget -O l10n.html 'http://hg.mozilla.org/l10n-central' 2> /dev/null
	egrep -o '/l10n-central/[^/]+' l10n.html | sed 's/^\/l10n-central\///' | egrep -v '^(static|x-testing)$$' | sort -u > $@
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
	cat languageNames.properties | LC_ALL=C sort -k1,1 | join - cll-codes.txt | sed '/^.. /s/^/A/' | LC_ALL=C sort -k1,1 | sed 's/^A//' > $@
	rm -f cll-codes.txt

FORCE:
