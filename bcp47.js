var BCP47 = {
	BCP47:				function ( tag ) {
		return this.parseTag( tag );
	},

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

	parseTag:			function ( tag ) {
		const ALPHA = '[A-Za-z]';
		const DIGIT = '[0-9]';
		const ALPHANUM = '[A-Za-z0-9]';
		const SINGLETON = '[A-WY-Za-wy-z0-9]';

		var extlang = ALPHA + '{3}' + '(?:-' + ALPHA + '{3}){0,2}';
		var language = '(' + ALPHA + '{2,3})' + '(?:-(' + extlang + '))?';
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

		var languageTagRE = new RegExp( languageTag );

		var subtags = languageTagRE.exec( tag );

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

		var parsedTag = ( !subtags ) ? false : {
			tag:		tag,
			type:		( ( subtags[1] ) ? 'grandfathered' : ( ( subtags[2] ) ? 'standard' : 'private' ) ),
			language:	( ( subtags[3] ) ? subtags[3] : null ),
			extlangs:	this._parseExtlangs( subtags[4] ),
			script:		( ( subtags[5] ) ? subtags[5] : null ),
			region:		( ( subtags[6] ) ? subtags[6] : null ),
			variants:	this._parseVariants( subtags[7] ),
			extensions:	this._parseExtensions( subtags[8] ),
			privateUse:	this._parsePrivateUse( subtags[9] ),
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
			var preferredValue;

			switch( parsedTag.tag ) {
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

				case 'sgn-BE-FR':
					preferredValue = 'sfb';
				break;

				case 'sgn-BE-NL':
					preferredValue = 'vgt';
				break;

				case 'sgn-CH-DE':
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

				case 'en-GB-oed':
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
}