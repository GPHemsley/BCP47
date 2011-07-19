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

		for( var i = 0; i < acceptLangs.length; i++ ) {
			console.log( BCP47.parseTag( acceptLangs[i].tag ) );
		}

//		console.log( BCP47.parseTag( 'zh-gan-hak-Hans-CN-1901-rozaj-2abc-t-fonipa-u-islamcal-myext-testing-x-private-testing' ) );
//		BCP47.runTests();
	</script>
</head>
<body>

</body>
</html>