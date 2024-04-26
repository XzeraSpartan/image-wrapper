const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

const uploadImage = async (file) => {
    // Ensure you're passing a Buffer or a stream. If using multer's memory storage, file.buffer will be a Buffer.
    const { data, error } = await supabase.storage
        .from('images')
        .upload(`uploads/${file.originalname}`, file.buffer, {
            contentType: file.mimetype, // Optional: Helps with setting the correct MIME type
            upsert: false // Optional: Set to true to overwrite files with the same name
        });

    if (error) throw new Error(error.message);
    return data;
};


const getImageUrl = async (path) => {
    const { data, error } = await supabase.storage
        .from('images')
        .getPublicUrl(path);
        console.log(data);

    if (error) {
        console.error('Error fetching public URL:', error.message);
        throw new Error(error.message);
    }
    console.log('Fetched URL:', data.publicUrl);  // Ensure this logs the expected URL
    return data.publicUrl;
};




module.exports = { uploadImage, getImageUrl };
