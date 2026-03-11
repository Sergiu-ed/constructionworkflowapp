const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.static('public')); // Serve static files from 'public' directory
app.use(express.json());

// Basic proxy to backend or frontend placeholder
app.get('/', (req, res) => {
    res.send(`
    <html>
      <head>
        <title>Construction Workflow App</title>
        <style>
          body { font-family: system-ui, sans-serif; padding: 2rem; background-color: #f4f4f5; }
          .container { max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
          h1 { color: #2563eb; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Construction Workflow App</h1>
          <p>The Express frontend is running successfully! It serves as the frontend client for the Flask API.</p>
        </div>
      </body>
    </html>
  `);
});

app.listen(port, () => {
    console.log(`Frontend Express server listening at http://localhost:${port}`);
});
