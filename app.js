import http from 'http';
import mongoose from 'mongoose';


mongoose.connect('mongodb+srv://gaelbaret:BwNBM8mWRK0bk6t4@se19.4zsg5oo.mongodb.net/');


const Blog = mongoose.model('blogs', new mongoose.Schema({
    title: String,
    body: String,
    date: { type: Date, default: Date.now }
}));


const server = http.createServer((req, res) => {
    // Set CORS headers so Python can talk to this server
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }


    if (req.url === '/api/posts' && req.method === 'GET') {
        Blog.find().sort({ date: -1 }).then(posts => {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(posts));
        });
    }

   
    else if (req.url === '/api/add' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', async () => {
            const newPost = new Blog(JSON.parse(body));
            await newPost.save();
            res.writeHead(201, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: "success" }));
        });
    }

   
    else if (req.url.startsWith('/api/delete/') && req.method === 'DELETE') {
        const id = req.url.split('/')[3];
        Blog.findByIdAndDelete(id).then(() => {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: "deleted" }));
        });
    }


    else if (req.url.startsWith('/api/edit/') && req.method === 'POST') {
        const id = req.url.split('/')[3];
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', async () => {
            const data = JSON.parse(body);
            await Blog.findByIdAndUpdate(id, { title: data.title, body: data.body });
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: "updated" }));
        });
    }


  
    else {
        res.writeHead(404);
        res.end("Not Found");
    }
});


server.listen(3000, () => {
    console.log('📡 JavaScript Database Service running at http://localhost:3000');
});