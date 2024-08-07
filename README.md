<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Email Viewer</title>
</head>
<body>
    <h1>Emails</h1>
    <table border="1">
        <thead>
            <tr>
                <th>Subject</th>
                <th>Sender</th>
                <th>Body</th>
            </tr>
        </thead>
        <tbody>
            {% for email in emails %}
            <tr>
                <td>{{ email.subject }}</td>
                <td>{{ email.sender }}</td>
                <td>{{ email.body }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
