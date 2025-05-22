<!DOCTYPE html>
<html>
<head>
    <title>Crop Recommendation Result</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0fff0;
            text-align: center;
            padding: 50px;
        }
        .result-box {
            background: #fff;
            padding: 20px;
            border-radius: 20px;
            display: inline-block;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        img {
            width: 300px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="result-box">
        <h2>Recommended Crop:</h2>
        <h1>{{ crop }}</h1>
        <img src="{{ url_for('static', filename='images/' + image) }}" alt="{{ crop }}">
        <br><br>
        <button onclick="speak()">🔊 Hear Recommendation</button>
    </div>

    <script>
        function speak() {
            const msg = new SpeechSynthesisUtterance("The recommended crop is {{ crop }}.");
            window.speechSynthesis.speak(msg);
        }
    </script>
</body>
</html>
