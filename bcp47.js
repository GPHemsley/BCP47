String.prototype.toUpperCaseFirst = function() {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

function BCP47Parser() {};

BCP47Parser.prototype = {
	_parseExtlangs:		function ( extlangs ) {
		if( !extlangs ) {
			return [];
		}

		parsedExtlangs = extlangs.split( '-' );

		return parsedExtlangs;
	},

	_parseVariants:		function ( variants ) {
		if( !variants ) {
			return [];
		}

		// 'variants' comes with a leading '-'
		parsedVariants = variants.substr( 1 ).split( '-' );

		return parsedVariants;
	},

	_parseExtensions:	function ( extensions ) {
		if( !extensions ) {
			return {};
		}

		var extensionsRE = new RegExp( '(?:-(([A-WY-Za-wy-z0-9])((?:-[A-Za-z0-9]{2,8})+))+)', 'g' );

		var parsedExtensions = {};

		var eachExtension;
		while( ( eachExtension = extensionsRE.exec( extensions ) ) != null ) {
			if( parsedExtensions[eachExtension[2]] ) {
				return false;
			}

			// Each extension group comes with a leading '-'
			parsedExtensions[eachExtension[2]] = eachExtension[3].substr( 1 ).split( '-' );
		}

		return parsedExtensions;
	},

	_parsePrivateUse:	function ( privateUse ) {
		if( !privateUse ) {
			return [];
		}

		// 'privateUse' comes with a leading 'x-'
		parsedPrivateUse = privateUse.substr( 2 ).split( '-' );

		return parsedPrivateUse;
	},

	getRelatedTags:		function( tag ) {
		var relatedTags = [];

		switch( tag ) {
			// XXX: This will cause an infinite loop if 'en-US' is not in availableList.
			case 'en':
			default:
				relatedTags.push( 'en-US' );
			break;
		}

		return relatedTags;
	},

	// Get the Preferred-Value for a given grandfathered language tag.
	getPreferredValue: function( tag ) {
		var preferredValue;

		switch( tag ) {
			case 'i-ami':
				preferredValue = 'ami';
			break;

			case 'i-bnn':
				preferredValue = 'bnn';
			break;

			case 'i-hak':
				preferredValue = 'hak';
			break;

			case 'i-klingon':
				preferredValue = 'tlh';
			break;

			case 'i-lux':
				preferredValue = 'lb';
			break;

			case 'i-navajo':
				preferredValue = 'nv';
			break;

			case 'i-pwn':
				preferredValue = 'pwn';
			break;

			case 'i-tao':
				preferredValue = 'tao';
			break;

			case 'i-tay':
				preferredValue = 'tay';
			break;

			case 'i-tsu':
				preferredValue = 'tsu';
			break;

			case 'sgn-be-fr':
				preferredValue = 'sfb';
			break;

			case 'sgn-be-nl':
				preferredValue = 'vgt';
			break;

			case 'sgn-ch-de':
				preferredValue = 'sgg';
			break;

			case 'art-lojban':
				preferredValue = 'jbo';
			break;

			case 'no-bok':
				preferredValue = 'nb';
			break;

			case 'no-nyn':
				preferredValue = 'nn';
			break;

			case 'zh-guoyu':
				preferredValue = 'cmn';
			break;

			case 'zh-hakka':
				preferredValue = 'hak';
			break;

			case 'zh-min-nan':
				preferredValue = 'nan';
			break;

			case 'zh-xiang':
				preferredValue = 'hsn';
			break;

			case 'en-gb-oed':
			case 'i-default':
			case 'i-enochian':
			case 'i-mingo':
			case 'cel-gaulish':
			case 'zh-min':
			default:
				// No 'Preferred-Value'
				preferredValue = false;
			break;
		}

		return preferredValue;
	},

	// Parse a language tag string into a parsedTag object.
	parseTag: function ( tag ) {
		const ALPHA = '[A-Za-z]';
		const DIGIT = '[0-9]';
		const ALPHANUM = '[A-Za-z0-9]';
		const SINGLETON = '[A-WY-Za-wy-z0-9]';

		var extlang = ALPHA + '{3}' + '(?:-' + ALPHA + '{3}){0,2}';
		var language = '(' + ALPHA + '{2,3}|\\*)' + '(?:-(' + extlang + '))?';
		var script = ALPHA + '{4}';
		var region = '(?:' + ALPHA + '{2}|' + DIGIT + '{3})';
		var variant = '(?:' + ALPHANUM + '{5,8}|' + DIGIT + ALPHANUM + '{3})';
		var extension = SINGLETON + '(?:-' + ALPHANUM + '{2,8})+';
		var privateuse = 'x' + '(?:-' + ALPHANUM + '{1,8})+';
		var langtag = '(' + language + ')' + '(?:-(' + script + '))?' + '(?:-(' + region + '))?' + '((?:-' + variant + ')*)' + '((?:-' + extension + ')*)' + '(?:-(' + privateuse + '))?';

		var irregular = '(?:en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon|i-lux|i-mingo|i-navajo|i-pwn|i-tao|i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE)';
		var regular = '(?:art-lojban|cel-gaulish|no-bok|no-nyn|zh-guoyu|zh-hakka|zh-min|zh-min-nan|zh-xiang)';
		var grandfathered = '(' + irregular + '|' + regular + ')';

		var languageTag = '^(?:' + grandfathered + '|' + privateuse + '|' + langtag + ')$';

		var languageTagRE = new RegExp( languageTag, 'i' );

		var subtags = languageTagRE.exec( tag.toLowerCase() );

		/*
			0 : full tag
			1 : grandfathered
			2 : language + extlangs
			3 : language
			4 : extlangs
			5 : script
			6 : region
			7 : variants (with leading '-')
			8 : all extensions and their parameters (with leading '-')
			9 : private use subtags

			Thus,
				if 1 then grandfathered tag
				elseif 2 then regular tag
				else (!1 && !2) private use tag
		*/

		if (!subtags) {
			return false;
		}

		var parsedTag = {
			tag:		tag,
			type:		( ( subtags[1] ) ? 'grandfathered' : ( ( subtags[2] ) ? ( ( subtags[3] == '*' ) ? 'range' : 'standard' ) : 'private' ) ),
			language:	( ( subtags[3] ) ? subtags[3] : null ),
			extlangs:	this._parseExtlangs( subtags[4] ),
			script:		( ( subtags[5] ) ? subtags[5].toUpperCaseFirst() : null ),
			region:		( ( subtags[6] ) ? subtags[6].toUpperCase() : null ),
			variants:	this._parseVariants( subtags[7] ),
			extensions: this._parseExtensions( subtags[8] ),
			privateUse: this._parsePrivateUse( subtags[9] ),
		};

		if( parsedTag.extensions === false ) {
			return false;
		}

		if( parsedTag.type == 'private' ) {
			parsedTag = {
				tag:	parsedTag.tag,
				type:	parsedTag.type,
			};
		} else if( parsedTag.type == 'grandfathered' ) {
			// Do fancy processing to parse equivalent tag
			var preferredValue = this.getPreferredValue( parsedTag.tag );

			if( preferredValue ) {
				parsedTag = this.parseTag( preferredValue );
			} else {
				// No 'Preferred-Value'
				parsedTag = {
					tag:	parsedTag.tag,
					type:	parsedTag.type,
				};
			}
		}

		return parsedTag;
	},

	makeTag:				function( parsedTag ) {
		// All valid parsed tags should have a 'tag' and a 'type'.
		if( !parsedTag.tag || !parsedTag.type ) {
			return false;
		}

		// Private-use and grandfathered tags are atomic.
		if( ( parsedTag.type == 'private' ) || ( parsedTag.type == 'grandfathered' ) ) {
			return parsedTag.tag;
		}

		var tag = parsedTag.language;

		if( parsedTag.extlangs.length > 0 ) {
			tag += '-' + parsedTag.extlangs.join( '-' );
		}

		if( parsedTag.script !== null ) {
			tag += '-' + parsedTag.script;
		}

		if( parsedTag.region !== null ) {
			tag += '-' + parsedTag.region;
		}

		if( parsedTag.variants.length > 0 ) {
			tag += '-' + parsedTag.variants.join( '-' );
		}

		if( parsedTag.extensions.length > 0 ) {
			for( var i = 'a'; i <= 'z'; i++ ) {
				if( i == 'x' ) {
					continue;
				}

				if( ( parsedTag.extensions[i] != undefined ) && ( parsedTag.extensions[i].length > 0 ) ) {
					tag += '-' + i + '-' + parsedTag.extensions[i].join( '-' );
				}
			}
		}

		if( parsedTag.privateUse.length > 0 ) {
			tag += '-x-' + parsedTag.privateUse.join( '-' );
		}

		return tag;
	},

	lookup:					function( priorityList, availableList ) {
		// First check for exact matches.
		for( var i = 0; i < priorityList.length; i++ ) {
			priorityList = priorityList.concat( this.getRelatedTags( priorityList[i] ) );

			if( availableList.indexOf( priorityList[i] ) > -1 ) {
				return priorityList[i];
			}
		}

		// No exact match, so do Lookup matching.
		for( var i = 0; i < priorityList.length; i++ ) {
/*			var tag = this.parseTag( priorityList[i] );

			// Private-use and grandfathered tags are atomic.
			if( ( tag.type == 'private' ) || ( tag.type == 'grandfathered' ) ) {
				continue;
			}

			while( tag.privateUse.length > 0 ) {
				tag.privateUse.pop();

				tag = this.makeTag( tag );

				if( availableList.indexOf( tag.tag ) > -1 ) {
					return tag.tag;
				}
			}

			while( tag.extensions.length > 0 ) {
				for( var j = 'a'; j <= 'z'; j++ ) {
					if( j == 'x' ) {
						continue;
					}

					if( tag.extensions[j] != undefined ) {
						while( tag.extensions[j].length > 0 ) {
							tag.extensions[j].pop();

							tag = this.makeTag( tag );

							if( availableList.indexOf( tag.tag ) > -1 ) {
								return tag.tag;
							}
						}
					}
				}
			}*/

			var tag = priorityList[i].split( '-' );

			while( tag.length > 0 ) {
				tag.pop();

				var newTag = tag.join( '-' );

				priorityList = priorityList.concat( this.getRelatedTags( newTag ) );

				if( availableList.indexOf( newTag ) > -1 ) {
					return newTag;
				}
			}
		}

		// XXX: This is the default. We might want to handle this differently.
		return 'en-US';
	},

	parseAcceptLanguage:	function( acceptLanguage ) {
		var languages = acceptLanguage.split( ',' );
		var acceptLangs = [];

		for( var i = 0; i < languages.length; i++ ) {
			var langSplit = languages[i].split( ';' );
			var langTag = langSplit[0];

			acceptLangs[i] = { tag: langTag, q: 1.000 };

			for( var j = 1; j < langSplit.length; j++ ) {
				var langParam = langSplit[j].split( '=' );

				if( langParam[0] == 'q' ) {
					acceptLangs[i] = { tag: langTag, q: parseFloat( langParam[j] ) };
				}
			}
		}

		// Ensure language tags are sorted by quality value
		function compareQualityValues( a, b ) {
			if( a.q > b.q ) {
				return -1;
			}

			if( a.q < b.q ) {
				return 1;
			}

			return 0;
		}

		return acceptLangs.sort( compareQualityValues );
	},

	runTests:			function () {
		// Tests
		console.log( this.parseTag( 'sr-Latn-RS' ), this.parseTag( 'es-419' ), this.parseTag( 'sr-Cyrl-RS' ) );
		// - Valid
		console.log( 'Simple language subtag:', this.parseTag( 'de' ), this.parseTag( 'fr' ), this.parseTag( 'ja' ), this.parseTag( 'i-enochian' ) );
		console.log( 'Language subtag plus Script subtag:', this.parseTag( 'zh-Hant' ), this.parseTag( 'zh-Hans' ), this.parseTag( 'sr-Cyrl' ), this.parseTag( 'sr-Latn' ) );
		console.log( 'Extended language subtags and their primary language subtag counterparts:', this.parseTag( 'zh-cmn-Hans-CN' ), this.parseTag( 'cmn-Hans-CN' ), this.parseTag( 'zh-yue-HK' ), this.parseTag( 'yue-HK' ) );
		console.log( 'Language-Script-Region:', this.parseTag( 'zh-Hans-CN' ), this.parseTag( 'sr-Latn-RS' ) );
		console.log( 'Language-Variant:', this.parseTag( 'sl-rozaj' ), this.parseTag( 'sl-rozaj-biske' ), this.parseTag( 'sl-nedis' ) );
		console.log( 'Language-Region-Variant:', this.parseTag( 'de-CH-1901' ), this.parseTag( 'sl-IT-nedis' ) );
		console.log( 'Language-Script-Region-Variant:', this.parseTag( 'hy-Latn-IT-arevela' ) );
		console.log( 'Language-Region:', this.parseTag( 'de-DE' ), this.parseTag( 'en-US' ), this.parseTag( 'es-419' ) );
		console.log( 'Private use subtags:', this.parseTag( 'de-CH-x-phonebk' ), this.parseTag( 'az-Arab-x-AZE-derbend' ) );
		console.log( 'Private use registry values:', this.parseTag( 'x-whatever' ), this.parseTag( 'qaa-Qaaa-QM-x-southern' ), this.parseTag( 'de-Qaaa' ), this.parseTag( 'sr-Latn-QM' ), this.parseTag( 'sr-Qaaa-RS' ) );
		console.log( 'Tags that use extensions:', this.parseTag( 'en-US-u-islamcal' ), this.parseTag( 'zh-CN-a-myext-x-private' ), this.parseTag( 'en-a-myext-b-another' ) );
		// - Invalid
		console.log( 'Some Invalid Tags:', this.parseTag( 'de-419-DE' ), this.parseTag( 'a-DE' ), this.parseTag( 'ar-a-aaa-b-bbb-a-ccc' ) );

		console.log( this.parseTag( 'zh-gan-hak-Hans-CN-1901-rozaj-2abc-t-fonipa-u-islamcal-myext-testing-x-private-testing' ) );

		console.log( this.parseTag( 'en-GB-oed' ) );

		console.log( this.parseTag( 'zh-min-nan' ) );

		console.log( this.parseTag( 'x-whatever' ) );
	}
};

var BCP47Parser = new BCP47Parser;

function BCP47() {};

BCP47.prototype = {
	IsStructurallyValidLanguageTag: function(locale) {
		return !!BCP47Parser.parseTag(locale);
	},

	CanonicalizeLanguageTag: function(locale) {
		return BCP47Parser.makeTag(BCP47Parser.parseTag(locale));
	},

	DefaultLocale: function() {
		return window.navigator.language;
	},

	CanonicalizeLocaleList: function(locales) {
		if (locales === undefined) {
			return [];
		}

		let seen = [];

		if (typeof locales === 'string') {
			locales = [ locales ];
		}

		let O = Object(locales);

		// ToUint32(lenValue)
		let len = O.length >>> 0;

		for (let k = 0; k < len; k++) {
			if (k in O) {
				let kValue = O[k];

				if (!(typeof kValue === 'string' || typeof kValue === 'object')) {
					throw TypeError;
				}

				let tag = String(kValue);

				if (!this.IsStructurallyValidLanguageTag(tag)) {
					throw RangeError;
				}

				tag = this.CanonicalizeLanguageTag(tag);

				if (!(tag in seen)) {
					seen.push(tag);
				}
			}
		}

		return seen;
	},

	BestAvailableLocale: function(availableLocales, locale) {
		if (!this.IsStructurallyValidLanguageTag(locale)) {
			return undefined;
		}

		let candidate = this.CanonicalizeLanguageTag(locale);

		while (candidate.length > 0) {
			if (availableLocales.indexOf(candidate) !== -1) {
				return candidate;
			}

			let pos = candidate.lastIndexOf('-');

			if (pos === -1) {
				return undefined;
			}

			// Skip singletons.
			if (pos >= 2 && candidate[pos - 2] === '-' ) {
				pos -= 2;
			}

			candidate = candidate.substring(0, pos);
		}
	},

	LookupMatcher: function(availableLocales, requestedLocales) {
		let len = requestedLocales.length;
		let availableLocale = undefined;

		for (let i = 0; i < len && availableLocale == undefined; i++) {
			var locale = requestedLocales[i];

			// XXX: We don't support the Unicode extensions yet.
			var noExtensionsLocale = locale;

			availableLocale = this.BestAvailableLocale(availableLocales, noExtensionsLocale);
		}

		// XXX: Is this a Record?
		let result = {};

		if (availableLocale !== undefined) {
			result.locale = availableLocale;

			// XXX: We don't support the Unicode extensions yet.
			if (locale !== noExtensionsLocale) {
				// XXX: These need to be expanded.
				let extension;
				let extensionIndex;

				result.extension = extension;
				result.extensionIndex = extensionIndex;
			}
		} else {
			result.locale = this.DefaultLocale();
		}

		return result;
	},

	BestFitMatcher: function(availableLocales, requestedLocales) {
		// XXX: Not yet implemented.
		return undefined;
	},

	ResolveLocale: function(availableLocales, requestedLocales, options, relevantExtensionKeys, localeData) {
		let matcher = options.localeMatcher;

		if (matcher === 'lookup') {
			var r = this.LookupMatcher(availableLocales, requestedLocales);
		} else {
			var r = this.BestFitMatcher(availableLocales, requestedLocales);
		}

		let foundLocale = r.locale;

		if (r.hasOwnProperty('extension')) {
			let extension = r.extension;
			let extensionIndex = r.extensionIndex;

			let extensionSubtags = extension.split('-');
			let extensionSubtagsLength = extensionSubtags.length;
		}

		let result = {};

		result.dataLocale = foundLocale;

		let supportedExtension = '-u';

		for (let i = 0, len = relevantExtensionKeys.length; i < len; i++) {
			let key = relevantExtensionKeys[String(i)];
			let foundDataLocale = localeData.foundLocale;
			let keyLocaleData = foundLocaleData.key;
			let value = keyLocaleData.'0';
			let supportedExtensionAddition = '';

			if (extensionSubtags !== undefined) {
				let keyPos = extensionSubtags.indexOf(key);

				if (keyPos !== -1) {
					if ((keyPos + 1 < extensionSubtagsLength) && (extensionSubtags[String(keyPos + 1)] > 2)) {
						let requestedValue = extensionSubtags[String(keyPos + 1)];
						var valuePos = keyLocaleData.indexOf(requestedValue);

						if (valuePos !== -1) {
							var value = requestedValue;
							var supportedExtensionAddition = '-' + key + '-' + value;
						}
					} else {
						var valuePos = keyLocaleData.indexOf('true');

						if (valuePos !== -1) {
							var value = 'true';
						}
					}
				}
			}

			// XXX: Is this the same as "has a field [[<key>]]"?
			if (options.hasOwnProperty(key)) {
				let optionsValue = options[key];

				if (keyLocaleData.indexOf(optionsValue) !== -1) {
					if (optionsValue !== value) {
						var value = optionsValue;
						var supportedExtensionAddition = '';
					}
				}
			}

			result[key] = value;
			supportedExtension += supportedExtensionAddition;
		}

		if (supportedExtension.length > 2) {
			// XXX: Check that this index is not off by one.
			let preExtension = foundLocale.substring(0, extensionIndex - 1);
			let postExtension = foundLocale.substring(extensionIndex);
			foundLocale = preExtension + supportedExtension + postExtension;
		}

		result.locale = foundLocale;

		return result;
	},

	LookupSupportedLocales: function(availableLocales, requestedLocales) {
		let len = requestedLocales.length;
		let subset = [];

		for (let k = 0; k < len; k++) {
			let locale = requestedLocales[k];

			// XXX: We don't support the Unicode extensions yet.
			let noExtensionsLocale = locale;

			let availableLocale = this.BestAvailableLocale(availableLocales, noExtensionsLocale);

			if (availableLocale !== undefined) {
				subset.push(availableLocale);
			}
		}

		// XXX: Do we need to distinguish between List and Array?
		let subsetArray = subset;

		return subsetArray;
	},

	BestFitSupportedLocales: function(availableLocales, requestedLocales) {
		// XXX: Not yet implemented.
		return undefined;
	},

	SupportedLocales: function(availableLocales, requestedLocales, options) {
		if (options !== undefined) {
			options = Object(options);

			var matcher = options.localeMatcher;

			if (matcher !== undefined) {
				matcher = String(matcher);

				if (!(matcher === 'lookup' || matcher === 'best fit')) {
					throw RangeError;
				}
			}
		}

		if (matcher === undefined || matcher === 'best fit') {
			var subset = this.BestFitSupportedLocales(availableLocales, requestedLocales);
		} else {
			var subset = this.LookupSupportedLocales(availableLocales, requestedLocales);
		}

		// XXX: Make sure this is correct.
		for (let P in subset) {
			let desc = Object.getOwnPropertyDescriptor(subset, P);

			desc.writable = false;
			desc.configurable = false;

			// XXX: Where does the third argument "true" come in?
			Object.defineProperty(subset, P, desc);
		}

		return subset;
	},

	GetOption: function(options, property, type, values, fallback) {
		let value = options[property];

		if (value !== undefined) {
			// Type is either boolean or string
			if (typeof value === 'boolean') {
				value = Boolean(value);
			} else if (typeof value == 'string') {
				value = String(value);
			}

			if (values !== undefined) {
				if (!(value in values)) {
					throw RangeError;
				}
			}
		} else {
			return fallback;
		}
	},

	GetNumberOption: function(options, property, minimum, maximum, fallback) {
		let value = options[property];

		if (value !== undefined) {
			value = Number(value);

			if (value == NaN || value < minimum || value > maximum) {
				throw RangeError;
			}
		} else {
			return fallback;
		}
	},
};

var BCP47 = new BCP47;

