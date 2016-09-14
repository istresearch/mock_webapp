<html>
<head>
	<title>{{title}}</title>
</head>
<body>
	<h1>{{title}}</h1>
	<form method="post">
		<table>	
			<tr><th>Username:</th><td><input name="username"></td></tr>
			<tr><th>Password:</th><td><input type="password" name="password"></td></tr>
			<tr><th></th><td><input type="submit"></td></tr>
		</table>
	</form>
	</div>
	<p><strong>Cookies:</strong></p>
	<pre>{{!cookies}}</pre>
	<p><strong>IP Address:</strong> {{ip}}</p>
</body>
</html>