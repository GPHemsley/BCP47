<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8" />
	<title>BCP 47</title>

	<script type="text/javascript" src="bcp47.js"></script>
	<script type="text/javascript">
		var acceptLanguage = '<?php print @$_SERVER['HTTP_ACCEPT_LANGUAGE']; ?>';
		var acceptLangs = BCP47.parseAcceptLanguage( acceptLanguage );

		console.log( acceptLangs );

		var priorityList = [];
		var availableList = [ 'en-GB', 'en-US', 'en-ZA', 'es-AR', 'es-CL', 'es-ES', 'es-MX', 'ga-IE', 'zh-Hant', 'zh-Hans' ];

		for( var i = 0; i < acceptLangs.length; i++ ) {
			var tag = BCP47.parseTag( acceptLangs[i].tag );
			console.log( tag );
			priorityList.push( tag.tag );
		}

		var testTag = 'zh-gan-hak-Hans-CN-1901-rozaj-2abc-t-fonipa-u-islamcal-myext-testing-x-private-testing';

		console.log( BCP47.parseTag( testTag ) );
//		BCP47.runTests();

		console.log( availableList );

		console.log( priorityList, BCP47.lookup( priorityList, availableList ) );

		priorityList.shift();
		console.log( priorityList, BCP47.lookup( priorityList, availableList ) );

		priorityList.unshift( testTag );
		console.log( priorityList, BCP47.lookup( priorityList, availableList ) );

		priorityList.unshift( 'zh-Hans-CN' );
		console.log( priorityList, BCP47.lookup( priorityList, availableList ) );

		console.log( [], BCP47.lookup( [], availableList ) );
	</script>
</head>
<body>

</body>
</html>