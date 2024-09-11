html_start = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Articles</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .article {
            margin-bottom: 40px;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .article img {
            max-width: 50%;
            height: auto;
            display: block;
            margin: 20px auto;
        }
        .Read-more:link, .Read-more:visited {
            background-color: #f44336;
            color: white;
            padding: 14px 25px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
        }
        .Read-more:hover, .Read-more:active {
            background-color: red;
        }
        .img-caption {
            text-align: center;
        }
        h2 {
            color: #333;
        }
        p {
            color: #555;
            text-align: justify;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align: center;">Latest News Articles</h1>
"""
html_end = """
    </div>
</body>
</html>
"""