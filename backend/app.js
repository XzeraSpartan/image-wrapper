require('dotenv').config();
const express = require('express');
const axios = require('axios');
const multer = require('multer');
const fs = require('fs');
const { uploadImage, getImageUrl } = require('./database/supabase');
const storage = multer.memoryStorage(); // using memory storage
const upload = multer({ storage: storage });
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());


app.post('/upload-image', upload.single('image'), async (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded.');
    }

    try {
        const uploadResult = await uploadImage(req.file);
        res.json({ message: 'Image uploaded successfully!', data: uploadResult });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.get('/get-image-url', async (req, res) => {
    const path = req.query.path;
    console.log(path)
    try {
        const url = await getImageUrl(path);
        if (!url) {
            return res.status(404).json({ message: "URL not found." });
        }
        res.json({ message: 'URL retrieved successfully!', url: url });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.post('/remove-background', async (req, res) => {
    const imageUrl = req.body.imageUrl;
  
    try {
      const response = await axios.post('https://api.remove.bg/v1.0/removebg', {
        image_url: imageUrl,
        size: 'auto'
      }, {
        headers: {
          'X-Api-Key': process.env.REMOVE_BG_API_KEY
        },
        responseType: 'arraybuffer'
      });
  
      // Consider dynamically naming the output file to avoid overwrite and manage multiple users
      const outputPath = `processed_images/no-bg-${Date.now()}.png`; // Generates a unique file name based on timestamp
  
      fs.writeFile(outputPath, response.data, 'binary', err => {
        if (err) {
          console.error('Failed to save the image:', err);
          return res.status(500).send('Failed to save the image');
        }
        res.send(`Image processed and saved as ${outputPath}`);
      });
    } catch (error) {
      console.error(`Error processing image: ${error.message}`);
      res.status(500).send(`Error processing image: ${error.message}`);
    }
  });




app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

