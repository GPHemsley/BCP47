RAW_DIR = raw/
SUPPORT_DIR = support/
PROP_FULL_DIR = properties/full/
PROP_L10N_DIR = properties/l10n/

all: languageNames.properties scriptNames.properties regionNames.properties

# Get version of languageNames.properties before the overhaul
moz-current.txt: FORCE
	wget -O $(SUPPORT_DIR)$@ 'http://hg.mozilla.org/mozilla-central/raw-file/444e087c6e27/toolkit/locales/en-US/chrome/global/languageNames.properties' 2> /dev/null
	sed -i'.bak' 's/ .*//' $(SUPPORT_DIR)$@

# Stable URL on my site that lists language codes for which there is a
# FLOSS spell checker in existence (summarizing the more extensive
# http://borel.slu.edu/crubadan/stadas.html
moz-spell.txt: FORCE
	wget -O $(SUPPORT_DIR)$@ 'http://borel.slu.edu/ispell/spell.txt' 2> /dev/null

# Get list of languages in which the Google search interface is available
google.txt: FORCE
	wget -O google.html 'http://www.google.com/preferences' 2> /dev/null
	egrep -o '<option value=[a-z][^>]+>' google.html | sed 's/^<option value=//' | sed 's/>//' | sed 's/ .*//' | LC_ALL=C sort -u > $(SUPPORT_DIR)$@
	rm -f preferences google.html

# Get list of active wikipedias
wikipedia.txt: FORCE
	wget -O wiki.html 'http://meta.wikimedia.org/wiki/List_of_Wikipedias' 2> /dev/null
	cat wiki.html | tr -d "\n" | sed 's/<tr>/~&/g' | tr '~' "\n" | egrep '^<tr><td>[0-9]+<' | sed 's/<\/tr>.*/<\/tr>/' | egrep -o '>[a-z][a-z-]+<'  | sed 's/^>//; s/<$$//' | sort -u > $(SUPPORT_DIR)$@
	rm -f wiki.html

# get list of current Mozilla l10n teams (whoever is committed to l10n-central)
moz-teams.txt: FORCE
	wget -O l10n.html 'http://hg.mozilla.org/releases/l10n/mozilla-aurora/' 2> /dev/null
	egrep -o '/mozilla-aurora/[^/]+' l10n.html | sed 's/^\/mozilla-aurora\///' | egrep -v '^(static|x-testing)$$' | sort -u > $(SUPPORT_DIR)$@
	rm -f l10n.html

# * Google adds some deprecated codes; iw, jw, sh (so be it)
# * Spelling adds some sublangs of macrolanguages (als, azj, plt, swh, etc.)
#   that coincide with existing spell checkers (in case they are relabelled)
#   and also some ISO 639-2/-5 codes (e.g. son, ber)
# * Teams currently adds "mai" only (also from spell checking though)
# * Wikipedia adds quite a few, but note many incorrect codes;
#   I'm filtering out incorrect als, nrm, and adding correct codes
#   where deprecated ones are used by WP - lzh, nan, etc.
languageNames.properties: moz-current.txt google.txt moz-spell.txt wikipedia.txt moz-teams.txt $(PROP_FULL_DIR)languageNames.properties
	(cat $(SUPPORT_DIR)moz-current.txt; (cat $(SUPPORT_DIR)google.txt | egrep -v '^xx-'; cat $(SUPPORT_DIR)moz-spell.txt $(SUPPORT_DIR)moz-teams.txt; cat $(SUPPORT_DIR)wikipedia.txt | egrep -v '^(als|nrm|simple)$$'; echo "lzh nan rup sgs vro yue" | tr " " "\n") | sed 's/-.*//') | LC_ALL=C sort -u > cll-codes.txt

	# Exclude deprecated subtags
	printf '^(%s) = ' `cat $(PROP_FULL_DIR)languageDeprecated.properties | sed 's/^#.*//' | sed 's/ = .*//' | egrep '[a-z]' | tr "\n" '|' | sed 's/.$$//'` > dep-language-regexp.txt

	( cat $(PROP_FULL_DIR)languageNames.properties | egrep '^[a-z]{2,8} =' | LC_ALL=C sort -k1,1 | join - cll-codes.txt | sed '/^.. /s/^/@/' | LC_ALL=C sort -k1,1 | sed 's/^@//' ) | egrep -v -f dep-language-regexp.txt > $(PROP_L10N_DIR)$@

	# Remove parentheticals without 'sed -i'
	cat $(PROP_L10N_DIR)$@ | sed 's/^\([^ =]*\) *= *\(.*\)  *\((.*)\)$$/# \2 \3~\1 = \2/' | tr "~" "\n" | sed 's/^\([a-z]\{2\} \)/\1 /' > stripped.txt

	# Add MPL boilerplate
	cat mpl_boilerplate.txt stripped.txt > $(PROP_L10N_DIR)$@

	rm -f dep-language-regexp.txt cll-codes.txt
	rm -f stripped.txt

scriptNames.properties: FORCE
	# Exclude deprecated subtags
	printf '^(%s) = ' `cat $(PROP_FULL_DIR)scriptDeprecated.properties | sed 's/^#.*//' | sed 's/ = .*//' | egrep '[A-Za-z]' | tr "\n" '|' | sed 's/.$$//'` > dep-script-regexp.txt

	( cat $(PROP_FULL_DIR)scriptNames.properties | egrep '^[A-Z][a-z]{3} =' | LC_ALL=C sort -k1,1 ) | egrep -v -f dep-script-regexp.txt | egrep -v '^(Zinh|Zxxx|Zyyy|Zzzz)' | perl -pe '$$_ = lcfirst($$_)' > $(PROP_L10N_DIR)$@

	# Remove parentheticals without 'sed -i'
#	cat $(PROP_L10N_DIR)$@ | sed 's/^\([^ =]*\) *= *\(.*\)  *\((.*)\)$$/# \2 \3~\1 = \2/' | tr "~" "\n" > stripped.txt
	cat $(PROP_L10N_DIR)$@ > stripped.txt

	# Add MPL boilerplate
	cat mpl_boilerplate.txt stripped.txt > $(PROP_L10N_DIR)$@

	rm -f dep-script-regexp.txt
	rm -f stripped.txt

regionNames.properties: FORCE
	# Exclude deprecated subtags
	printf '^(%s) = ' `cat $(PROP_FULL_DIR)regionDeprecated.properties | sed 's/^#.*//' | sed 's/ = .*//' | egrep '[A-Z]' | tr "\n" '|' | sed 's/.$$//'` > dep-region-regexp.txt

	( cat $(PROP_FULL_DIR)regionNames.properties | egrep '^([A-Z]{2}|[0-9]{3}) =' | LC_ALL=C sort -k1,1 | sed '/^[A-Z][A-Z] /s/^/!/' | LC_ALL=C sort -k1,1 | sed 's/^!//' ) | egrep -v -f dep-region-regexp.txt | egrep -v '^(AA|ZZ)' | perl -pe 's/^([A-Z]{2})/lc($$1) /e' | sed 's/^\([a-z]\{2\} \)/\1 /' > $(PROP_L10N_DIR)$@

	# Remove parentheticals without 'sed -i'
#	cat $(PROP_L10N_DIR)$@ | sed 's/^\([^ =]*\) *= *\(.*\)  *\((.*)\)$$/# \2 \3~\1 = \2/' | tr "~" "\n" > stripped.txt
	cat $(PROP_L10N_DIR)$@ > stripped.txt

	# Add MPL boilerplate
	cat mpl_boilerplate.txt stripped.txt > $(PROP_L10N_DIR)$@

	rm -f dep-region-regexp.txt
	rm -f stripped.txt

FORCE:
